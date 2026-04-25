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
            VariableDeclaration: self.translate_variable_declaration,
            BinaryOp: self.translate_binary_op,
            Return: self.translate_return,
            Javadoc: self.translate_javadoc,
            VarRef: self.translate_varref,
            Conditional: self.translate_conditional,
            Int: self.translate_int,
        }
    
    def translate(self, node):
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
        for member in node.member_list:
            result += self.indentation(self.indent_level) + f"class {node.name}:"
            result += result.join(self.translate(member))
        return result
    
    def translate_field(self, node):
        result = self.indentation(self.indent_level) + f"{node.name} = "
        result += result.join(self.translate(node.value))
        return self.indentation(self.indent_level).join(result)
    
    def translate_method(self, node):
        result = self.indentation(self.indent_level) + f"\"\"\"{self.translate_javadoc}\"\"\""
        result += self.indentation(self.indent_level) + f"def {node.name}("
        if node.params_list:
            result += f"{self.translate(node.params_list[0])}"
        if len(node.params_list) > 1:
            for param in node.params_list[1:]:
                result += ", "
                result += f"{self.translate(param)}"
        result += self.indentation(self.indent_level) + "):"
        self.indent_level += 1
        for i in node.instructions_list:
                result += self.indentation(self.indent_level).join(self.translate(i))
        return result
    
    def translate_param(self, node):
        return f"{node.name}: {node.type}"
    
    def translate_conditional(self, node, inside_else=False):
        if inside_else:
            result = self.indentation(self.indent_level) + f"{self.translate(node.condition)}:"
        else:
            result = self.indentation(self.indent_level) + f"if {self.translate(node.condition)}:"

        self.indent_level += 1
        result += self.indentation(self.indent_level) + f"{self.translate(node.then_do)}"
        self.indent_level -= 1
        if isinstance(self.else_do, Conditional):
            result += self.indentation(self.indent_level) + f"elif {self.translate(node.else_do, True)}:"
        else:
            result += self.indentation(self.indent_level) + f"else:"
            self.indent_level += 1
            result += self.indentation(self.indent_level) + f"{self.translate(node.else_do)}"
            self.indent_level += 1
        return result
    
    def translate_variable_declaration(self, node):
        return f"{node.name} = {self.translate(node.value)}"

    def translate_return(self, node):
        return self.translate(node.value)
    
    def translate_javadoc(self, node):
        return node.contents.strip("/**", "*/")
    
    def translate_varref(self, node):
        return node.name
    
    def translate_binary_op(self, node):
        left = self.translate(node.op_left)
        right = self.translate(node.op_right)
        return f"{left} {node.operation} {right}"
    
    def translate_int(self, node):
        return str(node.value)
    
    def translate_float(self, node):
        return str(node.value).strip("f")