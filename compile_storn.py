import sys
import argparse
import yaml

from antlr4 import FileStream, InputStream, CommonTokenStream

from storn.StornLexer import StornLexer
from storn.StornParser import StornParser
from CodeGenerator import CodeGenerator, CompileError

from vtx.VtxLexer import VtxLexer
from vtx.VtxParser import VtxParser
from Assembler import Assembler

def compile(source, is_file, start_address, imports, is_main):
    exports = {"globals": {}, "data": {}, "routines": {}}

    storn_input = FileStream(source) if is_file else InputStream(source)
    storn_lexer = StornLexer(storn_input)
    storn_stream = CommonTokenStream(storn_lexer)
    storn_parser = StornParser(storn_stream)
    storn_tree = storn_parser.program()
    if storn_parser.getNumberOfSyntaxErrors() > 0:
        raise CompileError("Failed to parse")
    generator = CodeGenerator(imports, exports, is_main)
    generator.visit(storn_tree)

    assembly = "\n".join(generator.instructions) + "\n"
    vtx_input = InputStream(assembly)
    vtx_lexer = VtxLexer(vtx_input)
    vtx_stream = CommonTokenStream(vtx_lexer)
    vtx_parser = VtxParser(vtx_stream)
    vtx_tree = vtx_parser.program()
    assembler = Assembler(imports, exports, start_address)
    assembler.visit(vtx_tree)

    return bytearray(assembler.instructions), assembly, exports

def main():
    parser = argparse.ArgumentParser(description="Storn Compiler")
    parser.add_argument("input", nargs="?", help="Source file (or stdin if omitted)")
    parser.add_argument("-o", "--output", help="Output file (or stdout if omitted)")
    parser.add_argument("-s", "--assembly", help="File to write assembly to (no assembly written if omitted)")
    parser.add_argument("-a", "--address", type=lambda x: int(x, 0), help="Address in memory to start program from. Used for label address resolution. Default (omission) places program at the end of memory")
    parser.add_argument("-i", "--imports", help="File to read import data from (no imports used if omitted)") # this is plural because `args.import` doesn't parse
    parser.add_argument("-e", "--export", help="File to write export data to (no exports generated if omitted)")
    args = parser.parse_args()

    try:
        if args.imports:
            with open(args.imports, "r") as import_file:
                imports = yaml.safe_load(import_file)
        else:
            imports = {"globals": {}, "data": {}, "routines": {}}

        if args.input:
            program, assembly, exports = compile(args.input, True, args.address, imports, args.imports is not None)
        else:
            source = sys.stdin.read()
            program, assembly, exports = compile(source, False, args.address, imports, args.imports is not None)

        if args.assembly:
            with open(args.assembly, "w") as assembly_file:
                assembly_file.write(assembly)

        if args.export:
            with open(args.export, "w") as export_file:
                yaml.dump(exports, export_file)

        if args.output:
            with open(args.output, "wb") as rom_file:
                rom_file.write(program)
        else:
            sys.stdout.buffer.write(program)
    except CompileError as error:
        print("Compilation failed with error:", file=sys.stderr)
        print(error, file=sys.stderr)
        sys.exit(1)
    except Exception as exception:
        print("Unexpected exception:", file=sys.stderr)
        raise exception

if __name__ == "__main__":
    main()
