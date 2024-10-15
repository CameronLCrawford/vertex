all:
	clang vertex.c -o out/vertex

debug-build:
	clang -g -O0 vertex.c -o debug/vertex

