#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define INSTRUCTION_ROM_BYTES 65536
#define PROGRAM_ROM_BYTES 65536
#define NUM_REGISTERS 15

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
    CTRL_FLAG_OUT1, CTRL_FLAG_OUT0, CTRL_RAM_IN, CTRL_RAM_OUT,

    // Control signals
    CTRL_RESET_MICRO_TICK, CTRL_OUT, CTRL_HALT
} Control;

typedef enum
{
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

typedef struct
{
    uint8_t     dataBus;
    uint32_t    controlBus;
    uint8_t     registers[NUM_REGISTERS];
    uint8_t     flags;                      // only three flag bits used
    uint8_t     microinstructionCounter;    // only four counter bits used
    uint8_t     *ram;                       // dynamically-allocated
    uint32_t    *controlROM;                // dynamically-allocated
} CPUState;

// During the 'tick':
// 1. The current instruction is decoded
// 2. Relevant register/RAM data is put onto bus
// 3. ALU calculations are evaluated
void tick(CPUState *cpu)
{
    // 16-bit instruction address
    uint16_t instructionAddress = 
        (cpu->flags << 12) | 
        (cpu->registers[REG_INSTRUCTION] << 4) |
        (cpu->microinstructionCounter++);

    // Set control bus according to control ROM
    cpu->controlBus = cpu->controlROM[instructionAddress];

    // Calculate and set register output state
    // Because controlBus bits are stored [..., out3, out2, out1, out0, ...]
    uint8_t registerOutCode = (cpu->controlBus >> CTRL_OUT3) & 0b1111;
    if (registerOutCode < NUM_REGISTERS)
    {
        cpu->dataBus = cpu->registers[registerOutCode];
    }

    // Calculate and set flag output state
    uint8_t flagOutCode = (cpu->controlBus >> CTRL_FLAG_OUT1) & 0b11;
    switch(flagOutCode)
    {
        case 0: // zero flag
            cpu->dataBus = (cpu->flags >> FLAG_ZERO) & 0b1;
            break;
        case 1: // sign flag
            cpu->dataBus = (cpu->flags >> FLAG_SIGN) & 0b1;
            break;
        case 2: // all flags (status)
            cpu->dataBus = cpu->flags;
            break;
        case 3: // no flags
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
        cpu->dataBus = cpu->ram[ramAddress];
    }

    // Calculate and set ALU state
    uint8_t aluCode = (cpu->controlBus >> CTRL_ALU3) & 0b1111;
    uint8_t acc = cpu->registers[REG_A];
    uint8_t temp = cpu->registers[REG_A_TEMP];
    uint8_t bus = cpu->dataBus;
    uint8_t carry = (cpu->flags >> FLAG_CARRY) & 0b1;
    switch(aluCode)
    {
        case 0: // no action taken
            break;
        case 1: // add
            bus = acc + temp;
            carry = acc + temp > 255;
            break;
        case 2: // subtract
            bus = acc - temp;
            carry = acc - temp < 0;
            break;
        // And
        case 3:
            bus = acc & temp;
            break;
        // Or
        case 4:
            bus = acc | temp;
            break;
        // Xor
        case 5:
            bus = acc ^ temp;
            break;
        // Not
        case 6:
            bus = !acc;
            break;
        // Increment
        case 7:
            bus = acc + 1;
            carry = acc == 255;
            break;
        // Decrement
        case 8:
            bus = acc - 1;
            carry = acc == 0;
            break;
        // Add (carry conditional)
        case 9:
            bus = acc + temp + carry;
            carry = acc + temp + carry > 255;
            break;
        // Subtract (carry conditional)
        case 10:
            bus = acc - temp - carry;
            carry = acc - temp - carry < 0;
            break;
        // Increment (carry conditional)
        case 11:
            bus = acc + carry;
            carry = acc + carry > 255;
            break;
        // Decrement (carry conditional)
        case 12:
            bus = acc - carry;
            carry = acc - carry < 0;
            break;
        // Unary negate
        case 13:
            bus = -acc;
            break;
        default:
            perror("ALU switch hit default");
            break;
    }
    cpu->dataBus = bus;
    cpu->flags |= (carry << FLAG_CARRY);
}

void tock(CPUState *cpu)
{

}

int main()
{
    CPUState cpu;

    cpu.ram = (uint8_t *)malloc(sizeof(uint8_t) * PROGRAM_ROM_BYTES);
    cpu.controlROM = (uint32_t *)malloc(sizeof(uint32_t) * INSTRUCTION_ROM_BYTES);

    // Initialisation:

    // 1. Reset CPU state
    cpu.registers[REG_H] = 128;
    cpu.registers[REG_STACK_H] = 8;

    // 2. Load instruction ROM

    // Open file
    FILE *instruction_rom_file = fopen("instruction_rom.bin", "rb");
    if (!instruction_rom_file)
    {
        perror("Failed to open instruction_rom.bin");
        return 1;
    }

    // Read ROM into buffer
    size_t instructionBytesRead = fread(cpu.controlROM, sizeof(uint32_t), INSTRUCTION_ROM_BYTES, instruction_rom_file);
    if (instructionBytesRead != INSTRUCTION_ROM_BYTES)
    {
        perror("instruction_rom.bin file read error");
        fclose(instruction_rom_file);
        return 1;
    }

    // 3. Load program file into memory

    // Open file
    FILE *program_rom_file = fopen("program_rom.bin", "rb");
    if (!program_rom_file)
    {
        perror("Failed to open program_rom.bin");
        return 1;
    }

    // Read ROM into buffer
    size_t programBytesRead = fread(cpu.ram, sizeof(uint8_t), PROGRAM_ROM_BYTES, program_rom_file);
    if (programBytesRead != PROGRAM_ROM_BYTES)
    {
        perror("program_rom.bin file read error");
        fclose(program_rom_file);
        return 1;
    }

    // Execute until halt
    while (!(cpu.controlBus >> CTRL_HALT))
    {
        tick(&cpu);
        tock(&cpu);
    }

    free(cpu.ram);
    free(cpu.controlROM);

    return 0;
}

