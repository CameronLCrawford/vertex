# Overview
`vertex` is a virtual machine that simulates an 8-bit CPU with 15 registers and the ability to address 64k of memory by utilising pairs of 8-bit registers.
This specification details the design of these components: 
- Instructions
- Registers 
- Flags
- I/O
- Arithmetic operations
- Program execution

# Instructions
The control ROM is made up of 2^16 32-bit words.
This ROM defines, at each address, the state of the control bus.
Each bit of the control bus controls a single pin of a component of the CPU eg. `AIN` would control whether or not the `A` register reads in and stores data from the bus on the next tick.
Note that some sets of instructions can be multiplexed eg. all 'register in' instructions because only a single register can be active during each tick.
The structure of an instruction word is as follows:

| Bit (0 LSB) | Abbreviation | Description |
| ----------- | ------------ | ----------- |
| 0-3 | in3, in2, in1, in0 | 4 bits represent 16 register input states |
| 4-7 | out3, out2, out1, out0 | 4 bits represent 16 register output states |
| 8-11 | alu3, alu2, alu1, alu0 | 4 bits represent 16 ALU states |
| 12 | counterInc | Increments program counter |
| 13 | addressInc | Increments address pointer |
| 14 | stackInc | Increments stack pointer |
| 15 | stackDex | Decrements stack pointer |
| 16 | moveAddressCounter | Stores program counter in address pointer |
| 17 | moveAddressStack | Stores stack pointer in address pointer |
| 18 | moveAddressHL | Stores HL registers in address pointer |
| 19 | zeroFlagOut | Value of zero flag onto databus |
| 20 | signFlagOut | Value of sign flag onto databus |
| 21 | ramIn | Memory at address stored in address pointer onto databus |
| 22 | ramOut | Data on bus stored at memory address in address pointer |
| 23 | resetMicroTick | Internal microtick counter is reset to 0 |
| 24 | out | Data on bus is outputted to terminal |
| 25 | halt | Program halts and execution stops |

The input address to the control bus is a combination of the flag status, the instruction opcode in the instruction register, and the microinstruction count.
This is constructed in the following way:

| Bit (0 LSB) | Description |
| ----------- | ----------- |
| 0-3 | Microinstruction counter value (0-15) |
| 4-11 | Instruction register value -- allows 256 instructions |
| 12-14 | Flag bits (sign, carry, zero) |
| 15 | Not used |

 Each machine code instruction is made up of several (up to 16) smaller microinstructions. 
 An example of a set of microinstructions that could represent an add instruction would be `{BOut | ATempIn, Add | AIn}`. 
 The binary or ("|") is used when two or more control bits are high as a part of single microinstruction. 
The first microinstruction dictates that the `B` register is putting its contents onto the bus and the `A temp` register is reading from the bus ie. the value in `B` is stored in `A temp`. 
 The second microinstruction causes the output of the simulated full-adder circuitry to be placed onto the bus and read into the `A` register.

# Registers
The 15 registers are all 8 bits wide.
They are all connected to an 8-bit-wide bus. 
The registers and their functions are detailed in this table:

| Register | Function |
| -------- | -------- |
| A | Accumulator main register. Can be read from |
| A Temporary | Accumulator temporary register. Cannot be read from |
| H | Upper half of 16-bit HL pair |
| L | Low half of 16-bit HL pair |
| Counter High | Upper half of 16-bit program counter |
| Counter Low | Lower half of 16-bit program counter |
| Address High | Upper half of 16-bit address pointer |
| Address Low | Lower half of 16-bit address pointer |
| Base High | Upper half of 16-bit base pointer |
| Base Low | Lower half of 16-bit base pointer |
| Stack High | Upper half of 16-bit stack pointer |
| Stack Low | Lower half of 16-bit stack pointer |
| Object High | Upper half of 16-bit object pointer |
| Object Low | Lower half of 16-bit object pointer |
| Instruction | Stores current instruction |

As is obvious from the table, there are multiple 8-bit registers that form one half of a larger 16-bit word. 
These 16-bit virtual registers and their functions are explained here:

| 16-bit Register | Function |
| --------------- | -------- |
| HL | General use 16-bit register which can be used in arithmetic operations. In general the programmer interacts with the registers, A, A Temp, H, and L |
| Counter | Program counter stores memory address of current instruction being executed. Can be incremented or have a new value loaded in to jump between sections of the program |
| Address Pointer | Stores the memory address in RAM that the CPU is interacting with (whether that be reading from or writing to). This is loaded with an address then an operation will either read in or write to the data at that address |
| Base Pointer | Stores the memory address of the base of the current stack frame |
| Stack Pointer | Stores the memory address of the top of the current stack frame |
| Object Pointer | Stores the memory address of the object that is currently being interacted with |

# Flags
The 3 system flags are:
- `sign` 
    - The value in the accumulator is positive or negative, as indicated by the sign bit
- `carry` 
    - The previous arithmetic operation resulted in a bit being carried whether by an addition overflow or a subtraction underflow
- `zero`
    - The value in the accumulator is 0
The carry flag is only set when a valid arithmetic operation occurs as it is the direct result of the operation; the other 2 flags are only set when data is moved into the accumulator and are solely based off the data present in the accumulator.
The CPU does not support interrupts currently.
The flags register can be put on the bus and this is used in the creation of a new stack frame to save the system state. 
It can also be read in from the bus to load the previous system state upon destruction of a stack frame.

# I/O
Output can be achieved by setting the `out` control bit high which will print the value of the bus to the terminal.

# Arithmetic operations
The CPU has an 8-bit ALU which is controlled through 4 control bits. 
It supports basic arithmetic and binary logic operations. 
The arithmetic operations come in two flavours: unconditional and carry conditional. 
The carry conditional operations will have a different output based on the status of the carry flag and this is implemented as it allows for arithmetic operations on larger than 8-bit numbers to be performed.
The ALU also supports a unary negate operation for negating the value in the accumulator. 
There are two registers that feed into the ALU: the `A` register and the `A Temp` register. All arithmetic operations do not affect the accumulator itself but instead output the result of the operation to the bus.
The operations supported by the ALU are as follows:

| Control Value | Operation |
| ------------- | --------- |
| 0 | No action taken |
| 1 | Add |
| 2 | Subtract |
| 3 | Binary AND |
| 4 | Binary OR |
| 5 | Binary XOR |
| 6 | Binary NOT |
| 7 | Increment |
| 8 | Decrement |
| 9 | Add (carry conditional) |
| 10 | Subtract (carry conditional) |
| 11 | Increment (carry conditional) |
| 12 | Decrement (carry conditional) |
| 13 | Unary negate |

