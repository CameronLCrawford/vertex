import sys
from antlr4 import FileStream, CommonTokenStream
from vtx.VtxLexer import VtxLexer
from vtx.VtxParser import VtxParser
from Assembler import Assembler

def assemble(assembly_file, rom_file):
    input = FileStream(assembly_file)
    lexer = VtxLexer(input)
    stream = CommonTokenStream(lexer)
    parser = VtxParser(stream)
    tree = parser.program()
    assembler = Assembler()
    assembler.visit(tree)
    rom_bytes = [0] * (2**16)
    rom_address = 2**15
    for instruction in assembler.instructions:
        rom_bytes[rom_address] = instruction
        rom_address += 1
    with open(rom_file, 'wb') as rom:
        rom.write(bytearray(rom_bytes))

if __name__ == "__main__":
    assemble(sys.argv[1], sys.argv[2])
