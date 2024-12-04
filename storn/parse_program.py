import sys
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from StornLexer import StornLexer
from StornParser import StornParser
from StornListener import StornListener
from antlr4.tree.Trees import Trees

def main(argv):
    input = FileStream(argv[1])
    lexer = StornLexer(input)
    stream = CommonTokenStream(lexer)
    parser = StornParser(stream)
    tree = parser.program()

    print(Trees.toStringTree(tree, None, parser))

    storn = StornListener()
    walker = ParseTreeWalker()
    walker.walk(storn, tree)

if __name__ == "__main__":
    main(sys.argv)
