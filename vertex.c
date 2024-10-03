#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define INSTRUCTION_ROM_BYTES 65536
#define PROGRAM_ROM_BYTES 65536

enum Controls
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
};

enum Registers
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

    // Special register
    REG_INSTRUCTION
};

enum Flags
{
    FLAG_SIGN,
    FLAG_CARRY,
    FLAG_ZERO
};

void tick()
{

}

void tock()
{

}

int main()
{
    // Buses
    uint8_t dataBus;
    uint32_t controlBus;

    // Registers and flags
    // NOTE: Only three flag bits are used
    uint8_t registers[15];
    uint8_t flags;

    // Microinstruction counter
    // NOTE: Only four counter bits are used
    uint8_t microinstructionCounter;

    // All addressable memory
    uint8_t *ram = (uint8_t *)malloc(sizeof(uint8_t) * PROGRAM_ROM_BYTES);

    // Control ROM
    uint32_t *controlROM = (uint32_t *)malloc(sizeof(uint32_t) * INSTRUCTION_ROM_BYTES);

    // Initialisation:

    // 1. Reset CPU state
    registers[REG_H] = 128;
    registers[REG_STACK_H] = 8;

    // 2. Load instruction ROM
    
    // Open file
    FILE *instruction_rom_file = fopen("instruction_rom.bin", "rb");
    if (!instruction_rom_file)
    {
        perror("Failed to open instruction_rom.bin");
        return 1;
    }

    // Read ROM into buffer
    size_t instructionBytesRead = fread(controlROM, sizeof(uint32_t), INSTRUCTION_ROM_BYTES, instruction_rom_file);
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
    size_t programBytesRead = fread(ram, sizeof(uint8_t), PROGRAM_ROM_BYTES, program_rom_file);
    if (programBytesRead != PROGRAM_ROM_BYTES)
    {
        perror("program_rom.bin file read error");
        fclose(program_rom_file);
        return 1;
    }

    return 0;
}

