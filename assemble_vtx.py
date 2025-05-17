import sys
import argparse
from antlr4 import FileStream, InputStream, CommonTokenStream
from vtx.VtxLexer import VtxLexer
from vtx.VtxParser import VtxParser
from Assembler import Assembler

def assemble(source, is_file):
    input = FileStream(source) if is_file else InputStream(source)
    lexer = VtxLexer(input)
    stream = CommonTokenStream(lexer)
    parser = VtxParser(stream)
    tree = parser.program()
    assembler = Assembler()
    assembler.visit(tree)
    return bytearray(assembler.instructions)

def main():
    parser = argparse.ArgumentParser(description="Vtx Assembler")
    parser.add_argument("input", nargs="?", help="Source file (or stdin if omitted)")
    parser.add_argument("-o", "--output", help="Output file (or stdout if omitted)")
    args = parser.parse_args()

    if args.input:
        program = assemble(args.input, True)
    else:
        source = sys.stdin.read()
        program = assemble(source, False)
    if args.output:
        with open(args.output, "wb") as rom_file:
            rom_file.write(program)
    else:
        sys.stdout.buffer.write(program)

if __name__ == "__main__":
    main()
