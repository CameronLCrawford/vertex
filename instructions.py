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

class Instruction():
    name: str
    description: str
    microinstructions: list[int]
    # List of three ints, where each is the scope for the respective
    # flag -- control, sign, zero.
    # A scope can be -1, 0, or 1:
    # - If scope = -1, this instruction is present only when the respective flag is low
    # - If scope = 0, this instruction is present irrespective of the state of the respective flag
    # - If scope = 1, this instruction is present only when the respective flag is high
    scopes: list[int]

    def __init__(self, name, description, microinstructions, scopes=[0, 0, 0]) -> None:
        self.name = name
        self.description = description
        self.microinstructions = microinstructions
        self.scopes = scopes

instructions: list[Instruction] = [
    ### ALU ###
    # ADD
    Instruction(
        "ADDA",
        "Add A to A",
        [MAC, RO | II, AO | ATI, ADD | AI, RST | CNI],
    ),
    Instruction(
        "ADDH",
        "Add H to A",
        [MAC, RO | II, HO | ATI, ADD | AI, RST | CNI],
    ),
    Instruction(
        "ADDL",
        "Add L to A",
        [MAC, RO | II, LO | ATI, ADD | AI, RST | CNI],
    ),
    Instruction(
        "ADDI",
        "Add immediate to A",
        [MAC, RO | II, CNI | ADI | RO | ATI, ADD | AI, RST | CNI],
    ),

    # SUBTRACT
    Instruction(
        "SUBH",
        "Subtract H from A",
        [MAC, RO | II, HO | ATI, SUB | AI, RST | CNI],
    ),
    Instruction(
        "SUBL",
        "Subtact L from A",
        [MAC, RO | II, LO | ATI, SUB | AI, RST | CNI],
    ),
    Instruction(
        "SUBI",
        "Subtract immediate from A",
        [MAC, RO | II, CNI | ADI | RO | ATI, SUB | AI, RST | CNI],
    ),

    # AND
    Instruction(
        "ANDH",
        "And H with A",
        [MAC, RO | II, HO | ATI, AND | AI, RST | CNI]
    ),
    Instruction(
        "ANDL",
        "And L with A",
        [MAC, RO | II, LO | ATI, AND | AI, RST | CNI]
    ),
    Instruction(
        "ANDI",
        "And immediate with A",
        [MAC, RO | II, CNI | ADI | RO | ATI, AND | AI, RST | CNI]
    ),

    # OR
    Instruction(
        "ORH",
        "Or H with A",
        [MAC, RO | II, HO | ATI, OR | AI, RST | CNI]
    ),
    Instruction(
        "ORL",
        "Or L with A",
        [MAC, RO | II, LO | ATI, OR | AI, RST | CNI]
    ),
    Instruction(
        "ORI",
        "Or immediate with A",
        [MAC, RO | II, CNI | ADI | RO | ATI, OR | AI, RST | CNI]
    ),

    # XOR
    Instruction(
        "XORH",
        "Xor H with A",
        [MAC, RO | II, HO | ATI, XOR | AI, RST | CNI]
    ),
    Instruction(
        "XORL",
        "Xor L with A",
        [MAC, RO | II, LO | ATI, XOR | AI, RST | CNI]
    ),
    Instruction(
        "XORI",
        "Xor immediate with A",
        [MAC, RO | II, CNI | ADI | RO | ATI, XOR | AI, RST | CNI]
    ),

    # NOT
    Instruction(
        "NOT",
        "Logical negate A",
        [MAC, RO | II, NOT | AI, RST | CNI]
    ),

    # INCREMENT
    Instruction(
        "INC",
        "Increment register A",
        [MAC, RO | II, INC | AI, RST | CNI],
    ),

    # DECREMENT
    Instruction(
        "DEC",
        "Decrement register A",
        [MAC, RO | II, DEC | AI, RST | CNI],
    ),

    # SHIFT
    Instruction(
        "SHL",
        "Shift A left",
        [MAC, RO | II, SHL | AI, RST | CNI],
    ),
    Instruction(
        "SHR",
        "Shift A right",
        [MAC, RO | II, SHR | AI, RST | CNI],
    ),

    # ADD (CARRY CONDITIONAL)
    Instruction(
        "ADDCA",
        "Add A to A (carry conditional)",
        [MAC, RO | II, AO | ATI, ADDC | AI, RST | CNI],
    ),
    Instruction(
        "ADDCH",
        "Add H to A (carry conditional)",
        [MAC, RO | II, HO | ATI, ADDC | AI, RST | CNI],
    ),
    Instruction(
        "ADDCL",
        "Add L to A (carry conditional)",
        [MAC, RO | II, LO | ATI, ADDC | AI, RST | CNI],
    ),
    Instruction(
        "ADDCI",
        "Add immediate to A (carry conditional)",
        [MAC, RO | II, CNI | ADI | RO | ATI, ADDC | AI, RST | CNI],
    ),

    # SUBTRACT (CARRY CONDITIONAL)
    Instruction(
        "SUBCH",
        "Subtract H from A (carry conditional)",
        [MAC, RO | II, HO | ATI, SUBC | AI, RST | CNI],
    ),
    Instruction(
        "ADDCL",
        "Subtract L from A (carry conditional)",
        [MAC, RO | II, LO | ATI, SUBC | AI, RST | CNI],
    ),
    Instruction(
        "SUBCI",
        "Subtract immediate from A (carry conditional)",
        [MAC, RO | II, CNI | ADI | RO | ATI, SUBC | AI, RST | CNI],
    ),

    # INCREMENT (CARRY CONDITIONAL)
    Instruction(
        "INCC",
        "Increment A (carry conditional)",
        [MAC, RO | II, INCC | AI, RST | CNI],
    ),

    # DECREMENT (CARRY CONDITIONAL)
    Instruction(
        "DECC",
        "Decrement A (carry conditional)",
        [MAC, RO | II, DECC | AI, RST | CNI],
    ),

    # NEGATE
    Instruction(
        "NEGA",
        "Arithmetic negate register A",
        [MAC, RO | II, UNEG | AI, RST | CNI],
    ),


    ### DATA ###
    Instruction(
        "MOVAI",
        "Move immediate into A",
        [MAC, RO | II, CNI | ADI | RO | AI, RST | CNI],
    ),
    Instruction(
        "MOVHI",
        "Move immediate into H",
        [MAC, RO | II, CNI | ADI | RO | HI, RST | CNI],
    ),
    Instruction(
        "MOVLI",
        "Move immediate into L",
        [MAC, RO | II, CNI | ADI | RO | LI, RST | CNI],
    ),


    ### JUMP ###
    # CONDITIONAL
    Instruction(
        "JZI",
        "Jump if zero to 16-bit immediate",
        jump_immediate,
        [0, 0, 1],
    ),
    Instruction(
        "JNZI",
        "Jump if not zero to 16-bit immediate",
        jump_immediate,
        [0, 0, -1],
    ),
    Instruction(
        "JCI",
        "Jump if carry to 16-bit immediate",
        jump_immediate,
        [0, 1, 0],
    ),
    Instruction(
        "JNCI",
        "Jump if not carry to 16-bit immediate",
        jump_immediate,
        [0, -1, 0],
    ),
    Instruction(
        "JNSI",
        "Jump if sign to 16-bit immediate",
        jump_immediate,
        [1, 0, 0],
    ),
    Instruction(
        "JNSI",
        "Jump if not sign to 16-bit immediate",
        jump_immediate,
        [-1, 0, 0],
    ),

    # UNCONDITIONAL
    Instruction(
        "JI",
        "Jump to 16-bit immediate",
        jump_immediate,
    ),

    ### STACK ###
    # PUSH
    Instruction(
        "PSHI",
        "Push immediate",
        [MAC, RO | II, CNI | ADI | RO | ATI | STD, MAS | ATO | RI],
    ),
    Instruction(
        "PSHA",
        "Push A",
        [MAC, RO | II | STD, MAS | AO | RI],
    ),
    Instruction(
        "PSHH",
        "Push H",
        [MAC, RO | II | STD, MAS | HO | RI],
    ),
    Instruction(
        "PSHL",
        "Push L",
        [MAC, RO | II | STD, MAS | LO | RI],
    ),


    # POP
    Instruction(
        "POPA",
        "Pop A",
        [MAC, RO | II | MAS, STI | AI | RO],
    ),
    Instruction(
        "POPH",
        "Pop H",
        [MAC, RO | II | MAS, STI | HI | RO],
    ),
    Instruction(
        "POPL",
        "Pop L",
        [MAC, RO | II | MAS, STI | LI | RO],
    ),

    ### MISC ###
    Instruction(
        "OUT",
        "Output value in A",
        [MAC, RO | II, AO | OUT, RST | CNI],
    ),
    Instruction(
        "HLT",
        "Halts",
        [MAC, RO | II, HLT, RST | CNI],
    ),
]

instruction_names = [instruction.name for instruction in instructions]
