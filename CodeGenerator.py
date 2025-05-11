from typing import Dict, List, Tuple, Literal
from storn.StornVisitor import StornVisitor
from storn.StornParser import StornParser
import copy

GLOBAL_VAR_BASE = 0
GLOBAL_VAR_BASE_LOW = GLOBAL_VAR_BASE & 0b11111111
GLOBAL_VAR_BASE_HIGH = GLOBAL_VAR_BASE >> 8

class CompileError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.__str__())

    def __str__(self) -> str:
        if self.line is not None and self.column is not None:
            return f"{self.line}:{self.column} {self.message}"
        return self.message

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
                raise CompileError(f"Cannot declare field of same type for data type {name}")
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
        self.globals: Dict[str, Type] = {}
        self.global_offset = 0
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
        data_type.calculate_offset(0)
        self.data_table[name] = data_type

        return None

    def visitTypeDeclaration(self, ctx: StornParser.TypeDeclarationContext) -> Tuple[str, Type]:
        return self.visitTypedVar(ctx.typedVar())

    def visitTypedVar(self, ctx: StornParser.TypedVarContext) -> Tuple[str, Type]:
        name = ctx.NAME().getText()
        type_ = self.visitType(ctx.type_())
        return name, type_

    def visitGlobal(self, ctx: StornParser.GlobalContext):
        name, type_ = self.visitTypeDeclaration(ctx.typeDeclaration())
        type_.calculate_size(self.data_table)
        type_.calculate_offset(self.global_offset)
        self.global_offset += type_.size
        self.globals[name] = type_

    # Add the routine to the routine table before
    # compiling statements to enable recursion
    def visitRoutine(self, ctx: StornParser.RoutineContext):
        parameters = self.visitTypedParamList(ctx.typedParamList())
        return_type = self.visitType(ctx.type_())
        routine_scope, size = self.visitLocalVars(ctx.localVars())
        name = ctx.NAME().getText()
        if name in self.routine_table:
            raise CompileError("Redeclaring routine", ctx.NAME().start.line, ctx.NAME().start.column)
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
        # Starts at 4 since BP exists on the stack as BPH and BPL and return is two bytes:
        # | 0x0000 |
        # |  ....  |
        # | LOCAL1 | <- SP
        # | LOCAL0 | <- local 0 offset
        # | BPL    | <- BP points here (0)
        # | BPH    | (1)
        # | RETURN | <- return low (2)
        # | RETURN | <- return high (3)
        # | PARAM0 | <- param 0 offset (4)
        # | PARAM0 |
        # | PARAM0 |
        # | PARAM1 | <- param 1 offset (4 + PARAM0.size)
        # |  ....  |
        # | 0xFFFF |
        cumulative_offset = 4
        for variable in ctx.typedVar():
            name, type_ = self.visitTypedVar(variable)
            type_.calculate_size(self.data_table)
            type_.calculate_offset(cumulative_offset)
            cumulative_offset += type_.size
            parameters[name] = type_

        return parameters

    def visitLocalVars(self, ctx: StornParser.LocalVarsContext) -> Tuple[Dict[str, Type], int]:
        routine_scope: Dict[str, Type] = {}
        variables = ctx.typeDeclaration()
        if not variables:
            return {}, 0

        # The cumulative offset starts at zero from BP
        # and is increased by the size of each variable
        # routine foo (x: [8], y: [16], z: [8])
        # | 0x0000 |
        # |  ....  |
        # | X      | <- x offset (0 + Z.size + Y.size + X.size)
        # | Y      | <- y low; y offset (0 + Z.size + Y.size)
        # | Y      | <- y high
        # | Z      | <- z offset (0 + Z.size)
        # | BPL    | <- BP points here
        # | BPH    |
        # |  ....  |
        # | 0xFFFF |
        cumulative_offset = 0
        for variable in reversed(variables):
            name, type_ = self.visitTypeDeclaration(variable)
            type_.calculate_size(self.data_table)
            cumulative_offset += type_.size
            type_.calculate_offset(cumulative_offset)
            routine_scope[name] = type_

        # Cumulative offset tracks total size
        return routine_scope, cumulative_offset

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
            raise CompileError("lvalue and expression are of different types", lvalue.start.line, lvalue.start.column)

        # Pop bytes from stack to memory range [HL, HL + (size - 1)]
        # The top of the stack is the lowest byte of the variable, hence
        # we pop into HL, pop into HL + 1, pop into HL + 2, etc.
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
            "inc",
            "ldr l a",
            "ldr a h",
            "inc cc",
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
                raise CompileError("Attempting to index non array type", ctx.projectionLvalue().start.line, ctx.projectionLvalue().start.line)

            index = self.visitExpression(ctx.expression(i))
            if not (isinstance(index, BaseType) and index.width == 8):
                raise CompileError("Attempting to index by expression that doesn't evaluate to [8]", ctx.expression(i).start.line, ctx.expression(i).start.column)

            size = lvalue.size

            # Naive multiplication
            # HL := HL + index * size
            self.instructions += [
                "pop b", # index
                f"ldr c {size}",
                f"L{self.label_count}:",
                "ldr a c",
                f"jmp zf L{self.label_count + 1}",
                "dec",
                "ldr c a",
                "ldr a l",
                "add b",
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

    def visitProjectionLvalue(self, ctx: StornParser.ProjectionLvalueContext) -> Type:
        lvalue = self.visitReferenceLvalue(ctx.referenceLvalue())

        field_count = (ctx.getChildCount() - 1) // 2
        for i in range(field_count):
            if not isinstance(lvalue, DataType):
                raise CompileError("Attempting to project non data type", ctx.referenceLvalue().start.line, ctx.referenceLvalue().start.column)

            field_name = ctx.NAME(i).getText()

            field_type = lvalue.fields[field_name]
            if not field_type:
                raise CompileError("Attempting to project unknown field", ctx.NAME(i).start.line, ctx.NAME(i).start.column)

            if isinstance(field_type, UnresolvedType):
                # Don't need to recalculate size or offset
                resolved_type = self.data_table[field_name].copy()
                field_type = resolved_type

            offset = field_type.offset
            offset_low = offset & 0b11111111
            offset_high = offset >> 8

            # Compute address of field by its offset from parent address in HL
            # HL := HL + offset
            self.instructions += [
                "ldr a l",
                f"add {offset_low}",
                "ldr l a",
                "ldr a h",
                f"add cc {offset_high}",
                "ldr h a",
            ]

            lvalue = field_type

        return lvalue

    def visitReferenceLvalue(self, ctx: StornParser.ReferenceLvalueContext) -> Type:
        lvalue = self.visitPrimaryLvalue(ctx.primaryLvalue())

        if ctx.DEREFERENCE():
            if not isinstance(lvalue, ReferenceType):
                raise CompileError("Attempting to dereference non reference type", ctx.primaryLvalue().start.line, ctx.primaryLvalue().start.column)

            # Address of reference is in HL; reference is a 2-byte little endian memory address
            # Need address of object referenced by said reference in HL
            # Hence, store ram[HL] in HL
            # i.e.:
            # L := ram[HL]
            # H := ram[HL + 1]
            self.instructions += [
                "ldr b m", # L
                "ldr a l",
                "inc",
                "ldr l a",
                "ldr a h",
                "inc cc",
                "ldr h m",
                "ldr l b",
            ]

            unresolved_type = lvalue.type_
            if isinstance(unresolved_type, UnresolvedType):
                resolved_type = self.data_table[unresolved_type.name].copy()
                resolved_type.offset = unresolved_type.offset
                lvalue = resolved_type
            else:
                lvalue = unresolved_type

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
        elif variable_name in self.globals:
            variable = self.globals[variable_name]
        else:
            raise CompileError("Reference to unknown variable", ctx.NAME().start.line, ctx.NAME().start.column)

        if isinstance(variable, UnresolvedType):
            resolved_variable = self.data_table[variable.name].copy()
            resolved_variable.offset = variable.offset
            variable = resolved_variable

        offset = variable.offset
        offset_low = offset & 0b11111111
        offset_high = offset >> 8

        if variable_name in self.globals:
            base_low = GLOBAL_VAR_BASE_LOW
            base_high = GLOBAL_VAR_BASE_HIGH
        else:
            base_low = "bpl"
            base_high = "bph"

        # Compute address of variable by its offset from BP
        # HL := BP +/- offset
        self.instructions += [
            f"ldr a {base_low}",
            f"{offset_operation} {offset_low}",
            "ldr l a",
            f"ldr a {base_high}",
            f"{offset_operation} cc {offset_high}",
            "ldr h a",
        ]

        return variable

    def visitIfStmt(self, ctx: StornParser.IfStmtContext):
        expression = self.visitExpression(ctx.expression())
        if not isinstance(expression, BaseType):
            raise CompileError("If condition expression evaluates to non numeric type", ctx.expression().start.line, ctx.expression().start.column)

        fail_label = self.label_count
        final_label = self.label_count + 1
        self.label_count += 2

        if expression.width == 8:
            self.instructions += [
                "pop a",
                f"jmp zf L{fail_label}"
            ]
        elif expression.width == 16:
            self.instructions += [
                "pop b",
                "pop a",
                "or b",
                f"jmp zf L{fail_label}"
            ]

        self.visitStatements(ctx.statements())
        self.instructions += [
            f"jmp L{final_label}",
            f"L{fail_label}:",
        ]

        if ctx.elifStmt():
            for elif_stmt in ctx.elifStmt():
                expression = self.visitExpression(elif_stmt.expression())
                if not isinstance(expression, BaseType):
                    raise CompileError("Elif condition expression evaluates to non numeric type", elif_stmt.expression().start.line, elif_stmt.expression().start.column)

                fail_label = self.label_count
                self.label_count += 1

                if expression.width == 8:
                    self.instructions += [
                        "pop a",
                        f"jmp zf L{fail_label}"
                    ]
                elif expression.width == 16:
                    self.instructions += [
                        "pop b",
                        "pop a",
                        "or b",
                        f"jmp zf L{fail_label}"
                    ]

                self.visitStatements(elif_stmt.statements())
                self.instructions += [
                    f"jmp L{final_label}",
                    f"L{fail_label}:",
                ]

        if ctx.elseStmt():
            self.visitStatements(ctx.elseStmt().statements())

        self.instructions += [
            f"L{final_label}:",
        ]

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

    def visitContinueStmt(self, ctx: StornParser.ContinueStmtContext):
        # See visitBreakStmt
        self.instructions += [
            f"jmp L{self.loop_label_stack[-1]}"
        ]

    def visitCall(self, ctx: StornParser.CallContext) -> Type:
        routine_name = ctx.NAME().getText()
        if routine_name in self.routine_table:
            routine = self.routine_table[routine_name]
        else:
            raise CompileError("Reference to unknown routine", ctx.NAME().start.line, ctx.NAME().start.column)

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

        parameters = ctx.parameters().expression()
        expected_parameter_types = self.routine_table[routine_name].parameters.values()

        total_parameter_size = 0
        for parameter, expected_parameter_type in zip(reversed(parameters), reversed(expected_parameter_types)):
            parameter_type = self.visitExpression(parameter)
            if parameter_type != expected_parameter_type:
                raise CompileError("Parameter expression is an inconsistent type with routine expectation", parameter.start.line, parameter.start.column)
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
                raise CompileError("Return type doesn't matched expectation for routine", ctx.expression().start.line, ctx.expression().start.column)

            # Pop expression result from stack to caller-allocated return space on stack
            # Start of caller-allocated return space is at: BP + 1 (caller BPH) + 2 (return addr) + param size
            # Pop and increment
            # | 0x0000 |
            # |  ....  |
            # | LOCAL1 | <- SP
            # | LOCAL0 | <- local 0 offset
            # | BPL    | <- BP points here
            # | BPH    |
            # | RETURN | <- return low
            # | RETURN | <- return high
            # | PARAM0 | <- param 0 offset
            # | PARAM0 |
            # | PARAM0 |
            # | PARAM1 | <- param 1 offset
            # | RETVAL | <- return value space highest byte
            # | RETVAL |
            # | RETVAL | <- return value space lowest byte
            # |  ....  |
            # | 0xFFFF |
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
        expression = self.visitBitwiseExpr(ctx.bitwiseExpr(0))

        bitwise_count = (ctx.getChildCount() - 1) // 2
        for i in range(bitwise_count):
            if not isinstance(expression, BaseType):
                raise CompileError("Attempting to perform logical operation on non numerical type", ctx.bitwiseExpr(i).start.line, ctx.bitwiseExpr(i).start.line)
            next_expression = self.visitBitwiseExpr(ctx.bitwiseExpr(i + 1))
            if not isinstance(next_expression, BaseType):
                raise CompileError("Attempting to perform logical operation on non numerical type", ctx.bitwiseExpr(i + 1).start.line, ctx.bitwiseExpr(i + 1).start.column)
            if expression.width != next_expression.width:
                raise CompileError("Attempting to perform logical operation on expressions of differing width", ctx.logicalOp(i).start.line, ctx.logicalOp(i).start.column)

            operation = ctx.logicalOp(i)
            width = expression.width
            if operation.AND():
                operation_instruction = "and b"
            else:
                operation_instruction = "or b"
            if width == 8:
                self.instructions += [
                    "pop a",
                    f"jmp nzf L{self.label_count}",
                    "ldr b a", # ie. ldr b 0
                    f"jmp L{self.label_count + 1}",
                    f"L{self.label_count}:",
                    "ldr b 1",
                    f"L{self.label_count + 1}:",
                    "pop a",
                    f"jmp zf L{self.label_count + 2}",
                    "ldr a 1",
                    f"L{self.label_count + 2}:",
                    operation_instruction,
                    f"jmp nzf L{self.label_count + 3}",
                    "psh 0",
                    f"jmp L{self.label_count + 4}",
                    f"L{self.label_count + 3}:",
                    "psh 1",
                    f"L{self.label_count + 4}:",
                ]
                self.label_count += 5
            elif width == 16: # TODO: implement me!
                raise CompileError("Logical operations not yet implemented for 16-bit-wide values")
            expression = next_expression

        return expression

    def visitBitwiseExpr(self, ctx: StornParser.BitwiseExprContext) -> Type:
        expression = self.visitComparativeExpr(ctx.comparativeExpr(0))

        comparative_count = (ctx.getChildCount() - 1) // 2
        for i in range(comparative_count):
            if not isinstance(expression, BaseType):
                raise CompileError("Attempting to perform bitwise operation on non numerical type", ctx.comparativeExpr(i).start.line, ctx.comparativeExpr(i).start.line)
            next_expression = self.visitComparativeExpr(ctx.comparativeExpr(i + 1))
            if not isinstance(next_expression, BaseType):
                raise CompileError("Attempting to perform bitwise operation on non numerical type", ctx.comparativeExpr(i + 1).start.line, ctx.comparativeExpr(i + 1).start.column)
            if expression.width != next_expression.width:
                raise CompileError("Attempting to perform bitwise operation on expressions of differing width", ctx.bitwiseOp(i).start.line, ctx.bitwiseOp(i).start.column)

            operation = ctx.bitwiseOp(i)
            width = expression.width
            if operation.DIS():
                operation_instruction = "or b"
            elif operation.CON():
                operation_instruction = "and b"
            else:
                operation_instruction = "xor b"
            if width == 8:
                self.instructions += [
                    "pop b",
                    "pop a",
                    operation_instruction,
                    "psh a",
                ]
            elif width == 16:
                # for x:16 & y:16,
                # Stack is:
                # | Y LOW  | <- top of stack
                # | Y HIGH |
                # | X LOW  |
                # | X HIGH |
                # and we want to finish with stack like:
                # | Y LOW & X LOW   | <- top of stack
                # | Y HIGH & X HIGH |
                self.instructions += [
                    "pop b",
                    "pop c",
                    "pop a",
                    operation_instruction,
                    "ldr b c",
                    "ldr c a",
                    "pop a",
                    operation_instruction,
                    "psh a",
                    "psh c",
                ]
            expression = next_expression

        return expression

    def visitComparativeExpr(self, ctx: StornParser.ComparativeExprContext) -> Type:
        expression = self.visitArithmeticExpr(ctx.arithmeticExpr(0))

        arithmetic_count = (ctx.getChildCount() - 1) // 2
        for i in range(arithmetic_count):
            if not isinstance(expression, BaseType):
                raise CompileError("Attempting to perform comparative operation on non numerical type", ctx.arithmeticExpr(i).start.line, ctx.arithmeticExpr(i).start.column)
            next_expression = self.visitArithmeticExpr(ctx.arithmeticExpr(i + 1))
            if not isinstance(next_expression, BaseType):
                raise CompileError("Attempting to perform comparative operation on non numerical type", ctx.arithmeticExpr(i + 1).start.line, ctx.arithmeticExpr(i + 1).start.column)
            if expression.width != next_expression.width:
                raise CompileError("Attempting to perform comparative operation on expressions of differing width", ctx.comparativeOp(i).start.line, ctx.comparativeOp(i).start.column)

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
                if operation.EQ():
                    # x - y
                    self.instructions += [
                        "pop b", # y low
                        "pop h", # y high
                        "pop a", # x low
                        "sub b", # x low - y low
                        f"jmp nzf L{self.label_count}",
                        "pop a", # x high
                        "sub h", # x high - y high
                        f"jmp zf L{self.label_count + 1}",
                        f"L{self.label_count}:",
                        "psh 0",
                        "psh 0",
                        f"jmp L{self.label_count + 2}",
                        f"L{self.label_count + 1}:",
                        "psh 0",
                        "psh 1",
                        f"L{self.label_count + 2}:",
                    ]
                    self.label_count += 3
                else: # TODO: I'd be surprised if this works
                    self.instructions += [
                        pop_ops[0],
                        "pop h",
                        pop_ops[1],
                        "sub b",
                        pop_ops[1],
                        f"ldr {pop_ops[0][-1]} h",
                        "sub cc b",
                        f"jmp {flag} L{self.label_count}",
                        "psh 0",
                        "psh 0",
                        f"jmp L{self.label_count + 1}",
                        f"L{self.label_count}:",
                        "psh 0",
                        "psh 1",
                        f"L{self.label_count + 1}:",
                    ]
                    self.label_count += 2

            expression = next_expression

        return expression

    def visitArithmeticExpr(self, ctx: StornParser.ArithmeticExprContext) -> Type:
        expression = self.visitShiftExpr(ctx.shiftExpr(0))

        shift_count = (ctx.getChildCount() - 1) // 2
        for i in range(shift_count):
            if not isinstance(expression, BaseType):
                raise CompileError("Attempting to perform additive operation on non numerical type", ctx.shiftExpr(i).start.line, ctx.shiftExpr(i).start.column)
            next_expression = self.visitShiftExpr(ctx.shiftExpr(i + 1))
            if not isinstance(next_expression, BaseType):
                raise CompileError("Attempting to perform additive operation on non numerical type", ctx.shiftExpr(i + 1).start.line, ctx.shiftExpr(i + 1).start.column)
            if expression.width != next_expression.width:
                raise CompileError("Attempting to perform additive operation on expressions of differing width", ctx.shiftExpr(i).start.line, ctx.shiftExpr(i).start.column)

            operation = ctx.arithmeticOp(i)
            width = expression.width
            if operation.PLUS():
                operation_instruction = "add"
            else:
                operation_instruction = "sub"
            if width == 8:
                self.instructions += [
                    "pop b",
                    "pop a",
                    f"{operation_instruction} b",
                    "psh a",
                ]
            elif width == 16:
                self.instructions += [
                    "pop l",
                    "pop h",
                    "pop a",
                    f"{operation_instruction} l",
                    "ldr l a",
                    "pop a",
                    f"{operation_instruction} cc h",
                    "psh a",
                    "psh l",
                ]
            expression = next_expression

        return expression

    def visitShiftExpr(self, ctx: StornParser.ShiftExprContext) -> Type:
        expression = self.visitMultiplicativeExpr(ctx.multiplicativeExpr(0))

        multiplicative_count = (ctx.getChildCount() - 1) // 2
        for i in range(multiplicative_count):
            if not isinstance(expression, BaseType):
                raise CompileError("Attempting to perform shift operation on non numerical type", ctx.multiplicativeExpr(i).start.line, ctx.multiplicativeExpr(i).start.column)
            next_expression = self.visitMultiplicativeExpr(ctx.multiplicativeExpr(i + 1))
            if not isinstance(next_expression, BaseType):
                raise CompileError("Attempting to perform shift operation on non numerical type", ctx.multiplicativeExpr(i + 1).start.line, ctx.multiplicativeExpr(i + 1).start.column)
            if next_expression.width != 8:
                raise CompileError("Attempting to shift by 16-bit-width expression. Can only shift by 8-bit expression", ctx.multiplicativeExpr(i).start.line, ctx.multiplicativeExpr(i).start.column)

            operation = ctx.shiftOp(i)
            width = expression.width
            if operation.SHR():
                operation_instruction = "shr"
            else:
                if width == 16:
                    raise CompileError("<< not currently supported for 16-bit-wide values", operation.start.line, operation.start.column)
                operation_instruction = "shl"
            if width == 8:
                self.instructions += [
                    "pop c",
                    "pop b",
                    f"L{self.label_count}:",
                    "ldr a c",
                    f"jmp zf L{self.label_count + 1}",
                    "ldr a b",
                    operation_instruction,
                    "ldr b a",
                    "ldr a c",
                    "dec",
                    "ldr c a",
                    f"jmp L{self.label_count}",
                    f"L{self.label_count + 1}:",
                    "psh b",
                ]
                self.label_count += 2
            elif width == 16: # TODO: implement me!
                raise CompileError("Shift operations not yet implemented for 16-bit-wide values")
            expression = next_expression

        return expression

    def visitMultiplicativeExpr(self, ctx: StornParser.MultiplicativeExprContext) -> Type:
        expression = self.visitUnaryExpr(ctx.unaryExpr(0))

        unary_count = (ctx.getChildCount() - 1) // 2
        for i in range(unary_count):
            if not (isinstance(expression, BaseType) and expression.width == 8):
                raise CompileError("Attempting to multiply expression not of type [8]", ctx.unaryExpr(i).start.line, ctx.unaryExpr(i).start.column)
            next_expression = self.visitUnaryExpr(ctx.unaryExpr(i + 1))
            if not (isinstance(next_expression, BaseType) and next_expression.width == 8):
                raise CompileError("Attempting to multiply expression not of type [8]", ctx.unaryExpr(i + 1).start.line, ctx.unaryExpr(i + 1).start.column)

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
        if ctx.primaryExpr():
            expression = self.visitPrimaryExpr(ctx.primaryExpr())
        else:
            expression = self.visitUnaryExpr(ctx.unaryExpr())

        if ctx.MINUS() or ctx.NOT():
            if not isinstance(expression, BaseType):
                raise CompileError("Attempting to perform unary operation on non numerical type", ctx.MINUS().start.line, ctx.MINUS().start.column)

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
        elif ctx.type_():
            type_ = self.visitType(ctx.type_())
            if isinstance(expression, BaseType) and isinstance(type_, BaseType):
                current_width = expression.width
                new_width = type_.width

                if current_width == new_width:
                    return expression

                if new_width == 8: # narrowing
                    self.instructions += [
                        "pop a",
                        "pop b",
                        "psh a",
                    ]
                elif new_width == 16: # promotion
                    self.instructions += [
                        "pop a",
                        "psh 0",
                        "psh a",
                    ]

                return BaseType(new_width)

            if expression.size != type_.size:
                raise CompileError("Attempting to cast non numeric type to different size", ctx.type_().start.line, ctx.type_().start.column)

            return type_

        return expression

    def visitPrimaryExpr(self, ctx: StornParser.PrimaryExprContext) -> Type:
        if ctx.expression():
            return self.visitExpression(ctx.expression())
        elif ctx.call():
            call_return_type = self.visitCall(ctx.call())
            return call_return_type
        elif ctx.lvalue():
            lvalue = self.visitLvalue(ctx.lvalue())

            # Push bytes from memory range [HL, HL + (size - 1)] to stack
            # Note that bytes are pushed in reverse order, starting from HL + (size - 1)
            offset = lvalue.size - 1
            offset_low = offset & 0b11111111
            offset_high = offset >> 8
            self.instructions += [
                "ldr a l",
                f"add {offset_low}",
                "ldr l a",
                "ldr a h",
                f"add cc {offset_high}",
                "ldr h a",
                f"ldr c {lvalue.size}",
                f"L{self.label_count}:",
                "ldr a c",
                f"jmp zf L{self.label_count + 1}",
                "dec",
                "ldr c a",
                "ldr a m",
                "psh a",
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

            return lvalue
        elif ctx.CONSTANT():
            constant = int(ctx.CONSTANT(0).getText())
            width = int(ctx.CONSTANT(1).getText())

            if width == 8:
                self.instructions += [
                    f"psh {constant}"
                ]
            elif width == 16:
                constant_low = constant & 0b11111111
                constant_high = constant >> 8
                self.instructions += [
                    f"psh {constant_high}",
                    f"psh {constant_low}",
                ]
            else:
                raise CompileError("Invalid width", ctx.CONSTANT(1).start.line, ctx.CONSTANT(1).start.column)

            return BaseType(width)
        elif ctx.type_():
            type_ = self.visitType(ctx.type_())
            type_.calculate_size(self.data_table)

            size = type_.size
            size_low = size & 0b11111111
            size_high = size >> 8
            self.instructions += [
                f"psh {size_high}",
                f"psh {size_low}",
            ]

            return BaseType(16)
        else:
            raise Exception("Unknown primary expression type")

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

