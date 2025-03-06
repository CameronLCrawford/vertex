grammar Vtx;

// Parser Rules

program
        : line* EOF
        ;

line
        : (label | instruction)
        ;

label
        : NAME ':'
        ;

instruction
        : loadRegister
        | store
        | push
        | pop
        | add
        | sub
        | binaryAnd
        | binaryOr
        | binaryXor
        | binaryNot
        | increment
        | decrement
        | shiftLeft
        | shiftRight
        | jump
        | out
        | halt
        ;

source
        : REGISTER
        | CONSTANT
        | ADDRESS
        ;

loadRegister
        : 'ldr' REGISTER source
        ;

store
        : 'str' ADDRESS REGISTER
        ;

push
        : 'psh' source
        ;

pop
        : 'pop' REGISTER
        ;

add
        : 'add' CARRY? source
        ;

sub
        : 'sub' CARRY? source
        ;

binaryAnd
        : 'and' source
        ;

binaryOr
        : 'or' source
        ;

binaryXor
        : 'xor' source
        ;

binaryNot
        : 'not'
        ;

increment
        : 'inc' CARRY?
        ;

decrement
        : 'dec' CARRY?
        ;

shiftLeft
        : 'shl'
        ;

shiftRight
        : 'shr' CARRY?
        ;

jump
        : 'jmp' CONDITION? NAME
        ;

out
        : 'out'
        ;

halt
        : 'hlt'
        ;

// Lexer Rules

NAME
        : [A-Z_][A-Z0-9_]*
        ;

CONSTANT
        : [0-9]+
        ;

REGISTER
        : 'a'
        | 'b'
        | 'c'
        | 'h'
        | 'l'
        ;

ADDRESS
        : '@' CONSTANT
        ;

CONDITION
        : 'zf'
        | 'sf'
        | 'cf'
        | 'nzf'
        | 'nsf'
        | 'ncf'
        ;

CARRY
        : 'cc'
        ;

// Whitespace and comments

WS
        : [ \t\r\n]+ -> skip
        ;

COMMENT
        : '\'' ~[\r\n]* -> skip
        ;

