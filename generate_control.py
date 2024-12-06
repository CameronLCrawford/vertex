import sys
import logging

def generate_control(rom_filename):
    # Control bits
    (I0, I1, I2, I3,        # Register input
     O0, O1, O2, O3,        # Register output
     A0, A1, A2, A3,        # Accumulator
     CNI, ADI, STI, STD,    # Counter signals
     MAC, MAS, MAH,         # Direct moves
     F1, F0, FI,            # Flags
     RI, RO,                # Memory
     RST, OUT, HLT          # Control and output
    ) = (2**i for i in range(27))

    # Register in codes
    AI  =   I0
    ATI =   I1
    HI  =   I1 | I0
    LI  =   I2
    CHI =   I2 | I0
    CLI =   I2 | I1
    AHI =   I2 | I1 | I0
    ALI =   I3
    BHI =   I3 | I0
    BLI =   I3 | I1
    SHI =   I3 | I1 | I0
    SLI =   I3 | I2
    OHI =   I3 | I2 | I0
    OLI =   I3 | I2 | I1
    II  =   I3 | I2 | I1 | I0

    # Register out codes
    AO  =   O0
    ATO =   O1
    HO  =   O1 | O0
    LO  =   O2
    CHO =   O2 | O0
    CLO =   O2 | O1
    AHO =   O2 | O1 | O0
    ALO =   O3
    BHO =   O3 | O0
    BLO =   O3 | O1
    SHO =   O3 | O1 | O0
    SLO =   O3 | O2
    OHO =   O3 | O2 | O0
    OLO =   O3 | O2 | O1
    IO  =   O3 | O2 | O1 | O0

    # ALU codes
    ADD     = A0
    SUB     = A1
    AND     = A1 | A0
    OR      = A2
    XOR     = A2 | A0
    NOT     = A2 | A1
    INC     = A2 | A1 | A0
    DEC     = A3
    SHR     = A3 | A0
    SHL     = A3 | A1
    ADDC    = A3 | A1 | A0
    SUBC    = A3 | A2
    INCC    = A3 | A2 | A0
    DECC    = A3 | A2 | A1
    UNEG    = A3 | A2 | A1 | A0

    # Instructions
    # Each instruction is a list of control bit states.
    # Consider the contrived example in binary: [00, 11, 10].
    # This would define an instruction that is three microticks long
    # and would set the control bits to 00, 11, and 10, in turn.
    # To avoid writing binary, the variables defined above are used
    # to define instructions.
    # Consider the example of the ADDA instruction, which adds the
    # accumulator to itself:
    # ADDA := [AO | ATI, ADD | AI].
    # Read as "1. A out, A Temp in; 2. Add, A in".
    # By taking the binary disjunction of control bits in each microtick,
    # complex control operations can be composed.
    # The `instructions` object is a list of all instructions
    instructions = [
        [AO | ATI, ADD | AI], # ADDA -- add value in A to A
        [A0 | ATI, SHL | AI], # SHLA -- shift A left
        [CNI | ADI | RO | AI], # LDA -- load A with 8-bit immediate
        [CNI | ADI | RO | ATI, CNI | ADI | RO | CLI, ATO | CHI], # JMPI -- jump to 16-bit immediate
        [AO | OUT], # OUT -- output value in accumulator
        [HLT]
    ]

    # Augment instructions with prefix and suffix
    augmented_instructions = []
    for i, instruction in enumerate(instructions):
        prefix = [MAC, RO | II]
        suffix = []
        if i == 3: # Don't increment counter on jump
            suffix += [RST]
        else:
            suffix += [RST | CNI]
        augmented_instruction = prefix + instruction + suffix
        augmented_instructions.append(augmented_instruction)

    # Generate ROM
    # The control ROM is addressed using the following composition of bits:
    # CF|SF|ZF|I7|I6|I5|I4|I3|I2|I1|I0|M3|M2|M1|M0
    # 14 13 12 11 10 09 08 07 06 05 04 03 02 01 00
    # The first 3 are flag bits (carry, sign, zero).
    # The next 8 are the current instruction index.
    # The final 4 are the microinstruction index.
    # Most instructions aren't influenced by the current flag states.
    # These instructions are duplicated 2**3=8 (3 flags) times across the ROM.
    # Some instructions depend on specific flag states.
    # These instructions are only duplicated where these conditions are met.
    rom = [0] * 65536
    for flag_state in range(8):
        for i, instruction in enumerate(augmented_instructions):
            for j, microinstruction in enumerate(instruction):
                address = (flag_state << 12) | (i << 4) | j
                rom[address] = microinstruction

    # Write out ROM
    rom_bytes = []
    for value in rom:
        value = bin(value)[2:].zfill(32)
        rom_bytes.append(int(value[24:32], 2))
        rom_bytes.append(int(value[16:24], 2))
        rom_bytes.append(int(value[8:16], 2))
        rom_bytes.append(int(value[:8], 2))
    with open(rom_filename, 'wb') as rom_file:
        rom_file.write(bytearray(rom_bytes))
    logging.info('Finished writing to ROM')

if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) != 2:
        logging.error('Expected 1 argument')
    else:
        generate_control(arguments[1])

