import sys
from antlr4 import FileStream, CommonTokenStream
from vtx.VtxLexer import VtxLexer
from vtx.VtxParser import VtxParser
from Assembler import Assembler

def assemble(assembly_file, machine_code_file):
    input = FileStream(assembly_file)
    lexer = VtxLexer(input)
    stream = CommonTokenStream(lexer)
    parser = VtxParser(stream)
    tree = parser.program()
    assembler = Assembler()
    assembler.visit(tree)
    with open(machine_code_file, "w") as out_file:
        for instruction in assembler.instructions:
            out_file.write(f"{instruction}\n")

if __name__ == "__main__":
    assemble(sys.argv[1], sys.argv[2])
