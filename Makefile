all:
	clang vertex.c -o out/vertex

debug-build:
	clang -g -O0 vertex.c -o debug/vertex

parser:
	java -Xmx500M -cp "/usr/local/lib/antlr-4.13.2-complete.jar:$CLASSPATH" org.antlr.v4.Tool -Dlanguage=Python3 storn/Storn.g4

