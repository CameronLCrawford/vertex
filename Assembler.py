from vtx.VtxVisitor import VtxVisitor
from vtx.VtxParser import VtxParser
from instructions import instructions, instruction_names

def convert_address_to_bytes(address: int) -> tuple[int, int]:
    binary_address = bin(address)[2:].zfill(16)
    high_byte = int(binary_address[:8], 2)
    low_byte = int(binary_address[8:], 2)
    return (high_byte, low_byte)

class Assembler(VtxVisitor):
    def __init__(self):
        self.instructions: list[int] = []
        self.symbol_table: dict[str, int] = {}
        self.current_address = 2**15
        self.debug_info = []

    def visitProgram(self, ctx: VtxParser.ProgramContext):
        for line in ctx.line():
            self.visit(line)
        # Resolve jump names with symbol table
        for i, instruction in enumerate(self.instructions):
            if instruction in self.symbol_table:
                prefix = self.instructions[:i]
                try:
                    suffix = self.instructions[(i + 2):]
                except IndexError:
                    suffix = []
                address_bytes = convert_address_to_bytes(self.symbol_table[instruction])
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
        if label_name in self.symbol_table:
            print(f"Warning: Label {label_name} defined more than once")
        self.symbol_table[label_name] = self.current_address

    def visitInstruction(self, ctx: VtxParser.InstructionContext):
        instruction = self.visitChildren(ctx)
        if instruction:
            self.instructions += instruction
            self.current_address += len(instruction)
            debug_instruction = instructions[instruction[0]]
            self.debug_info.append([
                debug_instruction.name,
                debug_instruction.microinstructions,
            ])
            self.debug_info += instruction[1:]

    def visitMove(self, ctx: VtxParser.MoveContext):
        destination = ctx.destination().getText().upper()
        source = ctx.source()
        if source.REGISTER():
            register = source.REGISTER().getText().upper()
            return [instruction_names.index(f"MOV{destination}{register}")]
        elif source.CONSTANT():
            constant = int(source.CONSTANT().getText())
            return [instruction_names.index(f"MOV{destination}I"), constant]
        elif source.ADDRESS():
            source = source.ADDRESS().getText()
            try:
                address = int(source.ADDRESS().CONSTANT())
            except ValueError:
                raise Exception("Cannot cast address to int")
            high_byte, low_byte = convert_address_to_bytes(address)
            return [instruction_names.index("MOVA@"), high_byte, low_byte]

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
                address = int(source.ADDRESS().CONSTANT())
            except IndexError:
                raise Exception("Cannot cast address to int")
            high_byte, low_byte = convert_address_to_bytes(address)
            return [instruction_names.index("PSH@"), high_byte, low_byte]

    def visitPop(self, ctx: VtxParser.PopContext):
        destination = ctx.destination().getText().upper()
        return [instruction_names.index(f"POP{destination}")]

    def visitAdd(self, ctx: VtxParser.AddContext):
        source = ctx.source()
        if source.REGISTER():
            register = source.REGISTER().getText().upper()
            return [instruction_names.index(f"ADD{register}")]
        elif source.CONSTANT():
            immediate = int(source.CONSTANT().getText())
            return [instruction_names.index("ADDI"), immediate]
        elif source.ADDRESS():
            pass # TODO: implement ADD@

    def visitSub(self, ctx: VtxParser.SubContext):
        source = ctx.source()
        if source.REGISTER():
            register = source.REGISTER().getText().upper()
            return [instruction_names.index(f"SUB{register}")]
        elif source.CONSTANT():
            immediate = int(source.CONSTANT().getText())
            return [instruction_names.index("SUBI"), immediate]
        elif source.ADDRESS():
            pass # TODO: implement SUB@

    def visitBinaryAnd(self, ctx: VtxParser.BinaryAndContext):
        source = ctx.source()
        if source.REGISTER():
            register = source.REGISTER().getText().upper()
            return [instruction_names.index(f"AND{register}")]
        elif source.CONSTANT():
            immediate = int(source.CONSTANT().getText())
            return [instruction_names.index("ANDI"), immediate]
        elif source.ADDRESS():
            pass # TODO: implement AND@

    def visitBinaryOr(self, ctx: VtxParser.BinaryOrContext):
        source = ctx.source()
        if source.REGISTER():
            register = source.REGISTER().getText().upper()
            return [instruction_names.index(f"OR{register}")]
        elif source.CONSTANT():
            immediate = int(source.CONSTANT().getText())
            return [instruction_names.index("ORI"), immediate]
        elif source.ADDRESS():
            pass # TODO: implement OR@

    def visitBinaryXor(self, ctx: VtxParser.BinaryXorContext):
        source = ctx.source()
        if source.REGISTER():
            register = source.REGISTER().getText().upper()
            return [instruction_names.index(f"XOR{register}")]
        elif source.CONSTANT():
            immediate = int(source.CONSTANT().getText())
            return [instruction_names.index("XORI"), immediate]
        elif source.ADDRESS():
            pass # TODO: implement XOR@

    def visitBinaryNot(self, ctx: VtxParser.BinaryNotContext):
        return [instruction_names.index("NOT")]

    def visitIncrement(self, ctx: VtxParser.IncrementContext):
        return [instruction_names.index("INC")]

    def visitDecrement(self, ctx: VtxParser.DecrementContext):
        return [instruction_names.index("DEC")]

    def visitShiftLeft(self, ctx: VtxParser.ShiftLeftContext):
        return [instruction_names.index("SHL")]

    def visitShiftRight(self, ctx: VtxParser.ShiftRightContext):
        return [instruction_names.index("SHR")]

    def visitNegate(self, ctx: VtxParser.NegateContext):
        return [instruction_names.index("NEG")]

    def visitJump(self, ctx: VtxParser.JumpContext):
        condition = ctx.CONDITION().getText().upper() if ctx.CONDITION() else ""
        label_name = ctx.NAME().getText()
        instruction = instruction_names.index(f"J{condition}I")
        return [instruction, label_name, "<LOW_BYTE>"]

    def visitOut(self, ctx: VtxParser.OutContext):
        return [instruction_names.index("OUT")]

    def visitHalt(self, ctx: VtxParser.HaltContext):
        return [instruction_names.index("HLT")]

