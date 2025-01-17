from vtx.VtxVisitor import VtxVisitor
from vtx.VtxParser import VtxParser

class Assembler(VtxVisitor):
    def __init__(self):
        self.instructions = []
        self.symbol_table = {}

    def visitLabel(self, ctx:VtxParser.LabelContext):
        print("PROGRAM")
        self.visitChildren(ctx)

