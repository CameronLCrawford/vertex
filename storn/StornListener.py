# Generated from storn/Storn.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .StornParser import StornParser
else:
    from StornParser import StornParser

# This class defines a complete listener for a parse tree produced by StornParser.
class StornListener(ParseTreeListener):

    # Enter a parse tree produced by StornParser#program.
    def enterProgram(self, ctx:StornParser.ProgramContext):
        pass

    # Exit a parse tree produced by StornParser#program.
    def exitProgram(self, ctx:StornParser.ProgramContext):
        pass


    # Enter a parse tree produced by StornParser#declaration.
    def enterDeclaration(self, ctx:StornParser.DeclarationContext):
        pass

    # Exit a parse tree produced by StornParser#declaration.
    def exitDeclaration(self, ctx:StornParser.DeclarationContext):
        pass


    # Enter a parse tree produced by StornParser#data.
    def enterData(self, ctx:StornParser.DataContext):
        pass

    # Exit a parse tree produced by StornParser#data.
    def exitData(self, ctx:StornParser.DataContext):
        pass


    # Enter a parse tree produced by StornParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:StornParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by StornParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:StornParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by StornParser#typedVar.
    def enterTypedVar(self, ctx:StornParser.TypedVarContext):
        pass

    # Exit a parse tree produced by StornParser#typedVar.
    def exitTypedVar(self, ctx:StornParser.TypedVarContext):
        pass


    # Enter a parse tree produced by StornParser#routine.
    def enterRoutine(self, ctx:StornParser.RoutineContext):
        pass

    # Exit a parse tree produced by StornParser#routine.
    def exitRoutine(self, ctx:StornParser.RoutineContext):
        pass


    # Enter a parse tree produced by StornParser#typedParamList.
    def enterTypedParamList(self, ctx:StornParser.TypedParamListContext):
        pass

    # Exit a parse tree produced by StornParser#typedParamList.
    def exitTypedParamList(self, ctx:StornParser.TypedParamListContext):
        pass


    # Enter a parse tree produced by StornParser#statements.
    def enterStatements(self, ctx:StornParser.StatementsContext):
        pass

    # Exit a parse tree produced by StornParser#statements.
    def exitStatements(self, ctx:StornParser.StatementsContext):
        pass


    # Enter a parse tree produced by StornParser#statement.
    def enterStatement(self, ctx:StornParser.StatementContext):
        pass

    # Exit a parse tree produced by StornParser#statement.
    def exitStatement(self, ctx:StornParser.StatementContext):
        pass


    # Enter a parse tree produced by StornParser#initStmt.
    def enterInitStmt(self, ctx:StornParser.InitStmtContext):
        pass

    # Exit a parse tree produced by StornParser#initStmt.
    def exitInitStmt(self, ctx:StornParser.InitStmtContext):
        pass


    # Enter a parse tree produced by StornParser#setStmt.
    def enterSetStmt(self, ctx:StornParser.SetStmtContext):
        pass

    # Exit a parse tree produced by StornParser#setStmt.
    def exitSetStmt(self, ctx:StornParser.SetStmtContext):
        pass


    # Enter a parse tree produced by StornParser#lvalue.
    def enterLvalue(self, ctx:StornParser.LvalueContext):
        pass

    # Exit a parse tree produced by StornParser#lvalue.
    def exitLvalue(self, ctx:StornParser.LvalueContext):
        pass


    # Enter a parse tree produced by StornParser#ifStmt.
    def enterIfStmt(self, ctx:StornParser.IfStmtContext):
        pass

    # Exit a parse tree produced by StornParser#ifStmt.
    def exitIfStmt(self, ctx:StornParser.IfStmtContext):
        pass


    # Enter a parse tree produced by StornParser#loopStmt.
    def enterLoopStmt(self, ctx:StornParser.LoopStmtContext):
        pass

    # Exit a parse tree produced by StornParser#loopStmt.
    def exitLoopStmt(self, ctx:StornParser.LoopStmtContext):
        pass


    # Enter a parse tree produced by StornParser#breakStmt.
    def enterBreakStmt(self, ctx:StornParser.BreakStmtContext):
        pass

    # Exit a parse tree produced by StornParser#breakStmt.
    def exitBreakStmt(self, ctx:StornParser.BreakStmtContext):
        pass


    # Enter a parse tree produced by StornParser#outputStmt.
    def enterOutputStmt(self, ctx:StornParser.OutputStmtContext):
        pass

    # Exit a parse tree produced by StornParser#outputStmt.
    def exitOutputStmt(self, ctx:StornParser.OutputStmtContext):
        pass


    # Enter a parse tree produced by StornParser#returnStmt.
    def enterReturnStmt(self, ctx:StornParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by StornParser#returnStmt.
    def exitReturnStmt(self, ctx:StornParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by StornParser#expression.
    def enterExpression(self, ctx:StornParser.ExpressionContext):
        pass

    # Exit a parse tree produced by StornParser#expression.
    def exitExpression(self, ctx:StornParser.ExpressionContext):
        pass


    # Enter a parse tree produced by StornParser#logicalExpr.
    def enterLogicalExpr(self, ctx:StornParser.LogicalExprContext):
        pass

    # Exit a parse tree produced by StornParser#logicalExpr.
    def exitLogicalExpr(self, ctx:StornParser.LogicalExprContext):
        pass


    # Enter a parse tree produced by StornParser#comparativeExpr.
    def enterComparativeExpr(self, ctx:StornParser.ComparativeExprContext):
        pass

    # Exit a parse tree produced by StornParser#comparativeExpr.
    def exitComparativeExpr(self, ctx:StornParser.ComparativeExprContext):
        pass


    # Enter a parse tree produced by StornParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:StornParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by StornParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:StornParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by StornParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:StornParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by StornParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:StornParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by StornParser#unaryExpr.
    def enterUnaryExpr(self, ctx:StornParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by StornParser#unaryExpr.
    def exitUnaryExpr(self, ctx:StornParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by StornParser#primaryExpr.
    def enterPrimaryExpr(self, ctx:StornParser.PrimaryExprContext):
        pass

    # Exit a parse tree produced by StornParser#primaryExpr.
    def exitPrimaryExpr(self, ctx:StornParser.PrimaryExprContext):
        pass


    # Enter a parse tree produced by StornParser#comparativeOp.
    def enterComparativeOp(self, ctx:StornParser.ComparativeOpContext):
        pass

    # Exit a parse tree produced by StornParser#comparativeOp.
    def exitComparativeOp(self, ctx:StornParser.ComparativeOpContext):
        pass


    # Enter a parse tree produced by StornParser#call.
    def enterCall(self, ctx:StornParser.CallContext):
        pass

    # Exit a parse tree produced by StornParser#call.
    def exitCall(self, ctx:StornParser.CallContext):
        pass


    # Enter a parse tree produced by StornParser#callArgs.
    def enterCallArgs(self, ctx:StornParser.CallArgsContext):
        pass

    # Exit a parse tree produced by StornParser#callArgs.
    def exitCallArgs(self, ctx:StornParser.CallArgsContext):
        pass


    # Enter a parse tree produced by StornParser#arrayIndex.
    def enterArrayIndex(self, ctx:StornParser.ArrayIndexContext):
        pass

    # Exit a parse tree produced by StornParser#arrayIndex.
    def exitArrayIndex(self, ctx:StornParser.ArrayIndexContext):
        pass


    # Enter a parse tree produced by StornParser#refValue.
    def enterRefValue(self, ctx:StornParser.RefValueContext):
        pass

    # Exit a parse tree produced by StornParser#refValue.
    def exitRefValue(self, ctx:StornParser.RefValueContext):
        pass


    # Enter a parse tree produced by StornParser#type.
    def enterType(self, ctx:StornParser.TypeContext):
        pass

    # Exit a parse tree produced by StornParser#type.
    def exitType(self, ctx:StornParser.TypeContext):
        pass



del StornParser