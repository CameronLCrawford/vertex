import sys
import argparse
from antlr4 import FileStream, InputStream, CommonTokenStream
from storn.StornLexer import StornLexer
from storn.StornParser import StornParser
from CodeGenerator import CodeGenerator, CompileError

def compile(source, is_file):
    input = FileStream(source) if is_file else InputStream(source)
    lexer = StornLexer(input)
    stream = CommonTokenStream(lexer)
    parser = StornParser(stream)
    tree = parser.program()
    if parser.getNumberOfSyntaxErrors() > 0:
        raise CompileError("Failed to parse")
    generator = CodeGenerator()
    generator.visit(tree)
    return generator.instructions

def main():
    parser = argparse.ArgumentParser(description="Storn Compiler")
    parser.add_argument("input", nargs="?", help="Source file (or stdin if omitted)")
    parser.add_argument("-o", "--output", help="Output file (or stdout if omitted)")
    args = parser.parse_args()

    try:
        if args.input:
            instructions = compile(args.input, True)
        else:
            source = sys.stdin.read()
            instructions = compile(source, False)

        output = open(args.output, "w") if args.output else sys.stdout
        for instruction in instructions:
            print(instruction, file=output)
        if args.output:
            output.close()
    except CompileError as error:
        print("Compilation failed with error:", file=sys.stderr)
        print(error, file=sys.stderr)
        sys.exit(1)
    except Exception as exception:
        print("Unexpected exception:", file=sys.stderr)
        raise exception

if __name__ == "__main__":
    main()
