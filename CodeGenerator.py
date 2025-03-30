from typing import Dict, List, Tuple, Literal
from storn.StornVisitor import StornVisitor
from storn.StornParser import StornParser
import copy

class Type:
    def __init__(self):
        self.size = 0
        self.offset = 0

    def calculate_size(self, data_table: Dict[str, "DataType"]):
        pass

    def calculate_offset(self, offset: int):
        self.offset = offset

    def copy(self):
        return copy.deepcopy(self)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Type)

    def __repr__(self) -> str:
        return ""

class BaseType(Type):
    def __init__(self, width: int):
        self.width = width
        self.size = int(width) // 8
        self.offset = 0

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseType) and self.width == other.width

    def __repr__(self) -> str:
        return f"[{self.width}]"

class UnresolvedType(Type):
    def __init__(self, name: str):
        self.name = name
        self.size = 0
        self.offset = 0

    def calculate_size(self, data_table: Dict[str, "DataType"]):
        self.size = data_table[self.name].size

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UnresolvedType) and self.name == other.name

    def __repr__(self) -> str:
        return self.name

class DataType(Type):
    def __init__(self, name: str, fields: Dict[str, Type]):
        for field in fields:
            if isinstance(field, UnresolvedType) and field.name == name:
                raise Exception("Cannot declare subfield of same type")
        self.name = name
        self.fields = fields
        self.size = 0
        self.offset = 0

    def calculate_size(self, data_table: Dict[str, "DataType"]):
        for field in self.fields.values():
            field.calculate_size(data_table)
            self.size += field.size

    def calculate_offset(self, offset: int):
        self.offset = offset
        size = 0
        for field in self.fields.values():
            field.calculate_offset(size)
            size += field.size

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DataType) and self.name == other.name and self.fields == other.fields

    def __repr__(self, seen=None):
        if seen is None:
            seen = set()
        if self.name in seen:
            return f"data {self.name} {{ ... }}"
        seen.add(self.name)
        return f"data {self.name} {{ " + ", ".join(
            f"{f} (offset: {self.fields[f].offset}): {self.fields[f].__repr__() if isinstance(self.fields[f], Type) else self.fields[f]}"
            for f in self.fields
        ) + " }"

class ReferenceType(Type):
    def __init__(self, type_: Type):
        self.type_ = type_
        self.size = 2
        self.offset = 0

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ReferenceType) and self.type_ == other.type_

    def __repr__(self):
        if isinstance(self.type_, str):
            return f"<[{self.type_}]>"
        return f"<{self.type_.__repr__()}>"

class ArrayType(Type):
    def __init__(self, type_: Type, length: int):
        self.type_ = type_
        self.elements = [type_] * length
        self.size = 0
        self.offset = 0

    def calculate_size(self, data_table: Dict[str, "DataType"]):
        for element in self.elements:
            element.calculate_size(data_table)
            element.calculate_offset(self.size)
            self.size += element.size

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ArrayType) and self.type_ == other.type_ and self.size == other.size

    def __repr__(self):
        if isinstance(self.type_, str):
            return f"[{self.type_}] ^ {len(self.elements)}"
        return f"{self.type_.__repr__()} ^ {len(self.elements)}"

class Routine:
    def __init__(self, parameters: Dict[str, Type], return_type: Type, scope: Dict[str, Type]):
        self.parameters = parameters
        self.return_type = return_type
        self.scope = scope

class CodeGenerator(StornVisitor):
    def __init__(self):
        self.instructions: List[str] = []
        self.data_table: Dict[str, DataType] = {}
        self.routine_table: Dict[str, Routine] = {}
        self.scope: Dict[str, Type] = {}
        self.label_count = 0

    def visitData(self, ctx: StornParser.DataContext):
        name = ctx.NAME().getText()
        declarations = ctx.typeDeclaration()

        fields: Dict[str, Type] = {}
        for declaration in declarations:
            field_name, field_type_ = self.visitTypeDeclaration(declaration)
            fields[field_name] = field_type_

        data_type = DataType(name, fields)
        data_type.calculate_size(self.data_table)
        self.data_table[name] = data_type

        return None

    def visitTypeDeclaration(self, ctx: StornParser.TypeDeclarationContext) -> Tuple[str, Type]:
        return self.visitTypedVar(ctx.typedVar())

    def visitTypedVar(self, ctx: StornParser.TypedVarContext) -> Tuple[str, Type]:
        name = ctx.NAME().getText()
        type_ = self.visitType(ctx.type_())
        return name, type_

    # Add the routine to the routine table before
    # compiling statements to enable recursion
    def visitRoutine(self, ctx: StornParser.RoutineContext):
        name = ctx.NAME().getText()
        param_list = ctx.typedParamList().typedVar()
        return_type = ctx.type_()
        variables = ctx.localVars()
        statements = ctx.statements().statement()

        parameters: Dict[str, Type] = {}
        for parameter in param_list:
            name, type_ = self.visitTypedVar(parameter)
            parameters[name] = type_

        routine_scope, size = self.visitLocalVars(variables)
        self.scope = routine_scope.copy()

        routine = Routine(parameters, return_type, routine_scope)
        self.routine_table[name] = routine

        # Prologue
        self.instructions += [
            f"{name.upper()}:",
            # "psh bp",
            # "mov bp sp",
            # f"sub sp {size}",
        ]

        # Body
        for statement in statements:
            self.visit(statement)

        # Epilogue
        self.instructions += [
            # "mov bp sp",
            # "pop bp",
            # "pop c",
        ]

    def visitLocalVars(self, ctx: StornParser.LocalVarsContext) -> Tuple[Dict[str, Type], int]:
        routine_scope: Dict[str, Type] = {}
        size = 0
        variables = ctx.typeDeclaration()
        if not variables:
            return {}, 0

        for variable in variables:
            name, type_ = self.visitTypeDeclaration(variable)
            type_.calculate_size(self.data_table)
            type_.calculate_offset(size)
            routine_scope[name] = type_
            size += type_.size

        return routine_scope, size

    def visitSetStmt(self, ctx: StornParser.SetStmtContext):
        lvalue = ctx.lvalue()
        expression = ctx.expression()

        # Compile expression first in case it modifies HL
        expression_type = self.visitExpression(expression)
        lvalue_type = self.visitLvalue(lvalue)

        if lvalue_type != expression_type:
            raise Exception("lvalue and expression are of different types")

        # Copy bytes from stack to memory range [<HL>, <HL - size>]
        self.instructions += [
            f"ldr c {expression_type.size}",
            f"L{self.label_count}:",
            "pop a",
            "str m a",
            "ldr a l",
            "dec",
            "ldr l a",
            "ldr a h",
            "dec cc",
            "ldr h a",
            "ldr a c",
            "dec",
            "ldr c a",
            f"jmp nzf L{self.label_count}",
        ]
        self.label_count += 1

    def visitLvalue(self, ctx: StornParser.LvalueContext) -> Type:
        return self.visitIndexLvalue(ctx.indexLvalue())

    def visitIndexLvalue(self, ctx: StornParser.IndexLvalueContext) -> Type:
        lvalue = self.visitProjectionLvalue(ctx.projectionLvalue())

        # first child is projectionLvalue then each expression adds two children: '@' and expression
        expression_count = (ctx.getChildCount() - 1) // 2
        for i in range(expression_count):
            if not isinstance(lvalue, ArrayType):
                raise Exception("Attemping to index non array type")

            index = self.visitExpression(ctx.expression(i))
            if not (isinstance(index, BaseType) and index.width == 8):
                raise Exception("Attempting to index by expression that doesn't evaluate to [8]")

            size = lvalue.size

            # Naive multiplication
            # HL := HL - index * size
            self.instructions += [
                f"ldr c {size}",
                "pop b", # index
                f"L{self.label_count}:",
                "ldr a l",
                "sub b",
                "ldr l a",
                "ldr a h",
                "dec cc",
                "ldr h a",
                "ldr a c",
                "dec",
                f"jmp nzf L{self.label_count}",
            ]
            self.label_count += 1

            lvalue = lvalue.type_

        return lvalue

    # TODO:
    # Consider `set foo / x / y = 10.`:
    #   - foo is a variable with a known offset
    #   - we know address of `y` at compilation
    #   - we can disregard instructions used to compute `foo / x`
    def visitProjectionLvalue(self, ctx: StornParser.ProjectionLvalueContext) -> Type:
        lvalue = self.visitReferenceLvalue(ctx.referenceLvalue())

        field_count = (ctx.getChildCount() - 1) // 2
        for i in range(field_count):
            if not isinstance(lvalue, DataType):
                raise Exception("Attempting to project non data type")

            field_name = ctx.NAME(i).getText()

            field_type = lvalue.fields[field_name]
            if not field_type:
                raise Exception("Attemping to project unknown field")

            if isinstance(field_type, UnresolvedType):
                # Don't need to recalculate size or offset
                resolved_type = self.data_table[field_name].copy()
                field_type = resolved_type

            offset = field_type.offset
            offset_low = offset & 0b11111111
            offset_high = offset >> 8

            # Compute address of field by its offset from parent address in HL
            # HL := HL - offset
            self.instructions += [
                "ldr a l",
                f"sub {offset_low}",
                "ldr l a",
                "ldr a h",
                f"sub cc {offset_high}",
                "ldr h a",
            ]

            lvalue = field_type

        return lvalue

    def visitReferenceLvalue(self, ctx: StornParser.ReferenceLvalueContext) -> Type:
        lvalue = self.visitPrimaryLvalue(ctx.primaryLvalue())

        if ctx.DEREFERENCE():
            if not isinstance(lvalue, ReferenceType):
                raise Exception("Attempting to dereference non reference type")

            # Address of reference is in HL
            # Need address referenced by said reference in HL
            # Hence, treat HL as an address and store ram[HL] in HL
            # i.e.:
            # L := ram[HL]
            # H := ram[HL - 1]
            self.instructions += [
                "ldr b m",
                "ldr a l",
                "dec",
                "ldr l a",
                "ldr a h",
                "dec cc",
                "ldr h m",
                "ldr l b",
            ]

            lvalue = lvalue.type_

        return lvalue

    def visitPrimaryLvalue(self, ctx: StornParser.PrimaryLvalueContext) -> Type:
        if ctx.lvalue():
            return self.visitLvalue(ctx.lvalue())

        try:
            variable = self.scope[ctx.NAME().getText()]
        except IndexError:
            raise Exception("Reference to unknown variable")

        if isinstance(variable, UnresolvedType):
            resolved_variable = self.data_table[variable.name].copy()
            resolved_variable.offset = variable.offset
            variable = resolved_variable

        offset = variable.offset
        offset_low = offset & 0b11111111
        offset_high = offset >> 8

        # Compute address of variable by its offset from BP
        # HL := BP - offset
        self.instructions += [
            "ldr a bpl",
            f"sub {offset_low}",
            "ldr l a",
            "ldr a bph",
            f"sub cc {offset_high}",
            "ldr h a",
        ]

        return variable

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

    def visitExpression(self, ctx: StornParser.ExpressionContext) -> Type:
        return self.visitLogicalExpr(ctx.logicalExpr())

    def visitLogicalExpr(self, ctx: StornParser.LogicalExprContext) -> Type:
        expression = self.visitComparativeExpr(ctx.comparativeExpr(0))

        comparative_count = (ctx.getChildCount() - 1) // 2
        for i in range(comparative_count):
            if not isinstance(expression, BaseType):
                raise Exception("Attemping to perform logical operation on non numerical type")
            next_expression = self.visitComparativeExpr(ctx.comparativeExpr(i + 1))
            if not isinstance(next_expression, BaseType):
                raise Exception("Attemping to perform logical operation on non numerical type")
            if expression.width != next_expression.width:
                raise Exception("Attemping to perform logical operation on expressions of differing width")

            operation = ctx.logicalOp()
            width = expression.width
            op_instruction = "or b" if operation.OR() else "and b"
            if width == 8:
                self.instructions += [
                    "pop b",
                    "pop a",
                    op_instruction,
                    "psh a",
                ]
            elif width == 16:
                self.instructions += [
                    "pop a",
                    "pop b",
                    op_instruction,
                    "ldr c a",
                    "pop a",
                    "pop b",
                    op_instruction,
                    "psh a",
                    "psh c",
                ]
            expression = next_expression

        return expression

    def visitComparativeExpr(self, ctx: StornParser.ComparativeExprContext):
        expression = self.visitAdditiveExpr(ctx.additiveExpr(0))

        additive_count = (ctx.getChildCount() - 1) // 2
        for i in range(additive_count):
            if not isinstance(expression, BaseType):
                raise Exception("Attemping to perform comparative operation on non numerical type")
            next_expression = self.visitAdditiveExpr(ctx.additiveExpr(i + 1))
            if not isinstance(next_expression, BaseType):
                raise Exception("Attemping to perform comparative operation on non numerical type")
            if expression.width != next_expression.width:
                raise Exception("Attemping to perform comparative operation on expressions of differing width")

            operation = ctx.comparativeOp()
            width = expression.width

            # Between the 10 cases (5 operations; 2 'widths'), only 2
            # operations are changing, namely, (i) the order of the
            # subtraction performed and (ii) the flag that is tested.
            # All 5 operations can be summarised here:
            # x = y  holds when y - x triggers zf
            # x < y  holds when x - y triggers sf
            # x > y  holds when y - x triggers sf
            # x <= y holds when y - x triggers nsf
            # x >= y holds when x - y triggers nsf
            pop_ops = ["pop b", "pop a"] # x - y
            if operation.EQ() or operation.GT() or operation.LEQ():
                pop_ops = ["pop a", "pop b"]
            flag: Literal["zf", "sf", "nsf"] = "zf"
            if operation.LT() or operation.GT():
                flag = "sf"
            if operation.LEQ() or operation.GEQ():
                flag = "nsf"

            if width == 8:
                self.instructions += [
                    *pop_ops,
                    "sub b",
                    f"jmp {flag} L{self.label_count}",
                    "psh 0",
                    f"jmp L{self.label_count + 1}",
                    f"L{self.label_count}:",
                    "psh 1",
                    f"L{self.label_count + 1}:",
                ]
                self.label_count += 2
            elif width == 16:
                self.instructions += [
                    *pop_ops,
                    "sub b",
                    f"jmp {flag} L{self.label_count}",
                    "psh 0",
                    f"jmp L{self.label_count + 1}",
                    f"L{self.label_count}:",
                    *pop_ops,
                    "sub b",
                    f"jmp {flag} L{self.label_count + 2}",
                    "psh 0",
                    f"jmp L{self.label_count + 1}",
                    f"L{self.label_count + 2}:",
                    "psh 1",
                    f"L{self.label_count + 1}:",
                ]
                self.label_count += 3

            expression = next_expression

        return expression

    def visitAdditiveExpr(self, ctx: StornParser.AdditiveExprContext):
        expression = self.visitMultiplicativeExpr(ctx.multiplicativeExpr(0))

        multiplicative_count = (ctx.getChildCount() - 1) // 2
        for i in range(multiplicative_count):
            if not isinstance(expression, BaseType):
                raise Exception("Attemping to perform additive operation on non numerical type")
            next_expression = self.visitAdditiveExpr(ctx.multiplicativeExpr(i + 1))
            if not isinstance(next_expression, BaseType):
                raise Exception("Attemping to perform additive operation on non numerical type")
            if expression.width != next_expression.width:
                raise Exception("Attemping to perform additive operation on expressions of differing width")

            operation = ctx.additiveOp()
            width = expression.width
            op_instruction = "add b" if operation.PLUS() else "sub b"
            op_cc_instruction = "add cc b" if operation.PLUS() else "sub cc b"
            if width == 8:
                self.instructions += [
                    "pop b",
                    "pop a",
                op_instruction,
                    "psh a",
                ]
            elif width == 16:
                self.instructions += [
                    "pop b",
                    "pop a",
                op_instruction,
                    "ldr c a",
                    "pop a",
                    "pop b",
                op_cc_instruction,
                    "psh a",
                    "psh c",
                ]
            expression = next_expression

        return expression

    def visitMultiplicativeExpr(self, ctx: StornParser.MultiplicativeExprContext):
        expression = self.visitUnaryExpr(ctx.unaryExpr(0))

        unary_count = (ctx.getChildCount() - 1) // 2
        for i in range(unary_count):
            if not (isinstance(expression, BaseType) and expression.width == 8):
                raise Exception("Attempting to multiply expression not of type [8]")
            next_expression = ctx.unaryExpr(i)
            if not (isinstance(next_expression, BaseType) and next_expression.width == 8):
                raise Exception("Attempting to multiply expression not of type [8]")

            self.instructions += [
                "pop l", # multiplier
                "pop b", # multiplicand
                "ldr c 8",
                f"L{self.label_count}:",
                "ldr a l",
                "and 1",
                f"jmp zf L{self.label_count + 1}",
                "ldr a h",
                "add b",
                "ldr h a",
                f"L{self.label_count + 1}:",
                "ldr a h",
                "shr",
                "ldr h a",
                "ldr a l",
                "shr cc",
                "ldr l a",
                "ldr a c",
                "dec",
                "ldr c a",
                f"jmp nzf L{self.label_count}",
                "psh h",
                "psh l",
            ]
            self.label_count += 2

            expression = next_expression

        return expression

    def visitUnaryExpr(self, ctx: StornParser.UnaryExprContext):
        expression = self.visitPrimaryExpr(ctx.primaryExpr())

        if ctx.MINUS() or ctx.NOT():
            if not isinstance(expression, BaseType):
                raise Exception("Attemping to perform unary operation on non numerical type")

            width = expression.width
            if ctx.MINUS():
                if width == 8:
                    self.instructions += [
                        "ldr a 0",
                        "pop b",
                        "sub b",
                        "psh a",
                    ]
                elif width == 16:
                    self.instructions += [
                        "ldr a 0",
                        "pop b",
                        "sub b",
                        "ldr c a",
                        "ldr a 0",
                        "pop b",
                        "sub cc b",
                        "psh a",
                        "psh c",
                    ]
            elif ctx.NOT():
                if width == 8:
                    self.instructions += [
                        "pop a",
                        "not",
                        "psh a",
                    ]
                elif width == 16:
                    self.instructions += [
                        "pop a",
                        "not",
                        "ldr b a",
                        "pop a",
                        "not",
                        "psh a",
                        "psh b",
                    ]

        return expression

    def visitPrimaryExpr(self, ctx: StornParser.PrimaryExprContext) -> Type:
        if ctx.expression():
            return self.visitExpression(ctx.expression())
        elif ctx.call():
            routine_name = ctx.call().NAME()
            try:
                routine = self.routine_table[routine_name]
            except IndexError:
                raise Exception("Reference to unknown routine")

            parameters = self.visitParameters(ctx.call().parameters())
            if parameters != routine.parameters:
                raise Exception("Invalid parameters for routine")

            # TODO: call routine

            return routine.return_type
        elif ctx.lvalue():
            lvalue = self.visitLvalue(ctx.lvalue())

            # Copy bytes from memory range [<HL>, <HL - size>] to stack
            self.instructions += [
                f"ldr c {lvalue.size}",
                f"L{self.label_count}:",
                "ldr a m",
                "psh a",
                "ldr a l",
                "inc",
                "ldr l a",
                "ldr a h",
                "inc cc",
                "ldr h a",
                "ldr a c",
                "dec",
                "ldr c a",
                f"jmp nzf L{self.label_count}",
            ]
            self.label_count += 1

            return lvalue
        else:
            constant = ctx.CONSTANT().getText()
            self.instructions += [
                f"psh {constant}"
            ]
            return BaseType(8)

    def visitType(self, ctx: StornParser.TypeContext) -> Type:
        if ctx.getChildCount() == 1: # Base type
            text = ctx.getText()
            width = int(text[1:-1])
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

