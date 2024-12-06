import sys
from antlr4 import FileStream, CommonTokenStream
from storn.StornLexer import StornLexer
from storn.StornParser import StornParser
from CodeGenerator import CodeGenerator

def compile(source_file, assembly_file):
    input = FileStream(source_file)
    lexer = StornLexer(input)
    stream = CommonTokenStream(lexer)
    parser = StornParser(stream)
    tree = parser.program()
    generator = CodeGenerator()
    generator.visit(tree)
    with open(assembly_file, "w") as out_file:
        for instruction in generator.instructions:
            out_file.write(f"{instruction}\n")

if __name__ == "__main__":
    compile(sys.argv[1], sys.argv[2])
