grammar Storn;

// Parser Rules

program
        : declaration* EOF
        ;

declaration
        : data
        | global
        | routine
        ;

data
        : 'data' NAME '{' typeDeclaration* '}'
        ;

typeDeclaration
        : typedVar '.'
        ;

typedVar
        : NAME ':' type
        ;

global
        : 'global' typeDeclaration
        ;

routine
        : 'routine' NAME '(' typedParamList ')' '->' type localVars statements
        ;

typedParamList
        : (typedVar (',' typedVar)*)?
        ;

localVars
        : typeDeclaration*
        ;

statements
        : '{' statement* '}'
        ;

statement
        : setStmt '.'
        | ifStmt
        | loopStmt
        | breakStmt '.'
        | continueStmt '.'
        | call '.'
        | outputStmt '.'
        | returnStmt '.'
        ;

setStmt
        : lvalue '=' expression
        ;

lvalue
        : indexLvalue
        ;

indexLvalue
        : projectionLvalue ('@' expression)*
        ;

projectionLvalue
        : referenceLvalue ('/' NAME)*
        ;

referenceLvalue
        : DEREFERENCE? primaryLvalue
        ;

primaryLvalue
        : '(' lvalue ')'
        | NAME
        ;

ifStmt
        : 'if' expression statements elifStmt* elseStmt?
        ;

elifStmt
        : 'elif' expression statements
        ;

elseStmt
        : 'else' statements
        ;

loopStmt
        : 'loop' statements
        ;

breakStmt
        : 'break'
        ;

continueStmt
        : 'continue'
        ;

outputStmt
        : 'output' expression
        ;

returnStmt
        : 'return' expression?
        ;

expression
        : logicalExpr
        ;

logicalExpr
        : bitwiseExpr (logicalOp bitwiseExpr)*
        ;

logicalOp
        : AND
        | OR
        ;

bitwiseExpr
        : comparativeExpr (bitwiseOp comparativeExpr)*
        ;

bitwiseOp
        : DIS
        | CON
        | XOR
        ;

comparativeExpr
        : arithmeticExpr (comparativeOp arithmeticExpr)*
        ;

comparativeOp
        : EQ
        | LT
        | GT
        | LEQ
        | GEQ
        ;

arithmeticExpr
        : shiftExpr (arithmeticOp shiftExpr)*
        ;

arithmeticOp
        : PLUS
        | MINUS
        ;

shiftExpr
        : multiplicativeExpr (shiftOp multiplicativeExpr)*
        ;

shiftOp
        : SHR
        | SHL
        ;

multiplicativeExpr
        : unaryExpr ('*' unaryExpr)*
        ;

unaryExpr
        : (MINUS | NOT | type) unaryExpr
        | primaryExpr
        ;

primaryExpr
        : '(' expression ')'
        | call
        | lvalue
        | CONSTANT ':' CONSTANT
        | '#' type
        | STRING
        | CHARACTER
        ;

call
        : '!' NAME '(' parameters ')'
        ;

parameters
        : (expression (',' expression)*)?
        ;

type
        : '[0]' | '[8]' | '[16]' | '[' NAME ']'
        | '<' type '>'
        | type '^' CONSTANT
        ;

// Lexer Rules

AND
        : 'and'
        ;

OR
        : 'or'
        ;

NAME
        : [a-zA-Z_][a-zA-Z0-9_]*
        ;

CHARACTER
        : '\'' ~['\r\n] '\''
        ;

STRING
        : '"' ~['\r\n]+ '"'
        ;


CONSTANT
        : [0-9]+
        ;

DEREFERENCE
        : '$'
        ;

DIS
        : '|'
        ;

CON
        : '&'
        ;

XOR
        : '^'
        ;

EQ
        : '='
        ;

LT
        : '<'
        ;

GT
        : '>'
        ;

LEQ
        : '<='
        ;

GEQ
        : '>='
        ;

PLUS
        : '+'
        ;

MINUS
        : '-'
        ;

NOT
        : '~'
        ;

SHR
        : '>>'
        ;

SHL
        : '<<'
        ;

// Whitespace and comments

WS
        : [ \t\r\n]+ -> skip
        ;

COMMENT
        : ';' ~[\r\n]* -> skip
        ;

