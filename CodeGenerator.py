from typing import Dict, List, Literal, Tuple
from storn.StornVisitor import StornVisitor
from storn.StornParser import StornParser

class Type:
    def __init__(self):
        self.size = 0
        self.offset = 0

    def calculate_size(self, data_table: Dict[str, "DataType"]):
        pass

    def calculate_offset(self, offset: int):
        self.offset = offset

    def __repr__(self) -> str:
        return ""

class TypedVar:
    def __init__(self, name: str, type_: Type):
        self.name = name
        self.type_ = type_
        self.size = 0
        self.offset = 0

    def calculate_size(self, data_table: Dict[str, "DataType"]):
        self.type_.calculate_size(data_table)
        self.size = self.type_.size

    def calculate_offset(self, offset: int):
        self.type_.calculate_offset(offset)

    def __repr__(self) -> str:
        return f"{self.name}: {self.type_}"

class BaseType(Type):
    def __init__(self, width: Literal[0, 8, 16]):
        self.width = width
        self.size = int(width) / 8
        self.offset = 0

    def __repr__(self) -> str:
        return f"[{self.width}]"

class UnresolvedType(Type):
    def __init__(self, name: str):
        self.name = name
        self.size = 0
        self.offset = 0

    def calculate_size(self, data_table: Dict[str, "DataType"]):
        self.size = data_table[self.name].size

    def __repr__(self) -> str:
        return self.name

class DataType(Type):
    def __init__(self, name: str, fields: List[TypedVar]):
        for field in fields:
            if isinstance(field, UnresolvedType) and field.name == name:
                raise Exception("Cannot declare subfield of same type")
        self.name = name
        self.fields = fields
        self.size = 0
        self.offset = 0

    def calculate_size(self, data_table: Dict[str, "DataType"]):
        for field in self.fields:
            field.calculate_size(data_table)
            self.size += field.size

    def calculate_offset(self, offset: int):
        for field in self.fields:
            field.calculate_offset(offset)
            offset += field.size

    def __repr__(self, seen=None):
        if seen is None:
            seen = set()
        if self.name in seen:
            return f"data {self.name} {{ ... }}"
        seen.add(self.name)
        return f"data {self.name} {{ " + ", ".join(
            f"{f.name} (offset: {f.offset}): {f.type_.__repr__() if isinstance(f.type_, Type) else f.type_}"
            for f in self.fields
        ) + " }"

class ReferenceType(Type):
    def __init__(self, type_: Type):
        self.type_ = type_
        self.size = 2
        self.offset = 0

    def __repr__(self):
        if isinstance(self.type_, str):
            return f"<[{self.type_}]>"
        return f"<{self.type_.__repr__()}>"

class ArrayType(Type):
    def __init__(self, type_: Type, length: int):
        self.type_ = type_
        self.length = length
        self.size = 0
        self.offset = 0

    def calculate_size(self, data_table: Dict[str, "DataType"]):
        self.type_.calculate_size(data_table)
        self.size = self.length * self.type_.size

    def __repr__(self):
        if isinstance(self.type_, str):
            return f"[{self.type_}] ^ {self.length}"
        return f"{self.type_.__repr__()} ^ {self.length}"

class RoutineVar:
    def __init__(self, type_: Type, offset: int):
        self.type_ = type_
        self.offset = offset

class Routine:
    def __init__(self, parameters: List[TypedVar], return_type: Type, scope: Dict[str, RoutineVar]):
        self.parameters = parameters
        self.return_type = return_type
        self.scope = scope

class CodeGenerator(StornVisitor):
    def __init__(self):
        self.instructions: List[str] = []
        self.data_table: Dict[str, DataType] = {}
        self.routine_table: Dict[str, Routine] = {}
        self.scope: Dict[str, RoutineVar] = {}

    def visitData(self, ctx: StornParser.DataContext):
        name = ctx.NAME().getText()
        declarations = ctx.typeDeclaration()

        fields: List[TypedVar] = []
        for declaration in declarations:
            fields.append(self.visitTypeDeclaration(declaration))

        data_type = DataType(name, fields)
        data_type.calculate_size(self.data_table)
        self.data_table[name] = data_type

        return None

    def visitTypeDeclaration(self, ctx: StornParser.TypeDeclarationContext):
        return self.visitTypedVar(ctx.typedVar())

    def visitTypedVar(self, ctx: StornParser.TypedVarContext):
        name = ctx.NAME().getText()
        type_ = self.visitType(ctx.type_())
        return TypedVar(name, type_)

    # Add the routine to the routine table before
    # compiling statements to enable recursion
    def visitRoutine(self, ctx: StornParser.RoutineContext):
        name = ctx.NAME().getText()
        param_list = ctx.typedParamList().typedVar()
        return_type = ctx.type_()
        variables = ctx.localVars()
        statements = ctx.statements().statement()

        parameters = []
        for parameter in param_list:
            parameters.append(self.visit(parameter))

        routine_scope, size = self.visitLocalVars(variables)
        self.scope = routine_scope.copy()

        routine = Routine(parameters, return_type, routine_scope)
        self.routine_table[name] = routine

        # Prologue
        self.instructions += [
            f"{name.upper()}:",
            "psh bp",
            "mov bp sp",
            f"sub sp {size}",
        ]

        # Body
        for statement in statements:
            self.visit(statement)

        # Epilogue
        self.instructions += [
            "mov bp sp",
            "pop bp",
            "pop c",
        ]

    def visitLocalVars(self, ctx: StornParser.LocalVarsContext) -> Tuple[Dict[str, RoutineVar], int]:
        routine_scope: Dict[str, RoutineVar] = {}
        size = 0
        variables = ctx.typeDeclaration()
        if not variables:
            return {}, 0

        for variable in variables:
            typed_var = self.visitTypeDeclaration(variable)
            typed_var.calculate_size(self.data_table)
            typed_var.calculate_offset(0)
            routine_scope[typed_var.name] = RoutineVar(typed_var.type_, size)
            size += typed_var.size

        return routine_scope, size

    def visitSetStmt(self, ctx: StornParser.SetStmtContext):
        return super().visitSetStmt(ctx)

    def visitLvalue(self, ctx: StornParser.LvalueContext):
        return super().visitLvalue(ctx)

    def visitIfStmt(self, ctx: StornParser.IfStmtContext):
        return super().visitIfStmt(ctx)

    def visitLoopStmt(self, ctx: StornParser.LoopStmtContext):
        return super().visitLoopStmt(ctx)

    def visitBreakStmt(self, ctx: StornParser.BreakStmtContext):
        return super().visitBreakStmt(ctx)

    def visitOutputStmt(self, ctx: StornParser.OutputStmtContext):
        return super().visitOutputStmt(ctx)

    def visitReturnStmt(self, ctx: StornParser.ReturnStmtContext):
        return super().visitReturnStmt(ctx)

    def visitExpression(self, ctx: StornParser.ExpressionContext):
        return super().visitExpression(ctx)

    def visitType(self, ctx: StornParser.TypeContext):
        if ctx.getChildCount() == 1: # Base type
            text = ctx.getText()
            width = text[1:-1]
            return BaseType(width)
        elif ctx.NAME(): # Data type to be resolved
            name = ctx.NAME().getText()
            return UnresolvedType(name)
        elif ctx.CONSTANT(): # Array type
            type_ = self.visitType(ctx.type_())
            length = int(ctx.CONSTANT().getText())
            return ArrayType(type_, length)
        else: # Reference type
            type_ = self.visitType(ctx.type_())
            return ReferenceType(type_)

