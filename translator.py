from classes import *
from scope import Scope

class Translator():
    def __init__(self):
        self.indent_level = 0
        self.scope = None

        self.equivalents = {
            Program: self.translate_program,
            Class: self.translate_class,
            Field: self.translate_field,
            Method: self.translate_method,
            Param: self.translate_param,
            Conditional: self.translate_conditional,
            While: self.translate_while,
            For: self.translate_for,
            DoWhile: self.translate_do_while,
            VariableDeclaration: self.translate_variable_declaration,
            Assign: self.translate_assign,
            CompoundAssign: self.translate_compound_assign,
            ExprOp: self.translate_expr_op,
            BinaryOp: self.translate_binary_op,
            Return: self.translate_return,
            Int: self.translate_int,
            Float: self.translate_float,
            Boolean: self.translate_boolean,
            String: self.translate_string,
            Char: self.translate_char,
            Null: self.translate_null,
            InlineComment: self.translate_inline,
            MultilineComment: self.translate_multiline,
            Javadoc: self.translate_javadoc,
            VarRef: self.translate_varref,
            MethodCall: self.translate_method_call,
            NewArray:self.translate_new_array,
        }

    precedence_binary_op = {
            '*': 3, '/': 3, '%': 3,
            '+': 4, '-': 4,
            '<<': 5, '>>': 5, '>>>': 5,
            '<': 6, '<=': 6, '>': 6, '>=': 6,
            '==': 7, '!=': 7,
            '&': 8,
            '^': 9,
            '|': 10,
            '&&': 11,
            '||': 12
        }

    def translate_initial(self, node, scope: Scope):
        self.scope = scope
        for java_class in node.seq: 
            self.scope.register_class(java_class)
        return self.translate(node)
    
    def indentation(self, n):
        return "\n" + "    "*n
    
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
        self.scope.current_class = node.name
        result = ""
        result += self.indentation(self.indent_level) + f"class {node.name}:"
        self.indent_level += 1
        for member in node.member_list:
            result += self.indentation(self.indent_level) + self.translate(member)
        self.indent_level -= 1
        return result
    
    def translate_field(self, node):
        result = f"{node.name} = "
        if node.value:
            result += self.translate(node.value)
        return result
    
    def translate_method(self, node):
        self.scope.enter_method(node)
        self.is_current_method_static = node.static
        result = ""
        if node.javadoc:
            result = self.indentation(self.indent_level) + f"\"\"\"{self.translate(node.javadoc)}\"\"\""

        if node.static:
            result += self.indentation(self.indent_level) + "@staticmethod"

        if node.name == self.scope.current_class:
            name = "__init__"
        else:
            name = node.name

        result += self.indentation(self.indent_level) + f"def {name}("

        if not node.static:
            result += f"self"
            if node.params_list and len(node.params_list) > 0:
                result += ", "
        if node.params_list:
            result += f"{self.translate(node.params_list[0])}"
        if len(node.params_list) > 1:
            for param in node.params_list[1:]:
                result += ", "
                result += f"{self.translate(param)}"

        result += "):"
        self.indent_level += 1
        if node.instructions_list:
            for i in node.instructions_list:
                result += self.indentation(self.indent_level) + self.translate(i)
        else:
            result += self.indentation(self.indent_level) + "pass"

        self.scope.locals_stack = []
        self.indent_level -= 1
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
            if len(node.else_do) == 1 and isinstance(node.else_do[0], Conditional):
                result += self.indentation(self.indent_level) + f"elif {self.translate_conditional(node.else_do[0], True)}"
            else:
                result += self.indentation(self.indent_level) + "else:"
                self.indent_level += 1
                for item in node.else_do:
                    result += self.indentation(self.indent_level) + f"{self.translate(item)}"
                self.indent_level -= 1
        return result
    
    def translate_while(self, node):
        result = f"while {self.translate(node.condition)}:"
        self.indent_level += 1
        for i in node.body:
            result += self.indentation(self.indent_level) + self.translate(i)
        self.indent_level -= 1
        return result

    def translate_for(self, node):
        var_name = node.initial.name
        self.scope.add_local(var_name)

        start_val = self.translate(node.initial.value)

        stop_val = self.translate(node.condition.op_right)
        if node.condition.operation == "<=":
            stop_val = f"{stop_val} + 1"
        elif node.condition.operation == ">=":
            stop_val = f"{stop_val} - 1"

        step = "1"
        if isinstance(node.update, ExprOp):
            if node.update.operation == "--":
                step = "-1"
        elif isinstance(node.update, CompoundAssign):
            step = self.translate(node.update.value)
            if node.update.operator == "-":
                step = f"-{step}"

        result = f"for {var_name} in range({start_val}, {stop_val}, {step}):"

        self.indent_level += 1
        for stmt in node.body:
            result += self.indentation(self.indent_level) + self.translate(stmt)
        self.indent_level -= 1

        return result

    def translate_do_while(self, node):
        # Java "do { body } while (cond)" becomes:
        # while True:
        #     body
        #     if not cond: 
        #       break
        
        result = "while True:"
        self.indent_level += 1
        
        for i in node.body:
            result += self.indentation(self.indent_level) + self.translate(i)
            
        condition = self.translate(node.condition)
        result += self.indentation(self.indent_level) + f"if not ({condition}):"
        result += self.indentation(self.indent_level + 1) + "break"
        
        self.indent_level -= 1
        return result
    
    def translate_variable_declaration(self, node):
        self.scope.add_local(node.name)
        return f"{node.name} = {self.translate(node.value)}"
    
    def translate_assign(self, node):
        name = node.name
        if name.startswith("this."):
            name = name[5:]
            return f"self.{name} = {self.translate(node.value)}"
            
        if not self.scope.is_local(name) and self.scope.is_field(name) and self.scope.locals_stack:
            name = f"self.{name}"
            
        return f"{name} = {self.translate(node.value)}"
    
    def translate_compound_assign(self, node):
        name = node.name
        if name.startswith("this."):
            name = name[5:]
            return f"self.{name} = {self.translate(node.value)}"
            
        if not self.scope.is_local(name) and self.scope.is_field(name) and self.scope.locals_stack:
            name = f"self.{name}"

        return f"{name} {node.operator} {self.translate(node.value)}"
    
    def translate_expr_op(self, node):
        val = self.translate(node.value)
        
        match node.operation:
            case "!":
                return f"not {val}"
            case "-":
                return f"-{val}"
            case "++":
                return f"{val} += 1"
            case "--":
                return f"{val} -= 1"
    
    def translate_binary_op(self, node):
        op_prec = self.precedence_binary_op.get(node.operation, 0)

        left = self.translate(node.op_left)
        if isinstance(node.op_left, BinaryOp):
            if self.precedence_binary_op.get(node.op_left.operation, 0) > op_prec:
                left = f"({left})"
                
        right = self.translate(node.op_right)
        if isinstance(node.op_right, BinaryOp):
            if self.precedence_binary_op.get(node.op_right.operation, 0) >= op_prec:
                right = f"({right})"

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
    
    def translate_string(self, node):
        return node.value
    
    def translate_char(self, node):
        return str(node.value)
    
    def translate_null(self, _node):
        return "None"
    
    def translate_inline(self, node):
        return "#" + str(node.contents).replace("//", "")
    
    def translate_multiline(self, node):
        content = node.contents.strip()
        if content.startswith("/*"):
            content = content[2:]
        if content.endswith("*/"):
            content = content[:-2]

        lines = content.split('\n')
        
        commented_lines = []
        for line in lines:
            clean_line = line.strip().lstrip('*').strip()
            commented_lines.append(f"#{clean_line}")
        sep = self.indentation(self.indent_level)
        return sep.join(commented_lines)
    
    def translate_javadoc(self, node):
        return node.contents.replace("/**", "").replace("*/", "")
    
    def translate_varref(self, node):
        name = node.name
        if name.startswith("this."):
            name = name[5:]
            return f"self.{name} = {self.translate(node.value)}"
        
        if self.scope.is_local(name):
            return name
        
        if self.scope.is_field(name) and self.scope.locals_stack:
            if getattr(self, 'is_current_method_static', False):
                return f"{self.scope.current_class}.{name}"
            else:
                return f"self.{name}"
    
        return node.name
    
    def translate_method_call(self, node):
        if not node.object or node.object == "this":
            if getattr(self, 'is_current_method_static', False):
                prefix = self.scope.current_class
            else:
                prefix = "self"
        else:
            prefix = self.translate_varref(VarRef(name=node.object))

        result = f"{prefix}.{node.method_name}("

        if node.params:
            translated_params = [self.translate(p) for p in node.params]
            result += ", ".join(translated_params)
            
        return result + ")"

        
    def translate_new_array(self, node):
        result = "["
        if node.items:
            result += f"{self.translate(node.items[0])}"
        if len(node.items) > 1:
            for item in node.items[1:]:
                result += ", "
                result += f"{self.translate(item)}"
        return result + "]"