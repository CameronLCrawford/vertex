import sys
from typing import Optional
from antlr4 import FileStream, CommonTokenStream
from vtx.VtxLexer import VtxLexer
from vtx.VtxParser import VtxParser
from Assembler import Assembler

def assemble(assembly_file: str, rom_file: str, debug_file: Optional[str]=None):
    input = FileStream(assembly_file)
    lexer = VtxLexer(input)
    stream = CommonTokenStream(lexer)
    parser = VtxParser(stream)
    tree = parser.program()
    assembler = Assembler()
    assembler.visit(tree)
    rom_bytes = []
    for instruction in assembler.instructions:
        rom_bytes.append(instruction)
    with open(rom_file, 'wb') as rom:
        rom.write(bytearray(rom_bytes))
    if debug_file:
        with open(debug_file, 'w') as debug:
            [debug.write(str(info) + "\n") for info in assembler.debug_info]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        assemble(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        assemble(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print(f"Invalid number of arguments. Expected 2 or 3 but got {len(sys.argv) - 1}.")
        print(sys.argv)
