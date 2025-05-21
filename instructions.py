# Control bits
(I0, I1, I2, I3,        # Register input
 O0, O1, O2, O3,        # Register output
 A0, A1, A2, A3,        # Accumulator
 CNI, ADI, STI, STD,    # Counter signals
 MAC, MAS, MAH, MCI,    # Direct moves
 F1, F0, FI,            # Flags
 RI, RO,                # Memory
 RST, IEN, OUT, HLT     # Control and output
) = (2**i for i in range(29))

# Register in codes
AI      =   I0
ATI     =   I1
BI      =   I1 | I0
CI      =   I2
HI      =   I2 | I0
LI      =   I2 | I1
CNHI    =   I2 | I1 | I0
CNLI    =   I3
AHI     =   I3 | I0
ALI     =   I3 | I1
BPHI    =   I3 | I1 | I0
BPLI    =   I3 | I2
SPHI    =   I3 | I2 | I0
SPLI    =   I3 | I2 | I1
II      =   I3 | I2 | I1 | I0

# Register out codes
AO      =   O0
ATO     =   O1
BO      =   O1 | O0
CO      =   O2
HO      =   O2 | O0
LO      =   O2 | O1
CNHO    =   O2 | O1 | O0
CNLO    =   O3
AHO     =   O3 | O0
ALO     =   O3 | O1
BPHO    =   O3 | O1 | O0
BPLO    =   O3 | O2
SPHO    =   O3 | O2 | O0
SPLO    =   O3 | O2 | O1
IO      =   O3 | O2 | O1 | O0

# ALU codes
ADD     = A0
SUB     = A1
AND     = A1 | A0
OR      = A2
XOR     = A2 | A0
INC     = A2 | A1
DEC     = A2 | A1 | A0
SHR     = A3
SHL     = A3 | A0
ADDC     = A3 | A1
SUBC    = A3 | A1 | A0
INCC    = A3 | A2
DECC    = A3 | A2 | A0
SHRC    = A3 | A2 | A1
SHLC    = A3 | A2 | A1 | A0

# Status codes
SI      = FI
SO      = F1 | F0

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
jump_immediate = [CNI | ADI | RO | ATI, CNI | ADI | RO | CNLI, ATO | CNHI, RST]
jump_m = [LO | CNLI, HO | CNHI, RST]

class Instruction():
    def __init__(self, name, microinstructions, scopes=[0, 0, 0]):
        self.name = name
        if name == "INTCAL":
            self.microinstructions = microinstructions
        else:
            self.microinstructions = [MAC, RO | II] + microinstructions
        # List of three ints, where each is the scope for the respective
        # flag -- [zero, sign, carry].
        # A scope can be -1, 0, or 1:
        # - If scope = -1, this instruction is present only when the respective flag is low
        # - If scope = 0, this instruction is present irrespective of the state of the respective flag
        # - If scope = 1, this instruction is present only when the respective flag is high
        self.scopes = scopes

instructions: list[Instruction] = [
    ### NOP ###
    Instruction(
        "NOP",
        []
    ),

    ### INTERRUPT ###
    # Define this here so the address is known by CPU
    # and unlikely to change. Not exposed in assembly API
    Instruction(
        "INTCAL",
        [STD | MAS, CNHO | RI, STD | MAS, CNLO | RI, MCI, MAC, RO | II | RST],
    ),
    # This is exposed in assembly API
    Instruction(
        "INTRET",
        [IEN | MAS, STI | CNLI | RO, MAS, STI | CNHI | RO, RST],
    ),

    ### ALU ###

    # REGISTER
    *[
        Instruction(
            f"{operation}{source}",
            [eval(f"{source}O") | ATI, eval(operation) | AI, RST | CNI],
        )
        for source in ["B", "C", "H", "L"]
        for operation in ["ADD", "ADDC", "SUB", "SUBC", "AND", "OR", "XOR"]
    ],

    # IMMEDIATE
    *[
        Instruction(
            f"{operation}I",
            [CNI | ADI | RO | ATI, eval(operation) | AI, RST | CNI],
        )
        for operation in ["ADD", "ADDC", "SUB", "SUBC", "AND", "OR", "XOR"]
    ],

    # @
    *[
        Instruction(
            f"{operation}@",
            [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | ATI, eval(operation) | AI]
        )
        for operation in ["ADD", "SUB", "AND", "OR", "XOR"]
    ],

    # UNARY
    *[
        Instruction(
            operation,
            [eval(operation) | AI, RST | CNI],
        )
        for operation in ["INC", "INCC", "DEC", "DECC", "SHL", "SHR", "SHLC", "SHRC"]
    ],

    ### DATA ###

    # IMMEDIATE MOVES
    *[
        Instruction(
            f"LDR{destination}I",
            [CNI | ADI | RO | eval(f"{destination}I"), RST | CNI],
        )
        for destination in ["A", "B", "C", "H", "L"]
    ],

    # MEMORY MOVES
    *[
        Instruction(
            f"LDR{destination}@",
            [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, RO | eval(f"{destination}I"), RST | CNI],
        )
        for destination in ["A", "B", "C", "H", "L"]
    ],

    # M MOVES
    *[
        Instruction(
            f"LDR{destination}M",
            [HO | AHI, LO | ALI, RO | eval(f"{destination}I"), RST | CNI],
        )
        for destination in ["A", "B", "C", "H", "L"]
    ],

    # REGISTER-REGISTER MOVES

    # MOVE INTO A
    *[
        Instruction(
            f"LDRA{source}",
            [eval(f"{source}O") | AI, RST | CNI],
        )
        for source in ["B", "C", "H", "L", "BPL", "BPH", "SPL", "SPH"]
    ],

    # MOVE INTO B
    *[
        Instruction(
            f"LDRB{source}",
            [eval(f"{source}O") | BI, RST | CNI],
        )
        for source in ["A", "C", "H", "L"]
    ],

    # MOVE INTO C
    *[
        Instruction(
            f"LDRC{source}",
            [eval(f"{source}O") | CI, RST | CNI],
        )
        for source in ["A", "B", "H", "L"]
    ],

    # MOVE INTO L
    *[
        Instruction(
            f"LDRL{source}",
            [eval(f"{source}O") | LI, RST | CNI],
        )
        for source in ["A", "B", "C", "H"]
    ],

    # MOVE INTO H
    *[
        Instruction(
            f"LDRH{source}",
            [eval(f"{source}O") | HI, RST | CNI],
        )
        for source in ["A", "B", "C", "L"]
    ],


    # MOVE INTO BPL
    *[
        Instruction(
            f"LDRBPL{source}",
            [eval(f"{source}O") | BPLI, RST | CNI],
        )
        for source in ["A", "SPL"]
    ],

    # MOVE INTO BPH
    *[
        Instruction(
            f"LDRBPH{source}",
            [eval(f"{source}O") | BPHI, RST | CNI],
        )
        for source in ["A", "SPH"]
    ],

    # MOVE INTO SPL
    *[
        Instruction(
            f"LDRSPL{source}",
            [eval(f"{source}O") | SPLI, RST | CNI],
        )
        for source in ["A", "BPL"]
    ],

    # MOVE INTO SPH
    *[
        Instruction(
            f"LDRSPH{source}",
            [eval(f"{source}O") | SPHI, RST | CNI],
        )
        for source in ["A", "BPH"]
    ],

    # STORE IN ADDRESS
    *[
        Instruction(
            f"STR@{source}",
            [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | AHI, eval(f"{source}O") | RI, RST | CNI],
        )
        for source in ["A", "B", "C", "H", "L"]
    ],

    # STORE IN M
    *[
        Instruction(
            f"STRM{source}",
            [HO | AHI, LO | ALI, eval(f"{source}O") | RI, RST | CNI],
        )
        for source in ["A", "B", "C", "H", "L"]
    ],

    ### JUMP ###
    # CONDITIONAL
    Instruction(
        "JZFI",
        jump_immediate,
        [1, 0, 0],
    ),
    Instruction(
        "JNZFI",
        jump_immediate,
        [-1, 0, 0],
    ),
    Instruction(
        "JSFI",
        jump_immediate,
        [0, 1, 0],
    ),
    Instruction(
        "JNSFI",
        jump_immediate,
        [0, -1, 0],
    ),
    Instruction(
        "JCFI",
        jump_immediate,
        [0, 0, 1],
    ),
    Instruction(
        "JNCFI",
        jump_immediate,
        [0, 0, -1],
    ),

    # UNCONDITIONAL
    Instruction(
        "JI",
        jump_immediate,
    ),
    Instruction(
        "JM",
        jump_m,
    ),

    ### STACK ###

    # PUSH
    Instruction(
        "PSHI",
        [CNI | ADI | RO | ATI, STD | MAS, ATO | RI, RST | CNI],
    ),
    *[
        Instruction(
            f"PSH{source}",
            [STD | MAS, eval(f"{source}O") | RI, RST | CNI],
        )
        for source in ["A", "B", "C", "H", "L", "BPH", "BPL", "S"]
    ],
    Instruction(
        "PSH@",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | ALI, ATO | ALI, STD | RO | ATI | MAS, ATO | RI, RST | CNI],
    ),

    # POP
    *[
        Instruction(
            f"POP{destination}",
            [MAS, STI | eval(f"{destination}I") | RO, RST | CNI],
        )
        for destination in ["A", "B", "C", "H", "L", "BPH", "BPL", "S"]
    ],

    # CALL
    Instruction(
        "CAL",
        [CNI | ADI | RO | ATI, CNI | ADI | RO | AI, CNI | STD | MAS, CNHO | RI, STD | MAS, CNLO | RI, ATO | CNHI, AO | CNLI, RST],
    ),

    ### MISC ###
    Instruction(
        "IEN",
        [IEN, RST | CNI],
    ),
    Instruction(
        "OUT",
        [AO | OUT, RST | CNI],
    ),
    Instruction(
        "HLT",
        [HLT],
    ),
]

# this may make life easier one day
if len(instructions) > 256:
    raise Exception("More than 256 instructions!")
instruction_names = [instruction.name for instruction in instructions]
invalid_conditional_jump = [MAC, RO | II, CNI, CNI, RST | CNI]

if __name__ == "__main__":
    print(f"There are {len(instructions)} instructions")
