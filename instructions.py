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
BI  =   I1 | I0
CI  =   I2
HI  =   I2 | I0
LI  =   I2 | I1
CHI =   I2 | I1 | I0
CLI =   I3
AHI =   I3 | I0
ALI =   I3 | I1
BHI =   I3 | I1 | I0
BLI =   I3 | I2
SHI =   I3 | I2 | I0
SLI =   I3 | I2 | I1
II  =   I3 | I2 | I1 | I0

# Register out codes
AO  =   O0
ATO =   O1
BO  =   O1 | O0
CO  =   O2
HO  =   O2 | O0
LO  =   O2 | O1
CHO =   O2 | O1 | O0
CLO =   O3
AHO =   O3 | O0
ALO =   O3 | O1
BHO =   O3 | O1 | O0
BLO =   O3 | O2
SHO =   O3 | O2 | O0
SLO =   O3 | O2 | O1
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
SHRC    = A3 | A2 | A1 | A0

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
    def __init__(self, name, description, microinstructions, scopes=[0, 0, 0]) -> None:
        self.name = name
        self.description = description
        self.microinstructions = [MAC, RO | II] + microinstructions
        # List of three ints, where each is the scope for the respective
        # flag -- [zero, sign, carry].
        # A scope can be -1, 0, or 1:
        # - If scope = -1, this instruction is present only when the respective flag is low
        # - If scope = 0, this instruction is present irrespective of the state of the respective flag
        # - If scope = 1, this instruction is present only when the respective flag is high
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
        "ADDB",
        "Add B to A",
        [BO | ATI, ADD | AI, RST | CNI],
    ),
    Instruction(
        "ADDC",
        "Add C to A",
        [CO | ATI, ADD | AI, RST | CNI],
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
    Instruction(
        "ADD@",
        "Add value at address in adjacent two bytes to A",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | ATI, ADD | AI]
    ),

    # SUBTRACT
    Instruction(
        "SUBB",
        "Subtract B from A",
        [BO | ATI, SUB | AI, RST | CNI],
    ),
    Instruction(
        "SUBC",
        "Subtract C from A",
        [CO | ATI, SUB | AI, RST | CNI],
    ),
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
    Instruction(
        "SUB@",
        "Subtract value at address in adjacent two bytes from A",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | ATI, SUB | AI]
    ),

    # AND
    Instruction(
        "ANDB",
        "And B with A",
        [BO | ATI, AND | AI, RST | CNI]
    ),
    Instruction(
        "ANDC",
        "And C with A",
        [CO | ATI, AND | AI, RST | CNI]
    ),
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
    Instruction(
        "AND@",
        "And value at address in adjacent two bytes with A",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | ATI, AND | AI]
    ),

    # OR
    Instruction(
        "ORB",
        "Or B with A",
        [BO | ATI, OR | AI, RST | CNI]
    ),
    Instruction(
        "ORC",
        "Or C with A",
        [CO | ATI, OR | AI, RST | CNI]
    ),
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
    Instruction(
        "OR@",
        "Or value at address in adjacent two bytes with A",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | ATI, OR | AI]
    ),

    # XOR
    Instruction(
        "XORB",
        "Xor B with A",
        [BO | ATI, XOR | AI, RST | CNI]
    ),
    Instruction(
        "XORC",
        "Xor C with A",
        [CO | ATI, XOR | AI, RST | CNI]
    ),
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
    Instruction(
        "XOR@",
        "Xor value at address in adjacent two bytes with A",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | ATI, XOR | AI]
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
        "ADDCB",
        "Add B to A (carry conditional)",
        [BO | ATI, ADDC | AI, RST | CNI],
    ),
    Instruction(
        "ADDCC",
        "Add C to A (carry conditional)",
        [CO | ATI, ADDC | AI, RST | CNI],
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
    Instruction(
        "ADDC@",
        "Add value at address in adjacent two bytes to A (carry conditional)",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | ATI, ADDC | AI]
    ),

    # SUBTRACT (CARRY CONDITIONAL)
    Instruction(
        "SUBCB",
        "Subtract B from A (carry conditional)",
        [BO | ATI, SUBC | AI, RST | CNI],
    ),
    Instruction(
        "SUBCC",
        "Subtract C from A (carry conditional)",
        [CO | ATI, SUBC | AI, RST | CNI],
    ),
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
    Instruction(
        "SUBC@",
        "Subtract value at address in adjacent two bytes from A (carry conditional)",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | ATI, SUBC | AI]
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

    # SHIFT RIGHT (CARRY CONDITIONAL)
    Instruction(
        "SHRC",
        "Shift A right (carry conditional)",
        [SHRC | AI, RST | CNI],
    ),

    ### DATA ###

    # IMMEDIATE MOVES
    Instruction(
        "LDRAI",
        "Move immediate into A",
        [CNI | ADI | RO | AI, RST | CNI],
    ),
    Instruction(
        "LDRBI",
        "Move immediate into B",
        [CNI | ADI | RO | BI, RST | CNI],
    ),
    Instruction(
        "LDRCI",
        "Move immediate into C",
        [CNI | ADI | RO | CI, RST | CNI],
    ),
    Instruction(
        "LDRHI",
        "Move immediate into H",
        [CNI | ADI | RO | HI, RST | CNI],
    ),
    Instruction(
        "LDRLI",
        "Move immediate into L",
        [CNI | ADI | RO | LI, RST | CNI],
    ),

    # MEMORY MOVES
    Instruction(
        "LDRA@",
        "Move value at address in adjacent two bytes into A",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | AI, RST | CNI],
    ),
    Instruction(
        "LDRB@",
        "Move value at address in adjacent two bytes into B",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | BI, RST | CNI],
    ),
    Instruction(
        "LDRC@",
        "Move value at address in adjacent two bytes into C",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | CI, RST | CNI],
    ),
    Instruction(
        "LDRH@",
        "Move value at address in adjacent two bytes into H",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | HI, RST | CNI],
    ),
    Instruction(
        "LDRL@",
        "Move value at address in adjacent two bytes into L",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | LI, RST | CNI],
    ),

    # REGISTER-REGISTER MOVES

    # MOVE INTO A
    Instruction(
        "LDRAB",
        "Move B into A",
        [BO | AI, RST | CNI],
    ),
    Instruction(
        "LDRAC",
        "Move C into A",
        [CO | AI, RST | CNI],
    ),
    Instruction(
        "LDRAL",
        "Move L into A",
        [LO | AI, RST | CNI],
    ),
    Instruction(
        "LDRAH",
        "Move H into A",
        [HO | AI, RST | CNI],
    ),

    # MOVE INTO B
    Instruction(
        "LDRBA",
        "Move A into B",
        [AO | BI, RST | CNI],
    ),
    Instruction(
        "LDRBC",
        "Move C into B",
        [CO | BI, RST | CNI],
    ),
    Instruction(
        "LDRBL",
        "Move L into B",
        [LO | BI, RST | CNI],
    ),
    Instruction(
        "LDRBH",
        "Move H into B",
        [HO | BI, RST | CNI],
    ),

    # MOVE INTO C
    Instruction(
        "LDRCA",
        "Move A into C",
        [AO | CI, RST | CNI],
    ),
    Instruction(
        "LDRCB",
        "Move B into C",
        [BO | CI, RST | CNI],
    ),
    Instruction(
        "LDRCL",
        "Move L into C",
        [LO | CI, RST | CNI],
    ),
    Instruction(
        "LDRCH",
        "Move H into C",
        [HO | CI, RST | CNI],
    ),

    # MOVE INTO L
    Instruction(
        "LDRLA",
        "Move A into L",
        [AO | LI, RST | CNI],
    ),
    Instruction(
        "LDRLB",
        "Move B into L",
        [BO | LI, RST | CNI],
    ),
    Instruction(
        "LDRLC",
        "Move C into L",
        [CO | LI, RST | CNI],
    ),
    Instruction(
        "LDRLH",
        "Move H into L",
        [HO | LI, RST | CNI],
    ),

    # MOVE INTO H
    Instruction(
        "LDRHA",
        "Move A into H",
        [AO | HI, RST | CNI],
    ),
    Instruction(
        "LDRHB",
        "Move B into H",
        [BO | HI, RST | CNI],
    ),
    Instruction(
        "LDRHC",
        "Move C into H",
        [CO | HI, RST | CNI],
    ),
    Instruction(
        "LDRHL",
        "Move L into H",
        [LO | HI, RST | CNI],
    ),

    # STORE
    Instruction(
        "STR@A",
        "Move A into address in adjacent two bytes",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, AO | RI, RST | CNI],
    ),
    Instruction(
        "STR@A",
        "Move A into address in adjacent two bytes",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, AO | RI, RST | CNI],
    ),
    Instruction(
        "STR@B",
        "Move B into address in adjacent two bytes",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, BO | RI, RST | CNI],
    ),
    Instruction(
        "STR@C",
        "Move C into address in adjacent two bytes",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, CO | RI, RST | CNI],
    ),
    Instruction(
        "STR@H",
        "Move H into address in adjacent two bytes",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, HO | RI, RST | CNI],
    ),
    Instruction(
        "STR@L",
        "Move L into address in adjacent two bytes",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, LO | RI, RST | CNI],
    ),

    ### JUMP ###
    # CONDITIONAL
    Instruction(
        "JZFI",
        "Jump if zero to 16-bit immediate",
        jump_immediate,
        [1, 0, 0],
    ),
    Instruction(
        "JNZFI",
        "Jump if not zero to 16-bit immediate",
        jump_immediate,
        [-1, 0, 0],
    ),
    Instruction(
        "JSFI",
        "Jump if sign to 16-bit immediate",
        jump_immediate,
        [0, 1, 0],
    ),
    Instruction(
        "JNSFI",
        "Jump if not sign to 16-bit immediate",
        jump_immediate,
        [0, -1, 0],
    ),
    Instruction(
        "JCFI",
        "Jump if carry to 16-bit immediate",
        jump_immediate,
        [0, 0, 1],
    ),
    Instruction(
        "JNCFI",
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
        "PSHB",
        "Push B",
        [STD | MAS, BO | RI, RST | CNI],
    ),
    Instruction(
        "PSHC",
        "Push C",
        [STD | MAS, CO | RI, RST | CNI],
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
        "POPB",
        "Pop B",
        [MAS, STI | BI | RO, RST | CNI],
    ),
    Instruction(
        "POPC",
        "Pop C",
        [MAS, STI | CI | RO, RST | CNI],
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

# this may make life easier one day
if len(instructions) > 256:
    raise Exception("More than 256 instructions!")
instruction_names = [instruction.name for instruction in instructions]
invalid_conditional_jump = [MAC, RO | II, CNI, CNI, RST | CNI]

if __name__ == "__main__":
    print(f"There are {len(instructions)} instructions")
