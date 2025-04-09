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
    def __init__(self, parameters: Dict[str, Type], return_type: Type, scope: Dict[str, Type], is_entry: bool):
        self.parameters = parameters
        self.return_type = return_type
        self.scope = scope
        self.is_entry = is_entry

class CodeGenerator(StornVisitor):
    def __init__(self):
        self.instructions: List[str] = ["jmp ENTRY"]
        self.data_table: Dict[str, DataType] = {}
        self.routine_table: Dict[str, Routine] = {}
        self.current_routine: Routine = Routine({}, Type(), {}, False)
        self.label_count = 0
        self.loop_label_stack = []

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
        parameters = self.visitTypedParamList(ctx.typedParamList())
        return_type = self.visitType(ctx.type_())
        routine_scope, size = self.visitLocalVars(ctx.localVars())
        name = ctx.NAME().getText()
        if name in self.routine_table:
            raise Exception("Redeclaring routine")
        routine = Routine(parameters, return_type, routine_scope, name == "entry")
        self.routine_table[name] = routine
        self.current_routine = routine

        # Prologue
        size_low = size & 0b11111111
        size_high = size >> 8
        self.instructions += [
            f"{name.upper()}:",
            # NOTE: push state here
            "psh bph",
            "psh bpl",
            "ldr bph sph",
            "ldr bpl spl",
            "ldr a spl",
            f"sub {size_low}",
            "ldr spl a",
            "ldr a sph",
            f"sub cc {size_high}",
            "ldr sph a",
        ]

        self.visitStatements(ctx.statements())

    def visitTypedParamList(self, ctx: StornParser.TypedParamListContext) -> Dict[str, Type]:
        parameters: Dict[str, Type] = {}

        # Tracks the cumulative offset from BP.
        # Starts at 3 since BP exists on the stack as BPH and BPL and return is two bytes:
        # | 0x0000 |
        # |  ....  |
        # | LOCAL1 | <- SP
        # | LOCAL0 | <- local 0 offset
        # | BPL    | <- BP points here
        # | BPH    |
        # | RETURN | <- return low
        # | RETURN | <- return high; cumulative offset starts here
        # | PARAM0 |
        # | PARAM0 |
        # | PARAM0 | <- param 0 offset
        # | PARAM1 | <- param 1 offset
        # |  ....  |
        # | 0xFFFF |
        cumulative_offset = 3
        for variable in ctx.typedVar():
            name, type_ = self.visitTypedVar(variable)
            type_.calculate_size(self.data_table)
            cumulative_offset += type_.size
            type_.calculate_offset(cumulative_offset)
            parameters[name] = type_

        return parameters

    def visitLocalVars(self, ctx: StornParser.LocalVarsContext) -> Tuple[Dict[str, Type], int]:
        routine_scope: Dict[str, Type] = {}
        variables = ctx.typeDeclaration()
        if not variables:
            return {}, 0

        # Note that cumulative offset is 1 here
        # in spite of there being no bytes between BP and the local vars.
        # This is because the pointer points to where the next variable
        # will be instead of where the base of it will end.
        cumulative_offset = 1
        for variable in reversed(variables):
            name, type_ = self.visitTypeDeclaration(variable)
            type_.calculate_size(self.data_table)
            type_.calculate_offset(cumulative_offset)
            routine_scope[name] = type_
            cumulative_offset += type_.size

        size = cumulative_offset - 1
        return routine_scope, size

    def visitStatements(self, ctx: StornParser.StatementsContext):
        statements = ctx.statement()

        for statement in statements:
            self.visit(statement)

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
            "ldr a c",
            f"jmp zf L{self.label_count + 1}",
            "dec",
            "ldr c a",
            "pop a",
            "str m a",
            "ldr a l",
            "dec",
            "ldr l a",
            "ldr a h",
            "dec cc",
            "ldr h a",
            f"jmp L{self.label_count}",
            f"L{self.label_count + 1}:",
        ]
        self.label_count += 2

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
                "pop b", # index
                f"ldr c {size}",
                f"L{self.label_count}:",
                "ldr a c",
                f"jmp zf L{self.label_count + 1}",
                "dec",
                "ldr c a",
                "ldr a l",
                "sub b",
                "ldr l a",
                "ldr a h",
                "dec cc",
                "ldr h a",
                f"jmp L{self.label_count}",
                f"L{self.label_count + 1}:",
            ]
            self.label_count += 2

            lvalue = lvalue.type_

            if isinstance(lvalue, UnresolvedType):
                lvalue = self.data_table[lvalue.name].copy()

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

        # Whether to add or subtract from BP to get variable address
        offset_operation = "add"
        variable_name = ctx.NAME().getText()
        if variable_name in self.current_routine.scope:
            variable = self.current_routine.scope[variable_name]
            offset_operation = "sub"
        elif variable_name in self.current_routine.parameters:
            variable = self.current_routine.parameters[variable_name]
        else:
            raise Exception("Reference to unknown variable")

        if isinstance(variable, UnresolvedType):
            resolved_variable = self.data_table[variable.name].copy()
            resolved_variable.offset = variable.offset
            variable = resolved_variable

        offset = variable.offset
        if offset_operation == "add":
            # Read visitTypedParamList
            offset += 3
            offset += variable.size
        offset_low = offset & 0b11111111
        offset_high = offset >> 8

        # Compute address of variable by its offset from BP
        # HL := BP +/- offset
        self.instructions += [
            "ldr a bpl",
            f"{offset_operation} {offset_low}",
            "ldr l a",
            "ldr a bph",
            f"{offset_operation} cc {offset_high}",
            "ldr h a",
        ]

        return variable

    def visitIfStmt(self, ctx: StornParser.IfStmtContext):
        expression = self.visitExpression(ctx.expression())
        if not (isinstance(expression, BaseType) and expression.width == 8):
            raise Exception("If condition expression evaluates to non [8] type")

        self.instructions += [
            "pop a",
            f"jmp zf L{self.label_count}"
        ]

        self.visitStatements(ctx.statements())

        self.instructions += [
            f"L{self.label_count}:",
        ]
        self.label_count += 1

    def visitLoopStmt(self, ctx: StornParser.LoopStmtContext):
        start_label = self.label_count
        end_label = self.label_count + 1
        self.loop_label_stack.append(start_label)
        self.label_count += 2

        self.instructions += [
            f"L{start_label}:",
        ]

        self.visitStatements(ctx.statements())

        self.instructions += [
            f"jmp L{start_label}",
            f"L{end_label}:",
        ]

        self.loop_label_stack.pop()

    def visitBreakStmt(self, ctx: StornParser.BreakStmtContext):
        # Start label is on top of loop label stack
        # End label is start label + 1
        self.instructions += [
            f"jmp L{self.loop_label_stack[-1] + 1}"
        ]

    def visitOutputStmt(self, ctx: StornParser.OutputStmtContext):
        expression = self.visitExpression(ctx.expression())

        self.instructions += [
            f"ldr c {expression.size}",
            f"L{self.label_count}:",
            "ldr a c",
            f"jmp zf L{self.label_count + 1}",
            "dec",
            "ldr c a",
            "pop a",
            "out",
            f"jmp L{self.label_count}",
            f"L{self.label_count + 1}:",
        ]
        self.label_count += 2

    def visitReturnStmt(self, ctx: StornParser.ReturnStmtContext):
        if self.current_routine.is_entry:
            self.instructions += [
                "hlt",
            ]
            return

        if ctx.expression():
            expression_type = self.visitExpression(ctx.expression())
            if expression_type != self.current_routine.return_type:
                raise Exception("Return type doesn't matched expectation for routine")

            # Copy expression result from stack to caller-allocated return space on stack
            # Start of caller-allocated return space is at: BP + 1 (caller BPH) + 2 (return addr) + param size
            # Pop and increment
            total_parameter_size = sum([
                param.size
                for param in self.current_routine.parameters.values()
            ])
            offset = total_parameter_size + 4
            offset_low = offset & 0b11111111
            offset_high = offset >> 8

            self.instructions += [
                "ldr a bpl",
                f"add {offset_low}",
                "ldr l a",
                "ldr a bph",
                f"add cc {offset_high}",
                "ldr h a",
                f"ldr c {self.current_routine.return_type.size}",
                f"L{self.label_count}:",
                "ldr a c",
                f"jmp zf L{self.label_count + 1}",
                "dec",
                "ldr c a",
                "pop a",
                "str m a",
                "ldr a l",
                "inc",
                "ldr l a",
                "ldr a h",
                "inc cc",
                "ldr h a",
                f"jmp L{self.label_count}",
                f"L{self.label_count + 1}:",
            ]
            self.label_count += 2

        # Epilogue: mov sp bp, pop bp, pop m (return), jmp m
        self.instructions += [
            "ldr sph bph",
            "ldr spl bpl",
            "pop bpl",
            "pop bph",
            "pop l",
            "pop h",
            "jmp m",
        ]

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

    def visitComparativeExpr(self, ctx: StornParser.ComparativeExprContext) -> Type:
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

            operation = ctx.comparativeOp(i)
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

    def visitAdditiveExpr(self, ctx: StornParser.AdditiveExprContext) -> Type:
        expression = self.visitMultiplicativeExpr(ctx.multiplicativeExpr(0))

        multiplicative_count = (ctx.getChildCount() - 1) // 2
        for i in range(multiplicative_count):
            if not isinstance(expression, BaseType):
                raise Exception("Attemping to perform additive operation on non numerical type")
            next_expression = self.visitMultiplicativeExpr(ctx.multiplicativeExpr(i + 1))
            if not isinstance(next_expression, BaseType):
                raise Exception("Attemping to perform additive operation on non numerical type")
            if expression.width != next_expression.width:
                raise Exception("Attemping to perform additive operation on expressions of differing width")

            operation = ctx.additiveOp(i)
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

    def visitMultiplicativeExpr(self, ctx: StornParser.MultiplicativeExprContext) -> Type:
        expression = self.visitUnaryExpr(ctx.unaryExpr(0))

        unary_count = (ctx.getChildCount() - 1) // 2
        for i in range(unary_count):
            if not (isinstance(expression, BaseType) and expression.width == 8):
                raise Exception("Attempting to multiply expression not of type [8]")
            next_expression = self.visitUnaryExpr(ctx.unaryExpr(i))
            if not (isinstance(next_expression, BaseType) and next_expression.width == 8):
                raise Exception("Attempting to multiply expression not of type [8]")

            self.instructions += [
                "pop l", # multiplier
                "pop b", # multiplicand
                "ldr h 0",
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

            expression = BaseType(16)

        return expression

    def visitUnaryExpr(self, ctx: StornParser.UnaryExprContext) -> Type:
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
            routine_name = ctx.call().NAME().getText()
            if routine_name in self.routine_table:
                routine = self.routine_table[routine_name]
            else:
                raise Exception("Reference to unknown routine")

            # Allocate space for return bytes on stack
            return_type = routine.return_type
            return_size = return_type.size
            return_size_low = return_size & 0b11111111
            return_size_high = return_size >> 8
            self.instructions += [
                "ldr a spl",
                f"sub {return_size_low}",
                "ldr spl a",
                "ldr a sph",
                f"sub cc {return_size_high}",
                "ldr sph a",
            ]

            parameters = ctx.call().parameters().expression()
            expected_parameter_types = self.routine_table[routine_name].parameters.values()

            total_parameter_size = 0
            for parameter, expected_parameter_type in zip(reversed(parameters), reversed(expected_parameter_types)):
                parameter_type = self.visitExpression(parameter)
                if parameter_type != expected_parameter_type:
                    raise Exception("Parameter expression is an inconsistent type with routine expectation")
                total_parameter_size += parameter_type.size

            self.instructions += [
                f"cal {routine_name.upper()}",
            ]

            # Pop parameters
            param_size_low = total_parameter_size & 0b11111111
            param_size_high = total_parameter_size >> 8
            self.instructions +=  [
                "ldr a spl",
                f"add {param_size_low}",
                "ldr spl a",
                "ldr a sph",
                f"add cc {param_size_high}",
                "ldr sph a",
            ]

            return return_type
        elif ctx.lvalue():
            lvalue = self.visitLvalue(ctx.lvalue())

            # Copy bytes from memory range [<HL>, <HL - size>] to stack
            self.instructions += [
                f"ldr c {lvalue.size}",
                f"L{self.label_count}:",
                "ldr a c",
                f"jmp zf L{self.label_count + 1}",
                "dec",
                "ldr c a",
                "ldr a m",
                "psh a",
                "ldr a l",
                "inc",
                "ldr l a",
                "ldr a h",
                "inc cc",
                "ldr h a",
                f"jmp L{self.label_count}",
                f"L{self.label_count + 1}:",
            ]
            self.label_count += 2

            return lvalue
        else:
            constant = ctx.CONSTANT().getText()
            width = int(ctx.literalWidth().getText())

            if width == 8:
                self.instructions += [
                    f"psh {constant}"
                ]
            elif width == 16:
                constant_low = constant & 0b11111111
                constant_high = constant >> 8
                self.instructions += [
                    f"psh {constant_low}",
                    f"psh {constant_high}",
                ]

            return BaseType(width)

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

