from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Node:
    line: int = 0
    def str(self, n):
        return f'{n*" "}#{self.line}\n'

@dataclass
class IterableNode(Node):
    seq: List = field(default_factory=list)

@dataclass
class Program(IterableNode):
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_program\n'
        res += ''.join([c.str(n+2) for c in self.seq])
        return res

@dataclass
class Class(Node):
    visibility: str = '_no_set'
    static: bool = False
    name: str = '_no_set'
    member_list: List = field(default_factory=list)
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_class: {self.name}\n'
        res += ''.join([m.str(n+2) for m in self.member_list])
        return res

@dataclass
class Field(Node):
    visibility: str = '_no_set'
    static: bool = False
    type: str = '_no_set'
    name: str = '_no_set'
    value: 'Expr' = None
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_field: {self.name}\n'
        res += f'{" "*n}type: {self.type}\n'
        if self.value:
            res += f'{" "*n}value:\n'
            res += self.value.str(n+2)
        return res

@dataclass
class Method(Node):
    javadoc: 'Javadoc' = None
    visibility: str = '_no_set'
    static: bool = False
    return_type: str = '_no_set'
    name: str = '_no_set'
    params_list: List = field(default_factory=list)
    instructions_list: List = field(default_factory=list)
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_method: {self.name}\n'
        res += f'{" "*n}return_type: {self.return_type}\n'
        res += ''.join([a.str(n+2) for a in self.params_list])
        res += ''.join([i.str(n+2) for i in self.instructions_list])
        return res

@dataclass
class Expr(Node):
    pass

@dataclass
class Param(Node):
    type: str = '_no_set'
    name: str = '_no_set'
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_param: {self.name}\n'
        res += f'{" "*n}type: {self.type}\n'
        return res

@dataclass
class Conditional(Expr):
    condition: Expr = None
    then_do: Expr = None
    else_do: Expr = None
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_if\n'
        res += f'{" "*n}condition:\n'
        res += self.condition.str(n+2)
        res += f'{" "*n}then:\n'
        res += ''.join([s.str(n+2) for s in self.then_do])
        res += f'{" "*n}else:\n'
        if self.else_do:
            res += ''.join([s.str(n+2) for s in self.else_do])
        return res

@dataclass
class While(Expr):
    condition: Expr = None
    body: List = field(default_factory=list)
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_while\n'
        res += f'{" "*n}condition:\n'
        res += self.condition.str(n+2)
        res += f'{" "*n}body:\n'
        res += ''.join([s.str(n+2) for s in self.body])
        return res

@dataclass
class For(Expr):
    initial: Expr = None
    condition: Expr = None
    update: Expr = None
    body: List = field(default_factory=list)
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_for\n'
        res += f'{" "*n}initial:\n'
        res += self.initial.str(n+2)
        res += f'{" "*n}condition:\n'
        res += self.condition.str(n+2)
        res += f'{" "*n}update:\n'
        res += self.update.str(n+2)
        res += f'{" "*n}body:\n'
        res += ''.join([s.str(n+2) for s in self.body])
        return res

@dataclass
class DoWhile(Expr):
    condition: Expr = None
    body: List = field(default_factory=list)
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_dowhile\n'
        res += f'{" "*n}body:\n'
        res += ''.join([s.str(n+2) for s in self.body])
        res += f'{" "*n}condition:\n'
        res += self.condition.str(n+2)
        return res

@dataclass
class VariableDeclaration(Expr):
    type: str = '_no_set'
    name: str = '_no_set'
    value: Expr = None
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_var: {self.name}\n'
        res += f'{" "*n}type: {self.type}\n'
        if self.value:
            res += f'{" "*n}value:\n'
            res += self.value.str(n+2)
        return res
    
@dataclass
class Assign(Expr):
    name: str = '_no_set'
    value: Expr = None
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_assign: {self.name}\n'
        res += f'{" "*n}value:\n'
        res += self.value.str(n+2)
        return res

@dataclass
class CompoundAssign(Expr):
    name: str = '_no_set'
    operator: str = '_no_set'
    value: Expr = None
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_cassign: {self.name}\n'
        res += f'{" "*n}operator: {self.operator}\n'
        res += f'{" "*n}value:\n'
        res += self.value.str(n+2)
        return res
    
@dataclass
class ExprOp(Expr):
    operation: str = '_no_set'
    value: Expr = None
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_exprOp:\n'
        res += f'{" "*n}operation: {self.operation}\n'
        res += f'{" "*n}value:\n'
        res += self.value.str(n+2)
        return res
    
@dataclass
class BinaryOp(Expr):
    operation: str = '_no_set'
    op_left: Expr = None
    op_right: Expr = None
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_binaryOp:\n'
        res += f'{" "*n}operation: {self.operation}\n'
        res += f'{" "*n}op_left:\n'
        res += self.op_left.str(n+2)
        res += f'{" "*n}op_right:\n'
        res += self.op_right.str(n+2)
        return res

@dataclass
class Return(Expr):
    value: Expr = None
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_return\n'
        res += f'{" "*n}value:\n'
        if self.value:
            res += self.value.str(n+2)
        return res

@dataclass
class Int(Expr):
    value: int = 0
    def str(self, n):
        res = super().str(n)
        res += f'{(n)*" "}_int\n'
        res += f'{(n+2)*" "}{self.value}\n'
        return res
    
@dataclass
class Float(Expr):
    value: float = 0.0
    def str(self, n):
        res = super().str(n)
        res += f'{(n)*" "}_float\n'
        res += f'{(n+2)*" "}{self.value}\n'
        return res
    
@dataclass
class Boolean(Expr):
    value: bool = False
    def str(self, n):
        res = super().str(n)
        res += f'{(n)*" "}_boolean\n'
        res += f'{(n+2)*" "}{self.value}\n'
        return res

@dataclass
class String(Expr):
    value: str = ''
    def str(self, n):
        res = super().str(n)
        res += f'{(n)*" "}_string\n'
        res += f'{(n+2)*" "}{self.value}\n'
        return res

@dataclass
class Char(Expr):
    value: str = ''
    def str(self, n):
        res = super().str(n)
        res += f'{(n)*" "}_char\n'
        res += f'{(n+2)*" "}{self.value}\n'
        return res
    
@dataclass
class Null(Expr):
    def str(self, n):
        res = super().str(n)
        res += f'{(n)*" "}_null\n'
        return res
    
@dataclass
class InlineComment(Node):
    contents: str = '_no_set'
    def str(self, n):
        res = super().str(n)
        res += f'{(n)*" "}_inline_comment\n'
        res += f'{(n)*" "}contents: {self.contents}\n'
        return res

@dataclass
class MultilineComment(Node):
    contents: str = '_no_set'
    def str(self, n):
        res = super().str(n)
        res += f'{(n)*" "}_multiline_comment\n'
        res += f'{(n)*" "}contents: {self.contents}\n'
        return res
    
@dataclass
class Javadoc(Node):
    contents: str = '_no_set'
    def str(self, n):
        res = super().str(n)
        res += f'{(n)*" "}_javadoc\n'
        res += f'{(n)*" "}contents: {self.contents}\n'
        return res
    
@dataclass
class VarRef(Expr):
    name: str = '_no_set'
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_varref: {self.name}\n'
        return res
    
@dataclass
class MethodCall(Expr):
    object: str = '_no_set'
    method_name: str = '_no_set'
    params: List = field(default_factory=list)
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_methodCall: {self.object}.{self.method_name}\n'
        res += ''.join([p.str(n+2) for p in self.params])
        return res
    
@dataclass
class NewArray(Expr):
    type: str = '_no_set'
    items: List = field(default_factory=list)
    def str(self, n):
        res = super().str(n)
        res += f'{" "*n}_newarray\n'
        res += f'{" "*n}type: {self.type}\n'
        res += f'{" "*n}items:\n'
        res += ''.join([i.str(n+2) for i in self.items])
        return res