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
        | ADDRESS
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
        | '@' NAME
        ;

CONDITION
        : 'z'
        | 'n'
        | 'c'
        | 'nz'
        | 'nn'
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

