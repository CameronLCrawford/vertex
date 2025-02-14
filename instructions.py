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
jump_immediate = [CNI | ADI | RO | ATI, CNI | ADI | RO | CLI, ATO | CHI, RST]

class Instruction():
    name: str
    description: str
    microinstructions: list[int]
    # List of three ints, where each is the scope for the respective
    # flag -- [zero, sign, carry].
    # A scope can be -1, 0, or 1:
    # - If scope = -1, this instruction is present only when the respective flag is low
    # - If scope = 0, this instruction is present irrespective of the state of the respective flag
    # - If scope = 1, this instruction is present only when the respective flag is high
    scopes: list[int]

    def __init__(self, name, description, microinstructions, scopes=[0, 0, 0]) -> None:
        self.name = name
        self.description = description
        self.microinstructions = [MAC, RO | II] + microinstructions
        self.scopes = scopes

instructions: list[Instruction] = [
    ### ALU ###
    # ADD
    Instruction(
        "ADDA",
        "Add A to A",
        [AO | ATI, ADD | AI, RST | CNI],
    ),
    Instruction(
        "ADDH",
        "Add H to A",
        [HO | ATI, ADD | AI, RST | CNI],
    ),
    Instruction(
        "ADDL",
        "Add L to A",
        [LO | ATI, ADD | AI, RST | CNI],
    ),
    Instruction(
        "ADDI",
        "Add immediate to A",
        [CNI | ADI | RO | ATI, ADD | AI, RST | CNI],
    ),

    # SUBTRACT
    Instruction(
        "SUBH",
        "Subtract H from A",
        [HO | ATI, SUB | AI, RST | CNI],
    ),
    Instruction(
        "SUBL",
        "Subtact L from A",
        [LO | ATI, SUB | AI, RST | CNI],
    ),
    Instruction(
        "SUBI",
        "Subtract immediate from A",
        [CNI | ADI | RO | ATI, SUB | AI, RST | CNI],
    ),

    # AND
    Instruction(
        "ANDH",
        "And H with A",
        [HO | ATI, AND | AI, RST | CNI]
    ),
    Instruction(
        "ANDL",
        "And L with A",
        [LO | ATI, AND | AI, RST | CNI]
    ),
    Instruction(
        "ANDI",
        "And immediate with A",
        [CNI | ADI | RO | ATI, AND | AI, RST | CNI]
    ),

    # OR
    Instruction(
        "ORH",
        "Or H with A",
        [HO | ATI, OR | AI, RST | CNI]
    ),
    Instruction(
        "ORL",
        "Or L with A",
        [LO | ATI, OR | AI, RST | CNI]
    ),
    Instruction(
        "ORI",
        "Or immediate with A",
        [CNI | ADI | RO | ATI, OR | AI, RST | CNI]
    ),

    # XOR
    Instruction(
        "XORH",
        "Xor H with A",
        [HO | ATI, XOR | AI, RST | CNI]
    ),
    Instruction(
        "XORL",
        "Xor L with A",
        [LO | ATI, XOR | AI, RST | CNI]
    ),
    Instruction(
        "XORI",
        "Xor immediate with A",
        [CNI | ADI | RO | ATI, XOR | AI, RST | CNI]
    ),

    # NOT
    Instruction(
        "NOT",
        "Logical negate A",
        [NOT | AI, RST | CNI]
    ),

    # INCREMENT
    Instruction(
        "INC",
        "Increment register A",
        [INC | AI, RST | CNI],
    ),

    # DECREMENT
    Instruction(
        "DEC",
        "Decrement register A",
        [DEC | AI, RST | CNI],
    ),

    # SHIFT
    Instruction(
        "SHL",
        "Shift A left",
        [SHL | AI, RST | CNI],
    ),
    Instruction(
        "SHR",
        "Shift A right",
        [SHR | AI, RST | CNI],
    ),

    # ADD (CARRY CONDITIONAL)
    Instruction(
        "ADDCA",
        "Add A to A (carry conditional)",
        [AO | ATI, ADDC | AI, RST | CNI],
    ),
    Instruction(
        "ADDCH",
        "Add H to A (carry conditional)",
        [HO | ATI, ADDC | AI, RST | CNI],
    ),
    Instruction(
        "ADDCL",
        "Add L to A (carry conditional)",
        [LO | ATI, ADDC | AI, RST | CNI],
    ),
    Instruction(
        "ADDCI",
        "Add immediate to A (carry conditional)",
        [CNI | ADI | RO | ATI, ADDC | AI, RST | CNI],
    ),

    # SUBTRACT (CARRY CONDITIONAL)
    Instruction(
        "SUBCH",
        "Subtract H from A (carry conditional)",
        [HO | ATI, SUBC | AI, RST | CNI],
    ),
    Instruction(
        "ADDCL",
        "Subtract L from A (carry conditional)",
        [LO | ATI, SUBC | AI, RST | CNI],
    ),
    Instruction(
        "SUBCI",
        "Subtract immediate from A (carry conditional)",
        [CNI | ADI | RO | ATI, SUBC | AI, RST | CNI],
    ),

    # INCREMENT (CARRY CONDITIONAL)
    Instruction(
        "INCC",
        "Increment A (carry conditional)",
        [INCC | AI, RST | CNI],
    ),

    # DECREMENT (CARRY CONDITIONAL)
    Instruction(
        "DECC",
        "Decrement A (carry conditional)",
        [DECC | AI, RST | CNI],
    ),

    # NEGATE
    Instruction(
        "NEGA",
        "Arithmetic negate register A",
        [UNEG | AI, RST | CNI],
    ),


    ### DATA ###
    Instruction(
        "MOVAI",
        "Move immediate into A",
        [CNI | ADI | RO | AI, RST | CNI],
    ),
    Instruction(
        "MOVHI",
        "Move immediate into H",
        [CNI | ADI | RO | HI, RST | CNI],
    ),
    Instruction(
        "MOVLI",
        "Move immediate into L",
        [CNI | ADI | RO | LI, RST | CNI],
    ),
    Instruction(
        "MOVA@",
        "Move value at address in adjacent two bytes into A",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | ALI, RO | AI, RST | CNI],
    ),
    Instruction(
        "MOVH@",
        "Move value at address in adjacent two bytes into H",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | ALI, RO | HI, RST | CNI],
    ),
    Instruction(
        "MOVL@",
        "Move value at address in adjacent two bytes into L",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | ALI, RO | LI, RST | CNI],
    ),


    ### JUMP ###
    # CONDITIONAL
    Instruction(
        "JZI",
        "Jump if zero to 16-bit immediate",
        jump_immediate,
        [1, 0, 0],
    ),
    Instruction(
        "JNZI",
        "Jump if not zero to 16-bit immediate",
        jump_immediate,
        [-1, 0, 0],
    ),
    Instruction(
        "JNSI",
        "Jump if sign to 16-bit immediate",
        jump_immediate,
        [0, 1, 0],
    ),
    Instruction(
        "JNSI",
        "Jump if not sign to 16-bit immediate",
        jump_immediate,
        [0, -1, 0],
    ),
    Instruction(
        "JCI",
        "Jump if carry to 16-bit immediate",
        jump_immediate,
        [0, 0, 1],
    ),
    Instruction(
        "JNCI",
        "Jump if not carry to 16-bit immediate",
        jump_immediate,
        [0, 0, -1],
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
        [CNI | ADI | RO | ATI, STD | MAS, ATO | RI, RST | CNI],
    ),
    Instruction(
        "PSHA",
        "Push A",
        [STD | MAS, AO | RI, RST | CNI],
    ),
    Instruction(
        "PSHH",
        "Push H",
        [STD | MAS, HO | RI, RST | CNI],
    ),
    Instruction(
        "PSHL",
        "Push L",
        [STD | MAS, LO | RI, RST | CNI],
    ),
    Instruction(
        "PSH@",
        "Push value at address in adjacent two bytes",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | ALI, STD | RO | ATI | MAS, ATO | RI, RST | CNI],
    ),

    # POP
    Instruction(
        "POPA",
        "Pop A",
        [MAS, STI | AI | RO, RST | CNI],
    ),
    Instruction(
        "POPH",
        "Pop H",
        [MAS, STI | HI | RO, RST | CNI],
    ),
    Instruction(
        "POPL",
        "Pop L",
        [MAS, STI | LI | RO, RST | CNI],
    ),

    ### MISC ###
    Instruction(
        "OUT",
        "Output value in A",
        [AO | OUT, RST | CNI],
    ),
    Instruction(
        "HLT",
        "Halts",
        [HLT, RST | CNI],
    ),
]

instruction_names = [instruction.name for instruction in instructions]
invalid_conditional_jump = [MAC, RO | II, CNI, CNI, RST | CNI]
