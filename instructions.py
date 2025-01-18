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
jump_immediate = [MAC, RO | II, CNI | ADI | RO | ATI, CNI | ADI | RO | CLI, ATO | CHI, RST]
invalid_conditional_jump = [MAC, RO | II, CNI, CNI, RST | CNI]
Instruction = tuple[
    str,            # Name
    str,            # Description
    list[int],      # Microinstructions
    list[int],      # Scopes
]
instructions: list[Instruction] = [
    ### ALU ###
    # ADD
    (
        "ADDA",
        "Add A to A",
        [MAC, RO | II, AO | ATI, ADD | AI, RST | CNI],
        [0, 0, 0],
    ),

    # SUB

    # SHIFT
    (
        "SHL",
        "Shift A left",
        [MAC, RO | II, A0 | ATI, SHL | AI, RST | CNI],
        [0, 0, 0],
    ),

    ### DATA ###
    (
        "MOVAI",
        "Move into A 8-bit immediate",
        [MAC, RO | II, CNI | ADI | RO | AI, RST | CNI],
        [0, 0, 0],
    ),

    ### JUMP ###
    # CONDITIONAL
    (
        "JZI",
        "Jump if zero to 16-bit immediate",
        jump_immediate,
        [0, 0, 1],
    ),

    # UNCONDITIONAL
    (
        "JI",
        "Jump to 16-bit immediate",
        jump_immediate,
        [0, 0, 0],
    ),

    ### STACK ###
    # PUSH

    # POP

    ### MISC ###
    (
        "OUT",
        "Output value in A",
        [MAC, RO | II, AO | OUT, RST | CNI],
        [0, 0, 0],
    ),
    (
        "HLT",
        "Halts",
        [MAC, RO | II, HLT, RST | CNI],
        [0, 0, 0],
    ),
]

instruction_names = [instruction[0] for instruction in instructions]
