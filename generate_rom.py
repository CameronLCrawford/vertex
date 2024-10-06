import sys
import logging

def generate(rom_filename):
    # Control bits
    (I3, I2, I1, I0, # Register input
     O3, O2, O1, O0, # Register output
     A3, A2, A1, A0, # Accumulator
     CI, AI, SI, SD, # Counter signals
     MC, MS, MH,     # Direct moves
     F1, F0, RI, RO, # Flags and addressing
     RS, OT, HT      # Control and output
    ) = (2**i for i in range(26))

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
    ADDC    = A3 | A0
    SUBC    = A3 | A1
    INCC    = A3 | A1 | A0
    DECC    = A3 | A2
    UNEG    = A3 | A2 | A0

    # Instructions
    # Each instruction is a list of control bit states.
    # Consider the contrived example in binary: [00, 11, 10].
    # This would define an instruction that is three microticks long
    # and would set the control bits to 00, 11, and 10, in turn.
    # To avoid writing binary, the variables defined above are used
    # to define instructions.
    # Consider the example of the ADDA instruction, which adds the
    # accumulator to itself:
    # ADDA := [A0 | ATI, ADD | AI].
    # Read as "1. A out, A Temp in; 2. Add, A in".
    # By taking the binary disjunction of control bits in each microtick,
    # complex control operations can be composed.
    # The `instructions` object is a list of all instructions
    instructions = [

    ]

    # Write out ROM
    rom_bytes = []
    with open(rom_filename, 'wb') as rom_file:
        rom_file.write(bytearray(rom_bytes))
    logging.info('Finished writing to ROM')

if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) != 2:
        logging.error('Expected 1 argument')
    else:
        generate(arguments[1])

