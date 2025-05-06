#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <sys/fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

#define CONTROL_ROM_BYTES 65536
#define RAM_SIZE 65536
#define MAX_PERIPHERAL_COUNT 8
#define INTCAL 1 // Interrupt call instruction
#define RAM_SHM_FILENAME "/tmp/vtx_ram_shm"
#define INTERRUPT_SHM_FILENAME "/tmp/vtx_interrupt_shm"

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
    CTRL_MOVE_ADDRESS_COUNTER, CTRL_MOVE_ADDRESS_STACK, CTRL_MOVE_ADDRESS_HL, CTRL_MOVE_COUNTER_INTERRUPT,

    // Flags and addressing
    CTRL_FLAG_OUT1, CTRL_FLAG_OUT0, CTRL_FLAG_IN,

    // Memory
    CTRL_RAM_IN, CTRL_RAM_OUT,

    // Control signals
    CTRL_RESET_MICRO_TICK, CTRL_INTERRUPT_ENABLE, CTRL_OUT, CTRL_HALT
} Control;

typedef enum
{
    // No-reg
    REG_NO,

    // Accumulator registers
    REG_A, REG_A_TEMP,

    // General-purpose registers
    REG_B, REG_C,

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
    ADDC, SUBC, INCC, DECC, SHRC
} AluOp;

typedef struct
{
    uint8_t     enabled;
    uint16_t    handlerAddress;
    uint8_t     raises[MAX_PERIPHERAL_COUNT];
} InterruptState;

typedef struct
{
    uint8_t                 dataBus;
    uint32_t                controlBus;
    uint8_t                 registers[16];
    uint8_t                 flags;                      // only three flag bits used
    uint8_t                 microinstructionCounter;    // only four counter bits used
    volatile uint8_t        *ram;
    uint32_t                *controlROM;
    volatile InterruptState *interruptState;
    uint8_t                 raisedPeripheral;
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
            if (++cpu->registers[REG_COUNTER_H] == 0)
            {
                logMessage(LOG_LEVEL_ERROR, "Counter overflow");
            };
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

    // Check for interrupt enable
    if ((cpu->controlBus >> CTRL_INTERRUPT_ENABLE) & 0b1)
    {
        cpu->interruptState->enabled = 1;
    }

    // Acknowledge peripheral raises
    if (cpu->interruptState->enabled)
    {
        for (int peripheral = 0; peripheral < MAX_PERIPHERAL_COUNT; peripheral++)
        {
            if (cpu->interruptState->raises[peripheral])
            {
                logMessage(LOG_LEVEL_DEBUG, "Peripheral %d has been acknowledged", peripheral);
                cpu->interruptState->raises[peripheral] = 0;
                cpu->interruptState->enabled = 0;
                cpu->raisedPeripheral = peripheral;
                break;
            }
        }
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
            carry = acc & 0b1;
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
        case SHRC:
            bus = (acc >> 1) | ((uint8_t)carry << 7);
            carry = acc & 0b1;
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
    if ((cpu->controlBus >> CTRL_MOVE_COUNTER_INTERRUPT) & 0b1)
    {
        logMessage(LOG_LEVEL_DEBUG, "Move counter interrupt");
        cpu->registers[REG_COUNTER_H] = cpu->interruptState->handlerAddress >> 8;
        cpu->registers[REG_COUNTER_L] = cpu->interruptState->handlerAddress;
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
    if ((cpu->controlBus >> CTRL_FLAG_IN) & 0b1)
    {
        cpu->flags = cpu->dataBus;
        logMessage(LOG_LEVEL_DEBUG, "Flags in new flags value: %d", cpu->flags);
    }

    // Reset microtick
    if ((cpu->controlBus >> CTRL_RESET_MICRO_TICK) & 0b1)
    {
        cpu->microinstructionCounter = 0;
        logMessage(LOG_LEVEL_DEBUG, "Reset microtick");

        // Handle interrupts on beginning of new instruction
        if (cpu->raisedPeripheral < MAX_PERIPHERAL_COUNT)
        {
            if (cpu->interruptState->raises[cpu->raisedPeripheral])
            {
                logMessage(LOG_LEVEL_DEBUG, "Interrupt raised by peripheral %d", cpu->raisedPeripheral);
                cpu->registers[REG_INSTRUCTION] = INTCAL;
                cpu->interruptState->raises[cpu->raisedPeripheral] = 0;
                cpu->raisedPeripheral = MAX_PERIPHERAL_COUNT;
            }
        }
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
    cpu.raisedPeripheral = MAX_PERIPHERAL_COUNT; // This means there's no raised peripheral

    // Connect to mmap RAM
    int ram_shm_fd = open(RAM_SHM_FILENAME, O_RDWR | O_CREAT, 0666);
    if (ram_shm_fd < 0)
    {
        logMessage(LOG_LEVEL_ERROR, "Unable to open RAM shared memory file");
        return 1;
    }
    if (ftruncate(ram_shm_fd, RAM_SIZE) < 0)
    {
        logMessage(LOG_LEVEL_ERROR, "Shared memory file different size to program ROM");
        close(ram_shm_fd);
        return 1;
    }
    cpu.ram = mmap(NULL, RAM_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, ram_shm_fd, 0);
    if (cpu.ram == MAP_FAILED)
    {
        logMessage(LOG_LEVEL_ERROR, "RAM memory map failed");
        close(ram_shm_fd);
        return 1;
    }
    close(ram_shm_fd);

    // Connect to mmap interrupt array
    int interrupt_shm_fd = open(INTERRUPT_SHM_FILENAME, O_RDWR | O_CREAT, 0666);
    if (interrupt_shm_fd < 0)
    {
        logMessage(LOG_LEVEL_ERROR, "Unable to open interrupt shared memory file");
        return 1;
    }
    if (ftruncate(interrupt_shm_fd, sizeof(InterruptState)) < 0)
    {
        logMessage(LOG_LEVEL_ERROR, "Shared memory file different size to interrupt state size");
        close(interrupt_shm_fd);
        return 1;
    }
    cpu.interruptState = mmap(NULL, sizeof(InterruptState), PROT_READ | PROT_WRITE, MAP_SHARED, interrupt_shm_fd, 0);
    if (cpu.interruptState == MAP_FAILED)
    {
        logMessage(LOG_LEVEL_ERROR, "Interrupt state memory map failed");
        close(interrupt_shm_fd);
        return 1;
    }
    cpu.interruptState->enabled = 1;

    cpu.controlROM = (uint32_t *)malloc(sizeof(uint32_t) * CONTROL_ROM_BYTES);
    if (!cpu.controlROM)
    {
        logMessage(LOG_LEVEL_ERROR, "Unable to allocate control ROM");
        munmap((void *)cpu.ram, RAM_SIZE);
        return 1;
    }

    // Initialisation:

    // Load control ROM
    logMessage(LOG_LEVEL_INFO, "Loading control ROM");

    // Open file
    FILE *command_file = fopen(command_filename, "rb");
    if (!command_file)
    {
        logMessage(LOG_LEVEL_ERROR, "Failed to open command ROM file");
        goto ROM_LOAD_ERROR;
    }

    // Read ROM into buffer
    size_t controlBytesRead = fread(cpu.controlROM, sizeof(uint32_t), CONTROL_ROM_BYTES, command_file);
    if (controlBytesRead != CONTROL_ROM_BYTES)
    {
        logMessage(LOG_LEVEL_ERROR, "Command ROM file read error");
        fclose(command_file);
        goto ROM_LOAD_ERROR;
    }

    logMessage(LOG_LEVEL_INFO, "Loaded control ROM");

    // Load program ROM into memory
    logMessage(LOG_LEVEL_INFO, "Loading program ROM");

    // Open file
    FILE *program_file = fopen(program_filename, "rb");
    if (!program_file)
    {
        logMessage(LOG_LEVEL_ERROR, "Failed to open program ROM file");
        goto ROM_LOAD_ERROR;
    }

    // Read ROM into buffer
    fseek(program_file, 0, SEEK_END);
    size_t programSize = ftell(program_file);
    fseek(program_file, 0, SEEK_SET);
    size_t programBytesRead = fread((uint8_t *)cpu.ram + RAM_SIZE - programSize, sizeof(uint8_t), programSize, program_file);
    if (programBytesRead != programSize)
    {
        logMessage(LOG_LEVEL_ERROR, "Program ROM file read error");
        fclose(program_file);
        goto ROM_LOAD_ERROR;
    }

    logMessage(LOG_LEVEL_INFO, "Loaded program ROM");

    // Set initial CPU state
    uint16_t programStartAddress = RAM_SIZE - programSize;
    uint16_t initialStackPointer = programStartAddress - 1;
    cpu.registers[REG_COUNTER_L] = programStartAddress & 0b11111111;
    cpu.registers[REG_COUNTER_H] = programStartAddress >> 8;
    cpu.registers[REG_STACK_L] = initialStackPointer & 0b11111111;
    cpu.registers[REG_STACK_H] = initialStackPointer >> 8;

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

    munmap((void *)cpu.ram, RAM_SIZE);
    munmap((void *)cpu.interruptState, sizeof(InterruptState));
    free(cpu.controlROM);

    return 0;

ROM_LOAD_ERROR:
    munmap((void *)cpu.ram, RAM_SIZE);
    munmap((void *)cpu.interruptState, sizeof(InterruptState));
    free(cpu.controlROM);
    return 1;
}

