from vtx.VtxVisitor import VtxVisitor
from vtx.VtxParser import VtxParser
from instructions import instruction_names

class Assembler(VtxVisitor):
    def __init__(self):
        self.instructions = []
        self.symbol_table = {}
        self.current_address = 2**15

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
                address = bin(int(self.symbol_table[instruction]))[2:].zfill(16)
                high_byte = int(address[:8], 2)
                low_byte = int(address[8:], 2)
                address_bytes = [high_byte, low_byte]
                self.instructions = prefix + address_bytes + suffix
            elif instruction == "<LOW_BYTE>":
                continue
            else:
                try:
                    int(instruction)
                except ValueError:
                    print(f"Error on instruction: {instruction}")

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
            instruction = f"MOV{destination}A"
            return [instruction_names.index(instruction)]

    def visitPush(self, ctx: VtxParser.PushContext):
        source = ctx.source().getText().upper()
        return [instruction_names.index(f"PUSH{source}")]

    def visitPop(self, ctx: VtxParser.PopContext):
        destination = ctx.destination().getText().upper()
        return [instruction_names.index(f"POP{destination}")]

    def visitAdd(self, ctx: VtxParser.AddContext):
        source = ctx.source().getText().upper()
        return [instruction_names.index(f"ADD{source}")]

    def visitSub(self, ctx: VtxParser.SubContext):
        source = ctx.source().getText().upper()
        return [instruction_names.index(f"SUB{source}")]

    def visitShiftLeft(self, ctx: VtxParser.ShiftLeftContext):
        return [instruction_names.index("SHL")]

    def visitShiftRight(self, ctx: VtxParser.ShiftRightContext):
        return [instruction_names.index("SHR")]

    def visitJump(self, ctx: VtxParser.JumpContext):
        condition = ctx.CONDITION().getText().upper() if ctx.CONDITION() else ""
        label_name = ctx.NAME().getText()
        instruction = instruction_names.index(f"J{condition}I")
        return [instruction, label_name, "<LOW_BYTE>"]

    def visitOut(self, ctx: VtxParser.OutContext):
        return [instruction_names.index("OUT")]

    def visitHalt(self, ctx: VtxParser.HaltContext):
        return [instruction_names.index("HLT")]

