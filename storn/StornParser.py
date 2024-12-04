# Generated from storn/Storn.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,43,282,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,1,0,5,0,62,8,0,10,0,12,0,65,9,0,1,
        0,1,0,1,1,1,1,3,1,71,8,1,1,2,1,2,1,2,1,2,5,2,77,8,2,10,2,12,2,80,
        9,2,1,2,1,2,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,
        1,5,1,5,1,5,1,6,1,6,1,6,5,6,103,8,6,10,6,12,6,106,9,6,3,6,108,8,
        6,1,7,1,7,5,7,112,8,7,10,7,12,7,115,9,7,1,7,1,7,1,8,1,8,1,8,1,8,
        1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,3,8,136,8,8,
        1,9,1,9,1,9,1,10,1,10,1,10,1,10,1,10,1,11,1,11,1,11,1,11,3,11,150,
        8,11,1,11,1,11,1,11,1,11,1,11,1,11,5,11,158,8,11,10,11,12,11,161,
        9,11,1,12,1,12,1,12,1,12,1,13,1,13,1,13,1,14,1,14,1,15,1,15,1,15,
        1,16,1,16,3,16,177,8,16,1,17,1,17,1,18,1,18,1,18,5,18,184,8,18,10,
        18,12,18,187,9,18,1,19,1,19,1,19,1,19,5,19,193,8,19,10,19,12,19,
        196,9,19,1,20,1,20,1,20,1,20,1,20,3,20,203,8,20,1,20,5,20,206,8,
        20,10,20,12,20,209,9,20,1,21,1,21,1,21,5,21,214,8,21,10,21,12,21,
        217,9,21,1,22,1,22,1,22,3,22,222,8,22,1,23,1,23,1,23,1,23,1,23,1,
        23,1,23,1,23,1,23,1,23,3,23,234,8,23,1,24,1,24,1,25,1,25,1,25,1,
        25,1,25,1,25,1,26,1,26,1,26,5,26,247,8,26,10,26,12,26,250,9,26,3,
        26,252,8,26,1,27,1,27,1,27,1,27,1,28,1,28,1,28,1,29,1,29,1,29,1,
        29,1,29,1,29,1,29,1,29,1,29,1,29,1,29,3,29,272,8,29,1,29,1,29,1,
        29,5,29,277,8,29,10,29,12,29,280,9,29,1,29,0,2,22,58,30,0,2,4,6,
        8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,
        52,54,56,58,0,3,1,0,22,23,1,0,27,28,2,0,13,13,29,32,286,0,63,1,0,
        0,0,2,70,1,0,0,0,4,72,1,0,0,0,6,83,1,0,0,0,8,86,1,0,0,0,10,90,1,
        0,0,0,12,107,1,0,0,0,14,109,1,0,0,0,16,135,1,0,0,0,18,137,1,0,0,
        0,20,140,1,0,0,0,22,149,1,0,0,0,24,162,1,0,0,0,26,166,1,0,0,0,28,
        169,1,0,0,0,30,171,1,0,0,0,32,174,1,0,0,0,34,178,1,0,0,0,36,180,
        1,0,0,0,38,188,1,0,0,0,40,197,1,0,0,0,42,210,1,0,0,0,44,221,1,0,
        0,0,46,233,1,0,0,0,48,235,1,0,0,0,50,237,1,0,0,0,52,251,1,0,0,0,
        54,253,1,0,0,0,56,257,1,0,0,0,58,271,1,0,0,0,60,62,3,2,1,0,61,60,
        1,0,0,0,62,65,1,0,0,0,63,61,1,0,0,0,63,64,1,0,0,0,64,66,1,0,0,0,
        65,63,1,0,0,0,66,67,5,0,0,1,67,1,1,0,0,0,68,71,3,4,2,0,69,71,3,10,
        5,0,70,68,1,0,0,0,70,69,1,0,0,0,71,3,1,0,0,0,72,73,5,1,0,0,73,74,
        5,40,0,0,74,78,5,2,0,0,75,77,3,6,3,0,76,75,1,0,0,0,77,80,1,0,0,0,
        78,76,1,0,0,0,78,79,1,0,0,0,79,81,1,0,0,0,80,78,1,0,0,0,81,82,5,
        3,0,0,82,5,1,0,0,0,83,84,3,8,4,0,84,85,5,4,0,0,85,7,1,0,0,0,86,87,
        5,40,0,0,87,88,5,5,0,0,88,89,3,58,29,0,89,9,1,0,0,0,90,91,5,6,0,
        0,91,92,5,40,0,0,92,93,5,7,0,0,93,94,3,12,6,0,94,95,5,8,0,0,95,96,
        5,9,0,0,96,97,3,58,29,0,97,98,3,14,7,0,98,11,1,0,0,0,99,104,3,8,
        4,0,100,101,5,10,0,0,101,103,3,8,4,0,102,100,1,0,0,0,103,106,1,0,
        0,0,104,102,1,0,0,0,104,105,1,0,0,0,105,108,1,0,0,0,106,104,1,0,
        0,0,107,99,1,0,0,0,107,108,1,0,0,0,108,13,1,0,0,0,109,113,5,2,0,
        0,110,112,3,16,8,0,111,110,1,0,0,0,112,115,1,0,0,0,113,111,1,0,0,
        0,113,114,1,0,0,0,114,116,1,0,0,0,115,113,1,0,0,0,116,117,5,3,0,
        0,117,15,1,0,0,0,118,119,3,18,9,0,119,120,5,4,0,0,120,136,1,0,0,
        0,121,122,3,20,10,0,122,123,5,4,0,0,123,136,1,0,0,0,124,136,3,24,
        12,0,125,136,3,26,13,0,126,127,3,28,14,0,127,128,5,4,0,0,128,136,
        1,0,0,0,129,130,3,30,15,0,130,131,5,4,0,0,131,136,1,0,0,0,132,133,
        3,32,16,0,133,134,5,4,0,0,134,136,1,0,0,0,135,118,1,0,0,0,135,121,
        1,0,0,0,135,124,1,0,0,0,135,125,1,0,0,0,135,126,1,0,0,0,135,129,
        1,0,0,0,135,132,1,0,0,0,136,17,1,0,0,0,137,138,5,11,0,0,138,139,
        3,8,4,0,139,19,1,0,0,0,140,141,5,12,0,0,141,142,3,22,11,0,142,143,
        5,13,0,0,143,144,3,34,17,0,144,21,1,0,0,0,145,146,6,11,-1,0,146,
        150,5,40,0,0,147,148,5,14,0,0,148,150,3,22,11,3,149,145,1,0,0,0,
        149,147,1,0,0,0,150,159,1,0,0,0,151,152,10,2,0,0,152,153,5,15,0,
        0,153,158,3,34,17,0,154,155,10,1,0,0,155,156,5,16,0,0,156,158,3,
        34,17,0,157,151,1,0,0,0,157,154,1,0,0,0,158,161,1,0,0,0,159,157,
        1,0,0,0,159,160,1,0,0,0,160,23,1,0,0,0,161,159,1,0,0,0,162,163,5,
        17,0,0,163,164,3,34,17,0,164,165,3,14,7,0,165,25,1,0,0,0,166,167,
        5,18,0,0,167,168,3,14,7,0,168,27,1,0,0,0,169,170,5,19,0,0,170,29,
        1,0,0,0,171,172,5,20,0,0,172,173,3,34,17,0,173,31,1,0,0,0,174,176,
        5,21,0,0,175,177,3,34,17,0,176,175,1,0,0,0,176,177,1,0,0,0,177,33,
        1,0,0,0,178,179,3,36,18,0,179,35,1,0,0,0,180,185,3,38,19,0,181,182,
        7,0,0,0,182,184,3,38,19,0,183,181,1,0,0,0,184,187,1,0,0,0,185,183,
        1,0,0,0,185,186,1,0,0,0,186,37,1,0,0,0,187,185,1,0,0,0,188,194,3,
        40,20,0,189,190,3,48,24,0,190,191,3,40,20,0,191,193,1,0,0,0,192,
        189,1,0,0,0,193,196,1,0,0,0,194,192,1,0,0,0,194,195,1,0,0,0,195,
        39,1,0,0,0,196,194,1,0,0,0,197,207,3,42,21,0,198,199,5,24,0,0,199,
        203,5,41,0,0,200,201,5,25,0,0,201,203,5,41,0,0,202,198,1,0,0,0,202,
        200,1,0,0,0,203,204,1,0,0,0,204,206,3,42,21,0,205,202,1,0,0,0,206,
        209,1,0,0,0,207,205,1,0,0,0,207,208,1,0,0,0,208,41,1,0,0,0,209,207,
        1,0,0,0,210,215,3,44,22,0,211,212,5,26,0,0,212,214,3,44,22,0,213,
        211,1,0,0,0,214,217,1,0,0,0,215,213,1,0,0,0,215,216,1,0,0,0,216,
        43,1,0,0,0,217,215,1,0,0,0,218,219,7,1,0,0,219,222,3,44,22,0,220,
        222,3,46,23,0,221,218,1,0,0,0,221,220,1,0,0,0,222,45,1,0,0,0,223,
        224,5,7,0,0,224,225,3,34,17,0,225,226,5,8,0,0,226,234,1,0,0,0,227,
        234,3,50,25,0,228,234,3,54,27,0,229,234,3,56,28,0,230,234,3,22,11,
        0,231,234,5,40,0,0,232,234,5,41,0,0,233,223,1,0,0,0,233,227,1,0,
        0,0,233,228,1,0,0,0,233,229,1,0,0,0,233,230,1,0,0,0,233,231,1,0,
        0,0,233,232,1,0,0,0,234,47,1,0,0,0,235,236,7,2,0,0,236,49,1,0,0,
        0,237,238,5,33,0,0,238,239,5,40,0,0,239,240,5,7,0,0,240,241,3,52,
        26,0,241,242,5,8,0,0,242,51,1,0,0,0,243,248,3,34,17,0,244,245,5,
        10,0,0,245,247,3,34,17,0,246,244,1,0,0,0,247,250,1,0,0,0,248,246,
        1,0,0,0,248,249,1,0,0,0,249,252,1,0,0,0,250,248,1,0,0,0,251,243,
        1,0,0,0,251,252,1,0,0,0,252,53,1,0,0,0,253,254,5,40,0,0,254,255,
        5,16,0,0,255,256,3,34,17,0,256,55,1,0,0,0,257,258,5,14,0,0,258,259,
        5,40,0,0,259,57,1,0,0,0,260,261,6,29,-1,0,261,272,5,34,0,0,262,272,
        5,35,0,0,263,272,5,36,0,0,264,265,5,37,0,0,265,266,5,40,0,0,266,
        272,5,38,0,0,267,268,5,29,0,0,268,269,3,58,29,0,269,270,5,30,0,0,
        270,272,1,0,0,0,271,260,1,0,0,0,271,262,1,0,0,0,271,263,1,0,0,0,
        271,264,1,0,0,0,271,267,1,0,0,0,272,278,1,0,0,0,273,274,10,1,0,0,
        274,275,5,39,0,0,275,277,5,41,0,0,276,273,1,0,0,0,277,280,1,0,0,
        0,278,276,1,0,0,0,278,279,1,0,0,0,279,59,1,0,0,0,280,278,1,0,0,0,
        22,63,70,78,104,107,113,135,149,157,159,176,185,194,202,207,215,
        221,233,248,251,271,278
    ]

class StornParser ( Parser ):

    grammarFileName = "Storn.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'data'", "'{'", "'}'", "'.'", "':'", 
                     "'routine'", "'('", "')'", "'->'", "','", "'init'", 
                     "'set'", "'='", "'$'", "'/'", "'@'", "'if'", "'loop'", 
                     "'break'", "'output'", "'return'", "'+'", "'&'", "'+:'", 
                     "'-:'", "'*'", "'-'", "'~'", "'<'", "'>'", "'<='", 
                     "'>='", "'!'", "'[0]'", "'[8]'", "'[16]'", "'['", "']'", 
                     "'^'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "NAME", "CONSTANT", "WS", "COMMENT" ]

    RULE_program = 0
    RULE_declaration = 1
    RULE_data = 2
    RULE_typeDeclaration = 3
    RULE_typedVar = 4
    RULE_routine = 5
    RULE_typedParamList = 6
    RULE_statements = 7
    RULE_statement = 8
    RULE_initStmt = 9
    RULE_setStmt = 10
    RULE_lvalue = 11
    RULE_ifStmt = 12
    RULE_loopStmt = 13
    RULE_breakStmt = 14
    RULE_outputStmt = 15
    RULE_returnStmt = 16
    RULE_expression = 17
    RULE_logicalExpr = 18
    RULE_comparativeExpr = 19
    RULE_additiveExpr = 20
    RULE_multiplicativeExpr = 21
    RULE_unaryExpr = 22
    RULE_primaryExpr = 23
    RULE_comparativeOp = 24
    RULE_call = 25
    RULE_callArgs = 26
    RULE_arrayIndex = 27
    RULE_refValue = 28
    RULE_type = 29

    ruleNames =  [ "program", "declaration", "data", "typeDeclaration", 
                   "typedVar", "routine", "typedParamList", "statements", 
                   "statement", "initStmt", "setStmt", "lvalue", "ifStmt", 
                   "loopStmt", "breakStmt", "outputStmt", "returnStmt", 
                   "expression", "logicalExpr", "comparativeExpr", "additiveExpr", 
                   "multiplicativeExpr", "unaryExpr", "primaryExpr", "comparativeOp", 
                   "call", "callArgs", "arrayIndex", "refValue", "type" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    T__31=32
    T__32=33
    T__33=34
    T__34=35
    T__35=36
    T__36=37
    T__37=38
    T__38=39
    NAME=40
    CONSTANT=41
    WS=42
    COMMENT=43

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(StornParser.EOF, 0)

        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StornParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(StornParser.DeclarationContext,i)


        def getRuleIndex(self):
            return StornParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = StornParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1 or _la==6:
                self.state = 60
                self.declaration()
                self.state = 65
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 66
            self.match(StornParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def data(self):
            return self.getTypedRuleContext(StornParser.DataContext,0)


        def routine(self):
            return self.getTypedRuleContext(StornParser.RoutineContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)




    def declaration(self):

        localctx = StornParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_declaration)
        try:
            self.state = 70
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 68
                self.data()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 69
                self.routine()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DataContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(StornParser.NAME, 0)

        def typeDeclaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StornParser.TypeDeclarationContext)
            else:
                return self.getTypedRuleContext(StornParser.TypeDeclarationContext,i)


        def getRuleIndex(self):
            return StornParser.RULE_data

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterData" ):
                listener.enterData(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitData" ):
                listener.exitData(self)




    def data(self):

        localctx = StornParser.DataContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_data)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.match(StornParser.T__0)
            self.state = 73
            self.match(StornParser.NAME)
            self.state = 74
            self.match(StornParser.T__1)
            self.state = 78
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 75
                self.typeDeclaration()
                self.state = 80
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 81
            self.match(StornParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typedVar(self):
            return self.getTypedRuleContext(StornParser.TypedVarContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_typeDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeDeclaration" ):
                listener.enterTypeDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeDeclaration" ):
                listener.exitTypeDeclaration(self)




    def typeDeclaration(self):

        localctx = StornParser.TypeDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_typeDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            self.typedVar()
            self.state = 84
            self.match(StornParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypedVarContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(StornParser.NAME, 0)

        def type_(self):
            return self.getTypedRuleContext(StornParser.TypeContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_typedVar

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypedVar" ):
                listener.enterTypedVar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypedVar" ):
                listener.exitTypedVar(self)




    def typedVar(self):

        localctx = StornParser.TypedVarContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_typedVar)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.match(StornParser.NAME)
            self.state = 87
            self.match(StornParser.T__4)
            self.state = 88
            self.type_(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RoutineContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(StornParser.NAME, 0)

        def typedParamList(self):
            return self.getTypedRuleContext(StornParser.TypedParamListContext,0)


        def type_(self):
            return self.getTypedRuleContext(StornParser.TypeContext,0)


        def statements(self):
            return self.getTypedRuleContext(StornParser.StatementsContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_routine

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoutine" ):
                listener.enterRoutine(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoutine" ):
                listener.exitRoutine(self)




    def routine(self):

        localctx = StornParser.RoutineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_routine)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self.match(StornParser.T__5)
            self.state = 91
            self.match(StornParser.NAME)
            self.state = 92
            self.match(StornParser.T__6)
            self.state = 93
            self.typedParamList()
            self.state = 94
            self.match(StornParser.T__7)
            self.state = 95
            self.match(StornParser.T__8)
            self.state = 96
            self.type_(0)
            self.state = 97
            self.statements()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypedParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typedVar(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StornParser.TypedVarContext)
            else:
                return self.getTypedRuleContext(StornParser.TypedVarContext,i)


        def getRuleIndex(self):
            return StornParser.RULE_typedParamList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypedParamList" ):
                listener.enterTypedParamList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypedParamList" ):
                listener.exitTypedParamList(self)




    def typedParamList(self):

        localctx = StornParser.TypedParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_typedParamList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==40:
                self.state = 99
                self.typedVar()
                self.state = 104
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==10:
                    self.state = 100
                    self.match(StornParser.T__9)
                    self.state = 101
                    self.typedVar()
                    self.state = 106
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StornParser.StatementContext)
            else:
                return self.getTypedRuleContext(StornParser.StatementContext,i)


        def getRuleIndex(self):
            return StornParser.RULE_statements

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatements" ):
                listener.enterStatements(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatements" ):
                listener.exitStatements(self)




    def statements(self):

        localctx = StornParser.StatementsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_statements)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 109
            self.match(StornParser.T__1)
            self.state = 113
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 4069376) != 0):
                self.state = 110
                self.statement()
                self.state = 115
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 116
            self.match(StornParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def initStmt(self):
            return self.getTypedRuleContext(StornParser.InitStmtContext,0)


        def setStmt(self):
            return self.getTypedRuleContext(StornParser.SetStmtContext,0)


        def ifStmt(self):
            return self.getTypedRuleContext(StornParser.IfStmtContext,0)


        def loopStmt(self):
            return self.getTypedRuleContext(StornParser.LoopStmtContext,0)


        def breakStmt(self):
            return self.getTypedRuleContext(StornParser.BreakStmtContext,0)


        def outputStmt(self):
            return self.getTypedRuleContext(StornParser.OutputStmtContext,0)


        def returnStmt(self):
            return self.getTypedRuleContext(StornParser.ReturnStmtContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)




    def statement(self):

        localctx = StornParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_statement)
        try:
            self.state = 135
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                self.enterOuterAlt(localctx, 1)
                self.state = 118
                self.initStmt()
                self.state = 119
                self.match(StornParser.T__3)
                pass
            elif token in [12]:
                self.enterOuterAlt(localctx, 2)
                self.state = 121
                self.setStmt()
                self.state = 122
                self.match(StornParser.T__3)
                pass
            elif token in [17]:
                self.enterOuterAlt(localctx, 3)
                self.state = 124
                self.ifStmt()
                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 4)
                self.state = 125
                self.loopStmt()
                pass
            elif token in [19]:
                self.enterOuterAlt(localctx, 5)
                self.state = 126
                self.breakStmt()
                self.state = 127
                self.match(StornParser.T__3)
                pass
            elif token in [20]:
                self.enterOuterAlt(localctx, 6)
                self.state = 129
                self.outputStmt()
                self.state = 130
                self.match(StornParser.T__3)
                pass
            elif token in [21]:
                self.enterOuterAlt(localctx, 7)
                self.state = 132
                self.returnStmt()
                self.state = 133
                self.match(StornParser.T__3)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InitStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typedVar(self):
            return self.getTypedRuleContext(StornParser.TypedVarContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_initStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInitStmt" ):
                listener.enterInitStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInitStmt" ):
                listener.exitInitStmt(self)




    def initStmt(self):

        localctx = StornParser.InitStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_initStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137
            self.match(StornParser.T__10)
            self.state = 138
            self.typedVar()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SetStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lvalue(self):
            return self.getTypedRuleContext(StornParser.LvalueContext,0)


        def expression(self):
            return self.getTypedRuleContext(StornParser.ExpressionContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_setStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetStmt" ):
                listener.enterSetStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetStmt" ):
                listener.exitSetStmt(self)




    def setStmt(self):

        localctx = StornParser.SetStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_setStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            self.match(StornParser.T__11)
            self.state = 141
            self.lvalue(0)
            self.state = 142
            self.match(StornParser.T__12)
            self.state = 143
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LvalueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(StornParser.NAME, 0)

        def lvalue(self):
            return self.getTypedRuleContext(StornParser.LvalueContext,0)


        def expression(self):
            return self.getTypedRuleContext(StornParser.ExpressionContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_lvalue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLvalue" ):
                listener.enterLvalue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLvalue" ):
                listener.exitLvalue(self)



    def lvalue(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = StornParser.LvalueContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 22
        self.enterRecursionRule(localctx, 22, self.RULE_lvalue, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 149
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [40]:
                self.state = 146
                self.match(StornParser.NAME)
                pass
            elif token in [14]:
                self.state = 147
                self.match(StornParser.T__13)
                self.state = 148
                self.lvalue(3)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 159
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,9,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 157
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
                    if la_ == 1:
                        localctx = StornParser.LvalueContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_lvalue)
                        self.state = 151
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 152
                        self.match(StornParser.T__14)
                        self.state = 153
                        self.expression()
                        pass

                    elif la_ == 2:
                        localctx = StornParser.LvalueContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_lvalue)
                        self.state = 154
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 155
                        self.match(StornParser.T__15)
                        self.state = 156
                        self.expression()
                        pass

             
                self.state = 161
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,9,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(StornParser.ExpressionContext,0)


        def statements(self):
            return self.getTypedRuleContext(StornParser.StatementsContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_ifStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStmt" ):
                listener.enterIfStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStmt" ):
                listener.exitIfStmt(self)




    def ifStmt(self):

        localctx = StornParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_ifStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 162
            self.match(StornParser.T__16)
            self.state = 163
            self.expression()
            self.state = 164
            self.statements()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LoopStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statements(self):
            return self.getTypedRuleContext(StornParser.StatementsContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_loopStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLoopStmt" ):
                listener.enterLoopStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLoopStmt" ):
                listener.exitLoopStmt(self)




    def loopStmt(self):

        localctx = StornParser.LoopStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_loopStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 166
            self.match(StornParser.T__17)
            self.state = 167
            self.statements()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BreakStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return StornParser.RULE_breakStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBreakStmt" ):
                listener.enterBreakStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBreakStmt" ):
                listener.exitBreakStmt(self)




    def breakStmt(self):

        localctx = StornParser.BreakStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_breakStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 169
            self.match(StornParser.T__18)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OutputStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(StornParser.ExpressionContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_outputStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOutputStmt" ):
                listener.enterOutputStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOutputStmt" ):
                listener.exitOutputStmt(self)




    def outputStmt(self):

        localctx = StornParser.OutputStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_outputStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 171
            self.match(StornParser.T__19)
            self.state = 172
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(StornParser.ExpressionContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_returnStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStmt" ):
                listener.enterReturnStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStmt" ):
                listener.exitReturnStmt(self)




    def returnStmt(self):

        localctx = StornParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_returnStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 174
            self.match(StornParser.T__20)
            self.state = 176
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3307527487616) != 0):
                self.state = 175
                self.expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalExpr(self):
            return self.getTypedRuleContext(StornParser.LogicalExprContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)




    def expression(self):

        localctx = StornParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 178
            self.logicalExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogicalExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def comparativeExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StornParser.ComparativeExprContext)
            else:
                return self.getTypedRuleContext(StornParser.ComparativeExprContext,i)


        def getRuleIndex(self):
            return StornParser.RULE_logicalExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogicalExpr" ):
                listener.enterLogicalExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogicalExpr" ):
                listener.exitLogicalExpr(self)




    def logicalExpr(self):

        localctx = StornParser.LogicalExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_logicalExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 180
            self.comparativeExpr()
            self.state = 185
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 181
                    _la = self._input.LA(1)
                    if not(_la==22 or _la==23):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 182
                    self.comparativeExpr() 
                self.state = 187
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparativeExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def additiveExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StornParser.AdditiveExprContext)
            else:
                return self.getTypedRuleContext(StornParser.AdditiveExprContext,i)


        def comparativeOp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StornParser.ComparativeOpContext)
            else:
                return self.getTypedRuleContext(StornParser.ComparativeOpContext,i)


        def getRuleIndex(self):
            return StornParser.RULE_comparativeExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparativeExpr" ):
                listener.enterComparativeExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparativeExpr" ):
                listener.exitComparativeExpr(self)




    def comparativeExpr(self):

        localctx = StornParser.ComparativeExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_comparativeExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 188
            self.additiveExpr()
            self.state = 194
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 189
                    self.comparativeOp()
                    self.state = 190
                    self.additiveExpr() 
                self.state = 196
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditiveExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multiplicativeExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StornParser.MultiplicativeExprContext)
            else:
                return self.getTypedRuleContext(StornParser.MultiplicativeExprContext,i)


        def CONSTANT(self, i:int=None):
            if i is None:
                return self.getTokens(StornParser.CONSTANT)
            else:
                return self.getToken(StornParser.CONSTANT, i)

        def getRuleIndex(self):
            return StornParser.RULE_additiveExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditiveExpr" ):
                listener.enterAdditiveExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditiveExpr" ):
                listener.exitAdditiveExpr(self)




    def additiveExpr(self):

        localctx = StornParser.AdditiveExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_additiveExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 197
            self.multiplicativeExpr()
            self.state = 207
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,14,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 202
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [24]:
                        self.state = 198
                        self.match(StornParser.T__23)
                        self.state = 199
                        self.match(StornParser.CONSTANT)
                        pass
                    elif token in [25]:
                        self.state = 200
                        self.match(StornParser.T__24)
                        self.state = 201
                        self.match(StornParser.CONSTANT)
                        pass
                    else:
                        raise NoViableAltException(self)

                    self.state = 204
                    self.multiplicativeExpr() 
                self.state = 209
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,14,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicativeExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StornParser.UnaryExprContext)
            else:
                return self.getTypedRuleContext(StornParser.UnaryExprContext,i)


        def getRuleIndex(self):
            return StornParser.RULE_multiplicativeExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeExpr" ):
                listener.enterMultiplicativeExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeExpr" ):
                listener.exitMultiplicativeExpr(self)




    def multiplicativeExpr(self):

        localctx = StornParser.MultiplicativeExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_multiplicativeExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 210
            self.unaryExpr()
            self.state = 215
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,15,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 211
                    self.match(StornParser.T__25)
                    self.state = 212
                    self.unaryExpr() 
                self.state = 217
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,15,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryExpr(self):
            return self.getTypedRuleContext(StornParser.UnaryExprContext,0)


        def primaryExpr(self):
            return self.getTypedRuleContext(StornParser.PrimaryExprContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_unaryExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryExpr" ):
                listener.enterUnaryExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryExpr" ):
                listener.exitUnaryExpr(self)




    def unaryExpr(self):

        localctx = StornParser.UnaryExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_unaryExpr)
        self._la = 0 # Token type
        try:
            self.state = 221
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [27, 28]:
                self.enterOuterAlt(localctx, 1)
                self.state = 218
                _la = self._input.LA(1)
                if not(_la==27 or _la==28):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 219
                self.unaryExpr()
                pass
            elif token in [7, 14, 33, 40, 41]:
                self.enterOuterAlt(localctx, 2)
                self.state = 220
                self.primaryExpr()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(StornParser.ExpressionContext,0)


        def call(self):
            return self.getTypedRuleContext(StornParser.CallContext,0)


        def arrayIndex(self):
            return self.getTypedRuleContext(StornParser.ArrayIndexContext,0)


        def refValue(self):
            return self.getTypedRuleContext(StornParser.RefValueContext,0)


        def lvalue(self):
            return self.getTypedRuleContext(StornParser.LvalueContext,0)


        def NAME(self):
            return self.getToken(StornParser.NAME, 0)

        def CONSTANT(self):
            return self.getToken(StornParser.CONSTANT, 0)

        def getRuleIndex(self):
            return StornParser.RULE_primaryExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimaryExpr" ):
                listener.enterPrimaryExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimaryExpr" ):
                listener.exitPrimaryExpr(self)




    def primaryExpr(self):

        localctx = StornParser.PrimaryExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_primaryExpr)
        try:
            self.state = 233
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 223
                self.match(StornParser.T__6)
                self.state = 224
                self.expression()
                self.state = 225
                self.match(StornParser.T__7)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 227
                self.call()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 228
                self.arrayIndex()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 229
                self.refValue()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 230
                self.lvalue(0)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 231
                self.match(StornParser.NAME)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 232
                self.match(StornParser.CONSTANT)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparativeOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return StornParser.RULE_comparativeOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparativeOp" ):
                listener.enterComparativeOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparativeOp" ):
                listener.exitComparativeOp(self)




    def comparativeOp(self):

        localctx = StornParser.ComparativeOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_comparativeOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 235
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8053071872) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(StornParser.NAME, 0)

        def callArgs(self):
            return self.getTypedRuleContext(StornParser.CallArgsContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_call

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCall" ):
                listener.enterCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCall" ):
                listener.exitCall(self)




    def call(self):

        localctx = StornParser.CallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_call)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 237
            self.match(StornParser.T__32)
            self.state = 238
            self.match(StornParser.NAME)
            self.state = 239
            self.match(StornParser.T__6)
            self.state = 240
            self.callArgs()
            self.state = 241
            self.match(StornParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CallArgsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StornParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(StornParser.ExpressionContext,i)


        def getRuleIndex(self):
            return StornParser.RULE_callArgs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCallArgs" ):
                listener.enterCallArgs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCallArgs" ):
                listener.exitCallArgs(self)




    def callArgs(self):

        localctx = StornParser.CallArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_callArgs)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 251
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3307527487616) != 0):
                self.state = 243
                self.expression()
                self.state = 248
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==10:
                    self.state = 244
                    self.match(StornParser.T__9)
                    self.state = 245
                    self.expression()
                    self.state = 250
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayIndexContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(StornParser.NAME, 0)

        def expression(self):
            return self.getTypedRuleContext(StornParser.ExpressionContext,0)


        def getRuleIndex(self):
            return StornParser.RULE_arrayIndex

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayIndex" ):
                listener.enterArrayIndex(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayIndex" ):
                listener.exitArrayIndex(self)




    def arrayIndex(self):

        localctx = StornParser.ArrayIndexContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_arrayIndex)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 253
            self.match(StornParser.NAME)
            self.state = 254
            self.match(StornParser.T__15)
            self.state = 255
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RefValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(StornParser.NAME, 0)

        def getRuleIndex(self):
            return StornParser.RULE_refValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRefValue" ):
                listener.enterRefValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRefValue" ):
                listener.exitRefValue(self)




    def refValue(self):

        localctx = StornParser.RefValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_refValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 257
            self.match(StornParser.T__13)
            self.state = 258
            self.match(StornParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(StornParser.NAME, 0)

        def type_(self):
            return self.getTypedRuleContext(StornParser.TypeContext,0)


        def CONSTANT(self):
            return self.getToken(StornParser.CONSTANT, 0)

        def getRuleIndex(self):
            return StornParser.RULE_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType" ):
                listener.enterType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType" ):
                listener.exitType(self)



    def type_(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = StornParser.TypeContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 58
        self.enterRecursionRule(localctx, 58, self.RULE_type, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 271
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [34]:
                self.state = 261
                self.match(StornParser.T__33)
                pass
            elif token in [35]:
                self.state = 262
                self.match(StornParser.T__34)
                pass
            elif token in [36]:
                self.state = 263
                self.match(StornParser.T__35)
                pass
            elif token in [37]:
                self.state = 264
                self.match(StornParser.T__36)
                self.state = 265
                self.match(StornParser.NAME)
                self.state = 266
                self.match(StornParser.T__37)
                pass
            elif token in [29]:
                self.state = 267
                self.match(StornParser.T__28)
                self.state = 268
                self.type_(0)
                self.state = 269
                self.match(StornParser.T__29)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 278
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,21,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = StornParser.TypeContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_type)
                    self.state = 273
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 274
                    self.match(StornParser.T__38)
                    self.state = 275
                    self.match(StornParser.CONSTANT) 
                self.state = 280
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,21,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[11] = self.lvalue_sempred
        self._predicates[29] = self.type_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def lvalue_sempred(self, localctx:LvalueContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         

    def type_sempred(self, localctx:TypeContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 1)
         




