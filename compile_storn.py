import sys
from antlr4 import FileStream, CommonTokenStream
from storn.StornLexer import StornLexer
from storn.StornParser import StornParser
from CodeGenerator import CodeGenerator, CompileError

def compile(source_file, assembly_file):
    input = FileStream(source_file)
    lexer = StornLexer(input)
    stream = CommonTokenStream(lexer)
    parser = StornParser(stream)
    tree = parser.program()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("Failed to parse.")
        return
    generator = CodeGenerator()
    try:
        generator.visit(tree)
    except CompileError as error:
        print("Compilation failed with error:")
        print(error)
        return
    except Exception as exception:
        raise exception
    with open(assembly_file, "w") as out_file:
        for instruction in generator.instructions:
            out_file.write(f"{instruction}\n")

if __name__ == "__main__":
    compile(sys.argv[1], sys.argv[2])
