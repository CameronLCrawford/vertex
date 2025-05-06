from vtx.VtxVisitor import VtxVisitor
from vtx.VtxParser import VtxParser
from instructions import instructions, instruction_names

MEMORY_SIZE = 2**16

def convert_address_to_bytes(address: int) -> tuple[int, int]:
    binary_address = bin(address)[2:].zfill(16)
    high_byte = int(binary_address[:8], 2)
    low_byte = int(binary_address[8:], 2)
    return (high_byte, low_byte)

class Assembler(VtxVisitor):
    def __init__(self):
        self.instructions: list[int] = []
        self.label_offset: dict[str, int] = {} # map from label to its offset relative to start of program
        self.program_offset = 0 # offset from start of program
        self.debug_info = []

    def visitProgram(self, ctx: VtxParser.ProgramContext):
        for line in ctx.line():
            self.visit(line)
        # Resolve jump / call names with symbol table
        program_size = len(self.instructions)
        for label in self.label_offset:
            self.label_offset[label] += MEMORY_SIZE - program_size
        for i, instruction in enumerate(self.instructions):
            if instruction in self.label_offset:
                prefix = self.instructions[:i]
                try:
                    suffix = self.instructions[(i + 2):]
                except IndexError:
                    suffix = []
                address_bytes = convert_address_to_bytes(self.label_offset[instruction])
                self.instructions = prefix + list(address_bytes) + suffix
            elif instruction == "<LOW_BYTE>":
                continue
            else:
                try:
                    int(instruction)
                except ValueError:
                    raise Exception(f"Error on instruction: {instruction}")

    def visitLabel(self, ctx: VtxParser.LabelContext):
        label_name = ctx.NAME().getText()
        if label_name in self.label_offset:
            print(f"Warning: Label {label_name} defined more than once")
        self.label_offset[label_name] = self.program_offset

    def visitInstruction(self, ctx: VtxParser.InstructionContext):
        instruction = self.visitChildren(ctx)
        if instruction:
            self.instructions += instruction
            self.program_offset += len(instruction)
            debug_instruction = instructions[instruction[0]]
            self.debug_info.append([
                debug_instruction.name,
                debug_instruction.microinstructions,
            ])
            self.debug_info += instruction[1:]

    def visitLoadRegister(self, ctx: VtxParser.LoadRegisterContext):
        destination = ctx.REGISTER().getText().upper()
        source = ctx.source()
        if source.REGISTER():
            register = source.REGISTER().getText().upper()
            return [instruction_names.index(f"LDR{destination}{register}")]
        elif source.CONSTANT():
            constant = int(source.CONSTANT().getText())
            return [instruction_names.index(f"LDR{destination}I"), constant]
        elif source.ADDRESS():
            try:
                address = int(source.ADDRESS().getText()[1:])
            except ValueError:
                raise Exception("Cannot cast address to int")
            high_byte, low_byte = convert_address_to_bytes(address)
            return [instruction_names.index(f"LDR{destination}@"), high_byte, low_byte]
        elif source.M():
            return [instruction_names.index(f"LDR{destination}M")]

    def visitStore(self, ctx: VtxParser.StoreContext):
        register = ctx.REGISTER().getText().upper()
        if ctx.ADDRESS():
            try:
                address = int(ctx.ADDRESS().getText()[1:])
            except ValueError:
                raise Exception("Cannot cast address to int")
            high_byte, low_byte = convert_address_to_bytes(address)
            return [instruction_names.index(f"STR@{register}"), high_byte, low_byte]
        elif ctx.M():
            return [instruction_names.index(f"STRM{register}")]

    def visitPush(self, ctx: VtxParser.PushContext):
        source = ctx.source()
        if source.REGISTER():
            register = source.REGISTER().getText().upper()
            return [instruction_names.index(f"PSH{register}")]
        elif source.CONSTANT():
            immediate = int(source.CONSTANT().getText())
            return [instruction_names.index("PSHI"), immediate]
        elif source.ADDRESS():
            try:
                address = int(source.ADDRESS().getText()[1:])
            except IndexError:
                raise Exception("Cannot cast address to int")
            high_byte, low_byte = convert_address_to_bytes(address)
            return [instruction_names.index("PSH@"), high_byte, low_byte]

    def visitPop(self, ctx: VtxParser.PopContext):
        destination = ctx.REGISTER().getText().upper()
        return [instruction_names.index(f"POP{destination}")]

    def visitAdd(self, ctx: VtxParser.AddContext):
        source = ctx.source()
        carry = ctx.CARRY()
        if carry:
            instruction = "ADDC"
        else:
            instruction = "ADD"
        if source.REGISTER():
            register = source.REGISTER().getText().upper()
            return [instruction_names.index(f"{instruction}{register}")]
        elif source.CONSTANT():
            immediate = int(source.CONSTANT().getText())
            return [instruction_names.index(f"{instruction}I"), immediate]
        elif source.ADDRESS():
            try:
                address = int(source.ADDRESS().getText()[1:])
            except IndexError:
                raise Exception("Cannot cast address to int")
            high_byte, low_byte = convert_address_to_bytes(address)
            return [instruction_names.index("ADD@"), high_byte, low_byte]

    def visitSub(self, ctx: VtxParser.SubContext):
        source = ctx.source()
        carry = ctx.CARRY()
        if carry:
            instruction = "SUBC"
        else:
            instruction = "SUB"
        if source.REGISTER():
            register = source.REGISTER().getText().upper()
            return [instruction_names.index(f"{instruction}{register}")]
        elif source.CONSTANT():
            immediate = int(source.CONSTANT().getText())
            return [instruction_names.index(f"{instruction}I"), immediate]
        elif source.ADDRESS():
            try:
                address = int(source.ADDRESS().getText()[1:])
            except IndexError:
                raise Exception("Cannot cast address to int")
            high_byte, low_byte = convert_address_to_bytes(address)
            return [instruction_names.index("OR@"), high_byte, low_byte]

    def visitBinaryAnd(self, ctx: VtxParser.BinaryAndContext):
        source = ctx.source()
        if source.REGISTER():
            register = source.REGISTER().getText().upper()
            return [instruction_names.index(f"AND{register}")]
        elif source.CONSTANT():
            immediate = int(source.CONSTANT().getText())
            return [instruction_names.index("ANDI"), immediate]
        elif source.ADDRESS():
            try:
                address = int(source.ADDRESS().getText()[1:])
            except IndexError:
                raise Exception("Cannot cast address to int")
            high_byte, low_byte = convert_address_to_bytes(address)
            return [instruction_names.index("AND@"), high_byte, low_byte]

    def visitBinaryOr(self, ctx: VtxParser.BinaryOrContext):
        source = ctx.source()
        if source.REGISTER():
            register = source.REGISTER().getText().upper()
            return [instruction_names.index(f"OR{register}")]
        elif source.CONSTANT():
            immediate = int(source.CONSTANT().getText())
            return [instruction_names.index("ORI"), immediate]
        elif source.ADDRESS():
            try:
                address = int(source.ADDRESS().getText()[1:])
            except IndexError:
                raise Exception("Cannot cast address to int")
            high_byte, low_byte = convert_address_to_bytes(address)
            return [instruction_names.index("OR@"), high_byte, low_byte]

    def visitBinaryXor(self, ctx: VtxParser.BinaryXorContext):
        source = ctx.source()
        if source.REGISTER():
            register = source.REGISTER().getText().upper()
            return [instruction_names.index(f"XOR{register}")]
        elif source.CONSTANT():
            immediate = int(source.CONSTANT().getText())
            return [instruction_names.index("XORI"), immediate]
        elif source.ADDRESS():
            try:
                address = int(source.ADDRESS().getText()[1:])
            except IndexError:
                raise Exception("Cannot cast address to int")
            high_byte, low_byte = convert_address_to_bytes(address)
            return [instruction_names.index("XOR@"), high_byte, low_byte]

    def visitBinaryNot(self, ctx: VtxParser.BinaryNotContext):
        return [instruction_names.index("NOT")]

    def visitIncrement(self, ctx: VtxParser.IncrementContext):
        carry = ctx.CARRY()
        if carry:
            instruction = "INCC"
        else:
            instruction = "INC"
        return [instruction_names.index(instruction)]

    def visitDecrement(self, ctx: VtxParser.DecrementContext):
        carry = ctx.CARRY()
        if carry:
            instruction = "DECC"
        else:
            instruction = "DEC"
        return [instruction_names.index(instruction)]

    def visitShiftLeft(self, ctx: VtxParser.ShiftLeftContext):
        return [instruction_names.index("SHL")]

    def visitShiftRight(self, ctx: VtxParser.ShiftRightContext):
        if ctx.CARRY():
            instruction = "SHRC"
        else:
            instruction = "SHR"
        return [instruction_names.index(instruction)]

    def visitJump(self, ctx: VtxParser.JumpContext):
        condition = ctx.CONDITION().getText().upper() if ctx.CONDITION() else ""
        if ctx.NAME():
            label_name = ctx.NAME().getText()
            instruction = instruction_names.index(f"J{condition}I")
            return [instruction, label_name, "<LOW_BYTE>"]
        elif ctx.M():
            return [instruction_names.index(f"J{condition}M")]

    def visitCall(self, ctx: VtxParser.CallContext):
        label_name = ctx.NAME().getText()
        return [instruction_names.index("CAL"), label_name, "<LOW_BYTE>"]

    def visitInterruptReturn(self, ctx: VtxParser.InterruptReturnContext):
        return [instruction_names.index("INTRET")]

    def visitOut(self, ctx: VtxParser.OutContext):
        return [instruction_names.index("OUT")]

    def visitHalt(self, ctx: VtxParser.HaltContext):
        return [instruction_names.index("HLT")]

