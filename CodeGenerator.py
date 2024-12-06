from storn.StornVisitor import StornVisitor
from storn.StornParser import StornParser

class CodeGenerator(StornVisitor):
    def __init__(self):
        self.instructions = []
        self.symbol_table = {}

    def visitProgram(self, ctx: StornParser.ProgramContext):
        print("PROGRAM")
        self.visitChildren(ctx)

    def visitDeclaration(self, ctx: StornParser.DeclarationContext):
        print("DECLARATION")
        self.visitChildren(ctx)

