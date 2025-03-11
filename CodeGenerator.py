from typing import Dict, List, Literal, Union
from storn.StornVisitor import StornVisitor
from storn.StornParser import StornParser

class Type:
    def resolve(self, data_table: Dict[str, "DataType"]):
        pass

    def __repr__(self, seen=None) -> str:
        return ""

class TypedVar:
    def __init__(self, name: str, type_: Union[Type, str]):
        self.name = name
        self.type_ = type_

    def resolve(self, data_table: Dict[str, "DataType"]):
        if isinstance(self.type_, str):
            if self.type_ in data_table:
                self.type_ = data_table[self.type_]
            else:
                raise Exception(f"Couldn't find type {self.type_}")
        else:
            self.type_.resolve(data_table)

    def __repr__(self) -> str:
        return f"{self.name}: {self.type_}"

class BaseType(Type):
    def __init__(self, width: Literal[0, 8, 16]):
        self.width = width

    def __repr__(self, seen=None) -> str:
        return f"[{self.width}]"

class DataType(Type):
    def __init__(self, name: str, fields: List[TypedVar]):
        self.name = name
        self.fields = fields

    def resolve(self, data_table: Dict[str, "DataType"]):
        for field in self.fields:
            if isinstance(field.type_, str) and field.type_ == self.name:
                raise Exception("Inconsistent self-referential data type")
            field.resolve(data_table)

    def __repr__(self, seen=None):
        if seen is None:
            seen = set()
        if self.name in seen:
            return f"data {self.name} {{ ... }}"
        seen.add(self.name)
        return f"data {self.name} {{ " + ", ".join(
            f"{f.name}: {f.type_.__repr__(seen) if isinstance(f.type_, Type) else f.type_}"
            for f in self.fields
        ) + " }"

class ReferenceType(Type):
    def __init__(self, type_: Type):
        self.type_ = type_

    def resolve(self, data_table: Dict[str, "DataType"]):
        if isinstance(self.type_, str):
            if self.type_ in data_table:
                self.type_ = data_table[self.type_]
            else:
                raise Exception(f"Couldn't find type {self.type_}")
        else:
            self.type_.resolve(data_table)

    def __repr__(self, seen=None):
        if isinstance(self.type_, str):
            return f"<[{self.type_}]>"
        return f"<{self.type_.__repr__(seen)}>"

class ArrayType(Type):
    def __init__(self, type_: Type, length: int):
        self.type_ = type_
        self.length = length

    def resolve(self, data_table: Dict[str, "DataType"]):
        if isinstance(self.type_, str):
            if self.type_ in data_table:
                self.type_ = data_table[self.type_]
            else:
                raise Exception(f"Couldn't find type {self.type_}")
        else:
            self.type_.resolve(data_table)

    def __repr__(self, seen=None):
        if isinstance(self.type_, str):
            return f"[{self.type_}] ^ {self.length}"
        return f"{self.type_.__repr__(seen)} ^ {self.length}"

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

        data_type = DataType(name, fields)
        self.data_table[name] = data_type
        data_type.resolve(self.data_table)

        print(self.data_table[name])
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
            return name
        elif ctx.CONSTANT(): # Array type
            type_ = self.visitType(ctx.type_())
            length = int(ctx.CONSTANT().getText())
            return ArrayType(type_, length)
        else: # Reference type
            type_ = self.visitType(ctx.type_())
            return ReferenceType(type_)

