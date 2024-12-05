import sys
from antlr4 import FileStream, CommonTokenStream
from storn.StornLexer import StornLexer
from storn.StornParser import StornParser
from antlr4.tree.Trees import Trees

def main(argv):
    input = FileStream(argv[1])
    lexer = StornLexer(input)
    stream = CommonTokenStream(lexer)
    parser = StornParser(stream)
    tree = parser.program()

    print(Trees.toStringTree(tree, None, parser))

if __name__ == "__main__":
    main(sys.argv)
