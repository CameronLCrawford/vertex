grammar Vtx;

// Parser Rules

program
        : line* EOF
        ;

line
        : (label | instruction) EOL
        ;

label
        : NAME ':'
        ;

instruction
        : move
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
        | negate
        | jump
        | out
        | halt
        ;

source
        : REGISTER
        | CONSTANT
        | ADDRESS
        ;

destination
        : REGISTER
        ;

move
        : 'mov' destination source
        ;

push
        : 'psh' source
        ;

pop
        : 'pop' destination
        ;

add
        : 'add' source
        ;

sub
        : 'sub' source
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
        : 'inc'
        ;

decrement
        : 'dec'
        ;

shiftLeft
        : 'shl'
        ;

shiftRight
        : 'shr'
        ;

negate
        : 'neg'
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
        | 'h'
        | 'l'
        ;

ADDRESS
        : '@' CONSTANT
        ;

CONDITION
        : 'z'
        | 's'
        | 'c'
        | 'nz'
        | 'ns'
        | 'nc'
        ;

// Whitespace and comments

EOL
        : [\r\n]+
        ;

WS
        : [ \t\r\n]+ -> skip
        ;

COMMENT
        : '\'' ~[\r\n]* -> skip
        ;

