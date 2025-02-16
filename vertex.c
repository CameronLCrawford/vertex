#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>

#define COMMAND_ROM_BYTES 65536
#define PROGRAM_ROM_BYTES 65536

typedef enum
{
    // Input signals
    CTRL_IN3, CTRL_IN2, CTRL_IN1, CTRL_IN0,

    // Output signals
    CTRL_OUT3, CTRL_OUT2, CTRL_OUT1, CTRL_OUT0,

    // ALU signals
    CTRL_ALU3, CTRL_ALU2, CTRL_ALU1, CTRL_ALU0,

    // Counter signals
    CTRL_COUNTER_INC, CTRL_ADDRESS_INC, CTRL_STACK_INC, CTRL_STACK_DEC,

    // Direct moves
    CTRL_MOVE_ADDRESS_COUNTER, CTRL_MOVE_ADDRESS_STACK, CTRL_MOVE_ADDRESS_HL,

    // Flags and addressing
    CTRL_FLAG_OUT1, CTRL_FLAG_OUT0, CTRL_FLAG_IN,

    // Memory
    CTRL_RAM_IN, CTRL_RAM_OUT,

    // Control signals
    CTRL_RESET_MICRO_TICK, CTRL_OUT, CTRL_HALT
} Control;

typedef enum
{
    // No-reg
    REG_NO,

    // Accumulator registers
    REG_A, REG_A_TEMP,

    // HL register pair
    REG_H, REG_L,

    // Counter register pair
    REG_COUNTER_H, REG_COUNTER_L,

    // Address register pair
    REG_ADDRESS_H, REG_ADDRESS_L,

    // Base register pair
    REG_BASE_H, REG_BASE_L,

    // Stack register pair
    REG_STACK_H, REG_STACK_L,

    // Object register pair
    REG_OBJECT_H, REG_OBJECT_L,

    // Stores current instruction
    REG_INSTRUCTION
} Register;

typedef enum
{
    FLAG_ZERO,
    FLAG_SIGN,
    FLAG_CARRY
} Flag;

typedef enum
{
    // No operation
    NOP,

    // Add/subtract
    ADD, SUB,

    // Binary logical
    AND, OR, XOR, NOT,

    // Inc/decrement
    INC, DEC,

    // Shift
    SHR, SHL,

    // Carry conditional
    ADDC, SUBC, INCC, DECC,

    // Unary negate
    UNEG
} AluOp;

typedef struct
{
    uint8_t     dataBus;
    uint32_t    controlBus;
    uint8_t     registers[16];
    uint8_t     flags;                      // only three flag bits used
    uint8_t     microinstructionCounter;    // only four counter bits used
    uint8_t     *ram;                       // dynamically-allocated
    uint32_t    *controlROM;                // dynamically-allocated
} CPUState;

typedef enum
{
    LOG_LEVEL_DEBUG,
    LOG_LEVEL_INFO,
    LOG_LEVEL_ERROR,
} LogLevel;

typedef enum
{
    EXEC_STAGE_INIT,
    EXEC_STAGE_RUN,
    EXEC_STAGE_HALT,
} ExecutionStage;

static LogLevel logLevel = LOG_LEVEL_INFO;
static ExecutionStage executionStage = EXEC_STAGE_INIT;

void logMessage(LogLevel level, const char *format, ...)
{
    if (level < logLevel)
    {
        return;
    }

    const char *levelName;
    switch(level)
    {
        case LOG_LEVEL_DEBUG:
            levelName = "DEBUG";
            break;
        case LOG_LEVEL_INFO:
            levelName = "INFO ";
            break;
        case LOG_LEVEL_ERROR:
            levelName = "ERROR";
            break;
        default:
            levelName = "UNKNOWN";
            break;
    }

    const char *stageName;
    switch(executionStage)
    {
        case EXEC_STAGE_INIT:
            stageName = "INIT";
            break;
        case EXEC_STAGE_RUN:
            stageName = "RUN ";
            break;
        case EXEC_STAGE_HALT:
            stageName = "HALT";
            break;
        default:
            stageName = "UNKNOWN";
            break;
    }

    fprintf(stderr, "[%s] ", levelName);
    fprintf(stderr, "[%s] ", stageName);
    va_list args;
    va_start(args, format);
    vfprintf(stderr, format, args);
    va_end(args);
    fprintf(stderr, "\n");
}

// During the 'tick':
// 1. The current instruction is decoded
// 2. Increment/decrement operations are performed
// 3. Relevant register/RAM data is put onto bus
// 4. ALU calculations are evaluated
void tick(CPUState *cpu)
{
    // 16-bit instruction address
    // Queries control ROM
    uint16_t instructionAddress = 
        (cpu->flags << 12) | 
        (cpu->registers[REG_INSTRUCTION] << 4) |
        (cpu->microinstructionCounter++);
    cpu->controlBus = cpu->controlROM[instructionAddress];
    logMessage(LOG_LEVEL_DEBUG, "Instruction address: 0x%x", instructionAddress);
    logMessage(LOG_LEVEL_DEBUG, "Control bus: 0x%x", cpu->controlBus);

    // Update virtual 16-bit register inc/dec and handle 8-bit overflow
    if ((cpu->controlBus >> CTRL_COUNTER_INC) & 0b1)
    {
        logMessage(LOG_LEVEL_DEBUG, "Incrementing counter register");
        if (++cpu->registers[REG_COUNTER_L] == 0)
        {
            cpu->registers[REG_COUNTER_H]++;
        }
    }
    if ((cpu->controlBus >> CTRL_ADDRESS_INC) & 0b1)
    {
        logMessage(LOG_LEVEL_DEBUG, "Incrementing address register");
        if (++cpu->registers[REG_ADDRESS_L] == 0)
        {
            cpu->registers[REG_ADDRESS_H]++;
        }
    }
    if ((cpu->controlBus >> CTRL_STACK_INC) & 0b1)
    {
        logMessage(LOG_LEVEL_DEBUG, "Incrementing stack register");
        if (++cpu->registers[REG_STACK_L] == 0)
        {
            cpu->registers[REG_STACK_H]++;
        }
    }
    if ((cpu->controlBus >> CTRL_STACK_DEC) & 0b1)
    {
        logMessage(LOG_LEVEL_DEBUG, "Decrementing stack register");
        if (--cpu->registers[REG_STACK_L] == 255)
        {
            cpu->registers[REG_STACK_H]--;
        }
    }

    // Calculate and set register output state
    // Because controlBus bits are stored [..., out3, out2, out1, out0, ...]
    uint8_t registerOutCode = (cpu->controlBus >> CTRL_OUT3) & 0b1111;
    logMessage(LOG_LEVEL_DEBUG, "Register out code: %d", registerOutCode);
    if (registerOutCode > 0)
    {
        cpu->dataBus = cpu->registers[registerOutCode];
        logMessage(LOG_LEVEL_DEBUG, "Register out new bus value: %d", cpu->dataBus);
    }

    // Calculate and set flag output state
    uint8_t flagOutCode = (cpu->controlBus >> CTRL_FLAG_OUT1) & 0b11;
    logMessage(LOG_LEVEL_DEBUG, "Flag out code: %d", flagOutCode);
    switch(flagOutCode)
    {
        case 0: // no flag
            break;
        case 1: // zero flag
            cpu->dataBus = (cpu->flags >> FLAG_ZERO) & 0b1;
            logMessage(LOG_LEVEL_DEBUG, "Zero flag out new bus value: %d", cpu->dataBus);
            break;
        case 2: // sign flag
            cpu->dataBus = (cpu->flags >> FLAG_SIGN) & 0b1;
            logMessage(LOG_LEVEL_DEBUG, "Sign flag out new bus value: %d", cpu->dataBus);
            break;
        case 3: // all flags (status)
            cpu->dataBus = cpu->flags;
            logMessage(LOG_LEVEL_DEBUG, "All flag out new bus value: %d", cpu->dataBus);
            break;
        default:
            break;
    }

    // Handle RAM out
    if ((cpu->controlBus >> CTRL_RAM_OUT) & 0b1)
    {
        uint16_t ramAddress = 
            (cpu->registers[REG_ADDRESS_H] << 8) |
            (cpu->registers[REG_ADDRESS_L]);
        logMessage(LOG_LEVEL_DEBUG, "RAM out address: 0x%x", ramAddress);
        cpu->dataBus = cpu->ram[ramAddress];
        logMessage(LOG_LEVEL_DEBUG, "RAM out new bus value: %d", cpu->dataBus);
    }

    // Calculate and set ALU state
    uint8_t aluCode = (cpu->controlBus >> CTRL_ALU3) & 0b1111;
    uint8_t acc = cpu->registers[REG_A];
    uint8_t temp = cpu->registers[REG_A_TEMP];
    uint8_t bus = cpu->dataBus;
    uint8_t carry = (cpu->flags >> FLAG_CARRY) & 0b1;
    logMessage(LOG_LEVEL_DEBUG, "ALU code: %d", aluCode);
    if (aluCode > 0)
    {
        logMessage(LOG_LEVEL_DEBUG, "Acc before ALU operation: %d", acc);
        logMessage(LOG_LEVEL_DEBUG, "Acc temp before ALU operation: %d", temp);
        logMessage(LOG_LEVEL_DEBUG, "Carry before ALU operation: %d", carry);
        logMessage(LOG_LEVEL_DEBUG, "Flags before ALU operation: %d", cpu->flags);
    }
    switch(aluCode)
    {
        case NOP:
            break;
        case ADD:
            bus = acc + temp;
            carry = (unsigned int)acc + (unsigned int)temp > 255;
            break;
        case SUB:
            bus = acc - temp;
            carry = acc < temp;
            break;
        case AND:
            bus = acc & temp;
            break;
        case OR:
            bus = acc | temp;
            break;
        case XOR:
            bus = acc ^ temp;
            break;
        case NOT:
            bus = ~acc;
            break;
        case INC:
            bus = acc + 1;
            carry = acc == 255;
            break;
        case DEC:
            bus = acc - 1;
            carry = acc == 0;
            break;
        case SHR:
            bus = acc >> 1;
            break;
        case SHL:
            bus = acc << 1;
            carry = acc & 0b10000000;
            break;
        case ADDC:
            bus = acc + temp + carry;
            carry = (unsigned int)acc + (unsigned int)temp + (unsigned int)carry > 255;
            break;
        case SUBC:
            bus = acc - temp - carry;
            carry = acc < (temp + carry);
            break;
        case INCC:
            bus = acc + carry;
            carry = (unsigned int)acc + (unsigned int)carry > 255;
            break;
        case DECC:
            bus = acc - carry;
            carry = acc < carry;
            break;
        case UNEG:
            bus = -acc;
            break;
        default:
            logMessage(LOG_LEVEL_ERROR, "ALU switch hit default");
            break;
    }
    if (aluCode > 0) {
        cpu->dataBus = bus;
        cpu->flags = (cpu->flags & ~(1 << FLAG_CARRY)) | (carry << FLAG_CARRY);
        logMessage(LOG_LEVEL_DEBUG, "Acc temp after ALU operation: %d", temp);
        logMessage(LOG_LEVEL_DEBUG, "Bus after ALU operation: %d", bus);
        logMessage(LOG_LEVEL_DEBUG, "Carry after ALU operation: %d", carry);
        logMessage(LOG_LEVEL_DEBUG, "Flags after ALU operation: %d", cpu->flags);
    }
}

void tock(CPUState *cpu)
{
    // Update relevant registers
    uint8_t registerInCode = (cpu->controlBus >> CTRL_IN3) & 0b1111;
    logMessage(LOG_LEVEL_DEBUG, "Register in code: %d", registerInCode);
    if (registerInCode > 0)
    {
        cpu->registers[registerInCode] = cpu->dataBus;
        logMessage(LOG_LEVEL_DEBUG, "Register in new register value: %d", cpu->registers[registerInCode]);
    }

    // Set flags if accumulator updated
    if (registerInCode == REG_A)
    {
        uint8_t sign = cpu->registers[REG_A] > 127;
        uint8_t zero = cpu->registers[REG_A] == 0;
        cpu->flags = (cpu->flags & ~((1 << FLAG_SIGN) | (1 << FLAG_ZERO)))
            | (sign << FLAG_SIGN)
            | (zero << FLAG_ZERO);
        logMessage(LOG_LEVEL_DEBUG, "Acc in new flags value: %d", cpu->flags);
    }

    // Handle direct register move
    if ((cpu->controlBus >> CTRL_MOVE_ADDRESS_COUNTER) & 0b1)
    {
        logMessage(LOG_LEVEL_DEBUG, "Move address counter");
        cpu->registers[REG_ADDRESS_H] = cpu->registers[REG_COUNTER_H];
        cpu->registers[REG_ADDRESS_L] = cpu->registers[REG_COUNTER_L];
    }
    if ((cpu->controlBus >> CTRL_MOVE_ADDRESS_STACK) & 0b1)
    {
        logMessage(LOG_LEVEL_DEBUG, "Move address stack");
        cpu->registers[REG_ADDRESS_H] = cpu->registers[REG_STACK_H];
        cpu->registers[REG_ADDRESS_L] = cpu->registers[REG_STACK_L];
    }
    if ((cpu->controlBus >> CTRL_MOVE_ADDRESS_HL) & 0b1)
    {
        logMessage(LOG_LEVEL_DEBUG, "Move address HL");
        cpu->registers[REG_ADDRESS_H] = cpu->registers[REG_H];
        cpu->registers[REG_ADDRESS_L] = cpu->registers[REG_L];
    }

    // Handle RAM in
    if ((cpu->controlBus >> CTRL_RAM_IN) & 0b1)
    {
        uint16_t ramAddress = 
            (cpu->registers[REG_ADDRESS_H] << 8) |
            (cpu->registers[REG_ADDRESS_L]);
        logMessage(LOG_LEVEL_DEBUG, "RAM in address: 0x%x", ramAddress);
        cpu->ram[ramAddress] = cpu->dataBus;
        logMessage(LOG_LEVEL_DEBUG, "RAM in new RAM value: %d", cpu->ram[ramAddress] = cpu->dataBus);
    }

    // Handle status in
    if ((cpu->controlBus >> CTRL_FLAG_IN) & 0b1) {
        cpu->flags = cpu->dataBus;
        logMessage(LOG_LEVEL_DEBUG, "Flags in new flags value: %d", cpu->flags);
    }

    // Reset microtick
    if ((cpu->controlBus >> CTRL_RESET_MICRO_TICK) & 0b1)
    {
        cpu->microinstructionCounter = 0;
        logMessage(LOG_LEVEL_DEBUG, "Reset microtick");
    }

    // Output to STDOUT
    if ((cpu->controlBus >> CTRL_OUT) & 0b1)
    {
        logMessage(LOG_LEVEL_INFO, "OUTPUT: %d", cpu->dataBus);
    }
}

// Arguments are filenames for command ROM and program ROM
int main(int argc, char **argv)
{
    // Handle arguments
    fprintf(stderr, "Loading arguments\n");
    if (argc < 3 || argc > 4)
    {
        fprintf(stderr, "Expected 2 or 3 arguments");
        return 1;
    }
    char *command_filename = argv[1];
    char *program_filename = argv[2];
    char *logLevelName = "info";
    if (argc == 4)
    {
        logLevelName = argv[3];
    }
    if (strcmp(logLevelName, "debug") == 0)
    {
        logLevel = LOG_LEVEL_DEBUG;
    }
    else if (strcmp(logLevelName, "info") == 0)
    {
        logLevel = LOG_LEVEL_INFO;
    }
    else if (strcmp(logLevelName, "error") == 0)
    {
        logLevel = LOG_LEVEL_ERROR;
    }
    else
    {
        fprintf(stderr, "Invalid log level");
        return 1;
    }

    logMessage(LOG_LEVEL_INFO, "Loaded arguments");

    // Instantiate CPU
    CPUState cpu = {0};
    cpu.ram = (uint8_t *)malloc(sizeof(uint8_t) * PROGRAM_ROM_BYTES);
    cpu.controlROM = (uint32_t *)malloc(sizeof(uint32_t) * COMMAND_ROM_BYTES);

    // Initialisation:

    // 1. Reset CPU state
    cpu.registers[REG_COUNTER_H] = 128;
    cpu.registers[REG_STACK_H] = 8;

    // 2. Load control ROM
    logMessage(LOG_LEVEL_INFO, "Loading control ROM");

    // Open file
    FILE *command_file = fopen(command_filename, "rb");
    if (!command_file)
    {
        logMessage(LOG_LEVEL_ERROR, "Failed to open command ROM file");
        goto ROM_LOAD_ERROR;
    }

    // Read ROM into buffer
    size_t commandBytesRead = fread(cpu.controlROM, sizeof(uint32_t), COMMAND_ROM_BYTES, command_file);
    if (commandBytesRead != COMMAND_ROM_BYTES)
    {
        logMessage(LOG_LEVEL_ERROR, "Command ROM file read error");
        fclose(command_file);
        goto ROM_LOAD_ERROR;
    }

    logMessage(LOG_LEVEL_INFO, "Loaded control ROM");

    // 3. Load program ROM into memory
    logMessage(LOG_LEVEL_INFO, "Loading program ROM");

    // Open file
    FILE *program_file = fopen(program_filename, "rb");
    if (!program_file)
    {
        logMessage(LOG_LEVEL_ERROR, "Failed to open program ROM file");
        goto ROM_LOAD_ERROR;
    }

    // Read ROM into buffer
    size_t programBytesRead = fread(cpu.ram, sizeof(uint8_t), PROGRAM_ROM_BYTES, program_file);
    if (programBytesRead != PROGRAM_ROM_BYTES)
    {
        logMessage(LOG_LEVEL_ERROR, "Program ROM file read error");
        fclose(program_file);
        goto ROM_LOAD_ERROR;
    }

    logMessage(LOG_LEVEL_INFO, "Loaded program ROM");

    // Execute until halt
    logMessage(LOG_LEVEL_INFO, "Initialisation complete. Starting execution:");
    executionStage = EXEC_STAGE_RUN;
    while (!((cpu.controlBus >> CTRL_HALT) & 0b1))
    {
        tick(&cpu);
        tock(&cpu);
    }
    executionStage = EXEC_STAGE_HALT;
    logMessage(LOG_LEVEL_INFO, "Program halted.");

    free(cpu.ram);
    free(cpu.controlROM);

    return 0;

ROM_LOAD_ERROR:
    free(cpu.ram);
    free(cpu.controlROM);
    return 1;
}

