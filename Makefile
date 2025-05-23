all:
	clang vertex.c -o out/vertex

debug-build:
	clang -g -O0 vertex.c -o debug/vertex

storn-parser:
	java -Xmx500M -cp "/usr/local/lib/antlr-4.13.2-complete.jar:$CLASSPATH" org.antlr.v4.Tool -Dlanguage=Python3 -visitor -no-listener -o storn Storn.g4

vtx-parser:
	java -Xmx500M -cp "/usr/local/lib/antlr-4.13.2-complete.jar:$CLASSPATH" org.antlr.v4.Tool -Dlanguage=Python3 -visitor -no-listener -o vtx Vtx.g4
