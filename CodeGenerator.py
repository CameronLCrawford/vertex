from typing import Dict, List, Literal
from storn.StornVisitor import StornVisitor
from storn.StornParser import StornParser

class Type:
    pass

class TypedVar:
    def __init__(self, name: str, type_: Type):
        self.name = name
        self.type_ = type_

    def __repr__(self) -> str:
        return f"{self.name}: {self.type_}"

class BaseType(Type):
    def __init__(self, width: Literal[0, 8, 16]):
        self.width = width

    def __repr__(self) -> str:
        return f"[{self.width}]"

class DataType(Type):
    def __init__(self, fields: List[TypedVar]):
        self.fields = fields

    def __repr__(self) -> str:
        return ", ".join([field.__repr__() for field in self.fields])

class ReferenceType(Type):
    def __init__(self, type_: Type):
        self.type_ = type_

    def __repr__(self) -> str:
        return f"<{self.type_}>"

class ArrayType(Type):
    def __init__(self, type_: Type, length: int):
        self.type_ = type_
        self.length = length

    def __repr__(self) -> str:
        return f"{self.type_} ^ {self.length}"

class CodeGenerator(StornVisitor):
    def __init__(self):
        self.instructions = []
        self.data_table: Dict[str, DataType] = {}

    def visitData(self, ctx: StornParser.DataContext):
        name = ctx.NAME().getText()
        declarations = ctx.typeDeclaration()

        fields: List[TypedVar] = []
        for declaration in declarations:
            fields.append(self.visitTypeDeclaration(declaration))

        self.data_table[name] = DataType(fields)
        print(name, self.data_table[name])
        return None

    def visitTypeDeclaration(self, ctx: StornParser.TypeDeclarationContext):
        return self.visitTypedVar(ctx.typedVar())

    def visitTypedVar(self, ctx: StornParser.TypedVarContext):
        name = ctx.NAME().getText()
        type_ = self.visitType(ctx.type_())
        return TypedVar(name, type_)

    def visitType(self, ctx: StornParser.TypeContext):
        if ctx.getChildCount() == 1: # Base
            text = ctx.getText()
            width = text[1:-1]
            return BaseType(width)
        elif ctx.NAME(): # Name type to be resolved
            name = ctx.NAME().getText()
            return self.data_table[name]
        elif ctx.CONSTANT(): # Array type
            type_ = self.visitType(ctx.type_())
            length = int(ctx.CONSTANT().getText())
            return ArrayType(type_, length)
        else: # Reference type
            type_ = self.visitType(ctx.type_())
            return ReferenceType(type_)

