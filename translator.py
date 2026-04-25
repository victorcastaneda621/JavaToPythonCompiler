from classes import *

class Translator():
    def __init__(self):
        self.indent_level = -1

        self.equivalents = {
            Program: self.translate_program,
            Class: self.translate_class,
            Field: self.translate_field,
            Method: self.translate_method,
            Param: self.translate_param,
            Conditional: self.translate_conditional,
            #While
            #For
            #DoWhile
            VariableDeclaration: self.translate_variable_declaration,
            #Assign
            #CompoundAssign
            #ExprOp
            BinaryOp: self.translate_binary_op,
            Return: self.translate_return,
            Int: self.translate_int,
            Float: self.translate_float,
            Boolean: self.translate_boolean,
            #String
            #Char
            #Null
            #InlineComment
            #MultilineComment
            Javadoc: self.translate_javadoc,
            VarRef: self.translate_varref,
            #MethodCall
            #NewArray
        }
    
    def translate(self, node):
        #print(node)
        #print(type(node), self.indent_level)
        if node is None:
            return ""
        current_eq = self.equivalents.get(type(node))
        return current_eq(node)
    
    def indentation(self, n):
        return "\n" + "    "*n
    
    # Specific handlers for each type of node in the AST

    def translate_program(self, node):
        result = ""
        for java_class in node.seq:
            result += self.translate(java_class) 
        return result
    
    def translate_class(self, node):
        self.indent_level += 1
        result = ""
        result += self.indentation(self.indent_level) + f"class {node.name}:"
        self.indent_level += 1
        for member in node.member_list:
            result += self.indentation(self.indent_level) + self.translate(member)
        self.indent_level -= 2
        return result
    
    def translate_field(self, node):
        result = f"{node.name} = "
        if node.value:
            result += self.translate(node.value)
        return result
    
    def translate_method(self, node):
        self.indent_level += 1
        if node.javadoc:
            result = self.indentation(self.indent_level) + f"\"\"\"{self.translate(node.javadoc)}\"\"\""
        else:
            result = ""

        if node.static:
            result += self.indentation(self.indent_level) + "@staticmethod"

        result += self.indentation(self.indent_level) + f"def {node.name}("

        if not node.static:
            result += f"self, "

        if node.params_list:
            result += f"{self.translate(node.params_list[0])}"
        if len(node.params_list) > 1:
            for param in node.params_list[1:]:
                result += ", "
                result += f"{self.translate(param)}"

        result += "):"
        self.indent_level += 1
        for i in node.instructions_list:
                result += self.indentation(self.indent_level) + self.translate(i)
        self.indent_level -= 2
        return result
    
    def translate_param(self, node):
        if node.type == "boolean":
            ntype = "bool"
        else:
            ntype = node.type
        return f"{node.name}: {ntype}"
    
    def translate_conditional(self, node, inside_else=False):
        if inside_else:
            result = f"{self.translate(node.condition)}:"
        else:
            result = f"if {self.translate(node.condition)}:"

        self.indent_level += 1
        for item in node.then_do:
            result += self.indentation(self.indent_level) + f"{self.translate(item)}"
        self.indent_level -= 1

        if node.else_do:
            for item in node.else_do:
                if isinstance(item, Conditional):
                    result += self.indentation(self.indent_level) + f"elif {self.translate_conditional(item, True)}:"
                else:
                    result += self.indentation(self.indent_level) + f"else:"
                    self.indent_level += 1
                    result += self.indentation(self.indent_level) + f"{self.translate(item)}"
                    self.indent_level -= 1
        return result
    
    # WHILE, FOR, DOWHILE
    
    def translate_variable_declaration(self, node):
        return f"{node.name} = {self.translate(node.value)}"
    
    # ASSIGN, COMPOUNDASSIGN, EXPROP
    
    def translate_binary_op(self, node):
        left = self.translate(node.op_left)
        right = self.translate(node.op_right)

        match(node.operation):
            case "&&":
                op = "and"
            case "||":
                op = "or"
            case _:
                op = node.operation
        
        return f"{left} {op} {right}"
    
    def translate_return(self, node):
        return "return " + self.translate(node.value)
    
    def translate_int(self, node):
        return str(node.value).replace("L", "")
    
    def translate_float(self, node):
        return str(node.value).replace("f", "")
    
    def translate_boolean(self, node):
        return str(node.value)[0].upper() + str(node.value)[1:]
    
    # string, char, null, inline, multiline
    
    def translate_javadoc(self, node):
        return node.contents.replace("/**", "").replace("*/", "")
    
    def translate_varref(self, node):
        return node.name
    
    # methodcall, newarray