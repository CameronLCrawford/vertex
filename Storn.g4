grammar Storn;

// Parser Rules

program
        : declaration* EOF
        ;

declaration
        : data
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

routine
        : 'routine' NAME '(' typedParamList ')' '->' type localVars statements
        ;

typedParamList
        : (typedVar (',' typedVar)*)?
        ;

localVars
        : (';' typeDeclaration+)?
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
        : 'set' lvalue '=' expression
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
        : 'if' expression statements
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
        : comparativeExpr (logicalOp comparativeExpr)*
        ;

logicalOp
        : OR
        | AND
        ;

comparativeExpr
        : additiveExpr (comparativeOp additiveExpr)*
        ;

comparativeOp
        : EQ
        | LT
        | GT
        | LEQ
        | GEQ
        ;

additiveExpr
        : multiplicativeExpr (additiveOp multiplicativeExpr)*
        ;

additiveOp
        : PLUS
        | MINUS
        ;

multiplicativeExpr
        : unaryExpr ('*' unaryExpr)*
        ;

unaryExpr
        : (MINUS | NOT | type)? primaryExpr
        ;

primaryExpr
        : '(' expression ')'
        | call
        | lvalue
        | CONSTANT ':' width
        ;

width
        : '8'
        | '16'
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

NAME
        : [a-zA-Z_][a-zA-Z0-9_]*
        ;

CONSTANT
        : [0-9]+
        ;

DEREFERENCE
        : '$'
        ;

OR
        : '|'
        ;

AND
        : '&'
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

// Whitespace and comments

WS
        : [ \t\r\n]+ -> skip
        ;

COMMENT
        : '\'' ~[\r\n]* -> skip
        ;

