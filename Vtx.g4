grammar Vtx;

// Parser Rules

program
        : line* EOF
        ;

line
        : (label | instruction)
        ;

label
        : LABEL ':'
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
        | increment
        | decrement
        | shiftLeft
        | shiftRight
        | jump
        | call
        | interruptReturn
        | out
        | halt
        ;

source
        : REGISTER
        | CONSTANT
        | ADDRESS
        | M
        ;

loadRegister
        : 'ldr' REGISTER source
        ;

store
        : 'str' (ADDRESS | M) REGISTER
        ;

push
        : 'psh' (source | 's')
        ;

pop
        : 'pop' (REGISTER | 's')
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

increment
        : 'inc' CARRY?
        ;

decrement
        : 'dec' CARRY?
        ;

shiftLeft
        : 'shl' CARRY?
        ;

shiftRight
        : 'shr' CARRY?
        ;

jump
        : 'jmp' CONDITION? (LABEL | M)
        ;

call
        : 'cal' (LABEL | ADDRESS)
        ;

interruptReturn
        : 'irt'
        ;

out
        : 'out'
        ;

halt
        : 'hlt'
        ;

// Lexer Rules

REGISTER
        : 'a'
        | 'b'
        | 'c'
        | 'h'
        | 'l'
        | 'bph'
        | 'bpl'
        | 'sph'
        | 'spl'
        | 'cn'
        ;

M
        : 'm'
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

LABEL
        : [a-zA-Z_][a-zA-Z0-9_]*
        ;

CONSTANT
        : [0-9]+
        ;

ADDRESS
        : '@' CONSTANT
        ;

// Whitespace and comments

WS
        : [ \t\r\n]+ -> skip
        ;

COMMENT
        : '\'' ~[\r\n]* -> skip
        ;

