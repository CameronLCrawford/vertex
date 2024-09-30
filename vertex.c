#include <stdint.h>

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

enum FlagNames
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
	uint8_t ram[65536];
	
	// Control ROM
	uint32_t controlROM[65536];

	// Initialisation:
	// 1. Reset CPU state
	// 2. Load instruction ROM
	// 3. Load program file into memory

	return 0;
}


