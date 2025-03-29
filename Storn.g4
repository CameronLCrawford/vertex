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
        : comparativeExpr (('|' | '&') comparativeExpr)*
        ;

comparativeExpr
        : additiveExpr (comparativeOp additiveExpr)* 
        ;

additiveExpr
        : multiplicativeExpr (('+:' CONSTANT | '-:' CONSTANT) multiplicativeExpr)* 
        ;

multiplicativeExpr
        : unaryExpr ('*' unaryExpr)*
        ;

unaryExpr
        : ('-' | '~') unaryExpr
        | primaryExpr
        ;

primaryExpr
        : '(' expression ')'
        | call
        | arrayIndex
        | refValue
        | lvalue
        | NAME
        | CONSTANT
        ;

comparativeOp
        : '=' | '<' | '>' | '<=' | '>='
        ;

call
        : '!' NAME '(' callArgs ')'
        ;

callArgs
        : (expression (',' expression)*)?
        ;

arrayIndex
        : NAME '@' expression
        ;

refValue
        : '$' NAME
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

// Whitespace and comments

WS
        : [ \t\r\n]+ -> skip
        ;

COMMENT
        : '\'' ~[\r\n]* -> skip
        ;

