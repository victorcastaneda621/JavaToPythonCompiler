from java_lexer import JavaLexer
from sly import Parser
from classes import *

class JavaParser(Parser):
    tokens = JavaLexer.tokens

    # Operator precedence
    precedence = (
        ('right', '=', 'PLUSEQ', 'MINUSEQ', 'TIMESEQ', 'DIVEQ', 'MODEQ'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQEQ', 'NEQ'),
        ('left', 'LT', 'GT', 'LE', 'GE'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'NOT'),
        ('right', 'UMINUS'),
        ('left', 'PLUSPLUS', 'MINUSMINUS')
    )

    debugfile = 'parser.out'

    def __init__(self):
        self.filename = ""
        self.errors = []

    def error(self, p):
        if p:
            if p.type in ['ID', 'INT_CONST', 'FLOAT_CONST', 'STR_CONST', 'CHAR_CONST']:
                message = f'"{self.filename}", line {p.lineno}: syntax error at or near {p.type} = {p.value}'
            elif p.type in JavaLexer.literals:
                message = f'"{self.filename}", line {p.lineno}: syntax error at or near \'{p.type}\''
            else:
                message = f'"{self.filename}", line {p.lineno}: syntax error at or near {p.type}'
            
            self.errors.append(message)
        else:
            self.errors.append(f'"{self.filename}", line 0: syntax error at or near EOF')

    @_("class_list")
    def program(self, p):
        return Program(seq=p.class_list, line=p.lineno)
    
    @_("java_class")
    def class_list(self, p):
        return [p.java_class]

    @_("class_list java_class")
    def class_list(self, p):
        return p.class_list + [p.java_class]
    
    @_("visibility static_mod CLASS ID '{' member_list '}'")
    def java_class(self, p):
        return Class(
            visibility=p.visibility,
            static=p.static_mod,
            name=p.ID,
            member_list=p.member_list,
            line=p.lineno
        )
    
    @_("PUBLIC", "PRIVATE")
    def visibility(self, p):
        return p[0].lower()

    @_("STATIC", "")
    def static_mod(self, p):
        return hasattr(p, 'STATIC')
    
    @_("member_list member")
    def member_list(self, p):
        return p.member_list + [p.member]

    @_("member")
    def member_list(self, p):
        return [p.member]
    
    @_("visibility static_mod return_type ID '=' expr ';'")
    def member(self, p):
        return Field(
            visibility=p.visibility, 
            static=p.static_mod, 
            type=p.return_type, 
            name=p.ID, 
            value=p.expr, 
            line=p.lineno
        )
    
    @_("visibility static_mod return_type ID ';'")
    def member(self, p):
        return Field(
            visibility=p.visibility, 
            static=p.static_mod, 
            type=p.return_type, 
            name=p.ID, 
            value=None, 
            line=p.lineno
        )
    
    @_("visibility static_mod return_type ID '(' param_list ')' '{' instruction_list '}'")
    def member(self, p):
        return Method(
            visibility=p.visibility, 
            static=p.static_mod,
            return_type=p.return_type, 
            name=p.ID,
            params_list=p.param_list, 
            instructions_list=p.instruction_list, 
            line=p.lineno
        )

    @_("javadoc visibility static_mod return_type ID '(' param_list ')' '{' instruction_list '}'")
    def member(self, p):
        return Method(
            javadoc=p.javadoc, 
            visibility=p.visibility, 
            static=p.static_mod,
            return_type=p.return_type, 
            name=p.ID,
            params_list=p.param_list, 
            instructions_list=p.instruction_list, 
            line=p.lineno
        )
    
    @_("visibility static_mod ID '(' param_list ')' '{' instruction_list '}'")
    def member(self, p):
        return Method(
            visibility=p.visibility, 
            static=p.static_mod,
            return_type=None, 
            name=p.ID,
            params_list=p.param_list, 
            instructions_list=p.instruction_list, 
            line=p.lineno
        )

    @_("javadoc visibility static_mod ID '(' param_list ')' '{' instruction_list '}'")
    def member(self, p):
        return Method(
            javadoc=p.javadoc, 
            visibility=p.visibility, 
            static=p.static_mod,
            return_type=None, 
            name=p.ID,
            params_list=p.param_list, 
            instructions_list=p.instruction_list, 
            line=p.lineno
        )
    
    @_("INLINE_COMMENT")
    def member(self, p):
        return InlineComment(contents=p.INLINE_COMMENT, line=p.lineno)

    @_("MULTILINE_COMMENT")
    def member(self, p):
        return MultilineComment(contents=p.MULTILINE_COMMENT, line=p.lineno)
    
    @_("JAVADOC")
    def javadoc(self, p):
        return Javadoc(
            contents=p.JAVADOC, line=p.lineno
        )
    
    @_("return_type ID")
    def param(self, p):
        return Param(
            type=p.return_type,
            name=p.ID, 
            line=p.lineno
        )
    
    @_("expr ';'")
    def instruction(self, p):
        return p.expr
    
    @_("IF '(' expr ')' '{' instruction_list '}'")
    def instruction(self, p):
        return Conditional(condition=p.expr, then_do=p.instruction_list, line=p.lineno)
    
    @_("IF '(' expr ')' '{' instruction_list '}' ELSE '{' instruction_list '}'")
    def instruction(self, p):
        return Conditional(condition=p.expr, then_do=p.instruction_list0, else_do=p.instruction_list1, line=p.lineno)
    
    @_("IF '(' expr ')' '{' instruction_list '}' ELSE instruction")
    def instruction(self, p):
        return Conditional(condition=p.expr, then_do=p.instruction_list, else_do=[p.instruction], line=p.lineno)
    
    @_("INLINE_COMMENT")
    def instruction(self, p):
        return InlineComment(contents=p.INLINE_COMMENT, line=p.lineno)

    @_("MULTILINE_COMMENT")
    def instruction(self, p):
        return MultilineComment(contents=p.MULTILINE_COMMENT, line=p.lineno)
    
    @_("INT", "LONG", "SHORT", "FLOAT", "DOUBLE", "BOOLEAN", "CHAR", "STRINGTYPE", "VOID")
    def return_type(self, p):
        return p[0].lower()
    
    @_("ID")
    def return_type(self, p):
        return p.ID
    
    @_("param")
    def param_list(self, p):
        return [p.param]
    
    @_("param_list ',' param")
    def param_list(self, p):
        return p.param_list + [p.param]

    @_("")
    def param_list(self, p):
        return []
    
    @_("instruction_list instruction")
    def instruction_list(self, p):
        return p.instruction_list + [p.instruction]

    @_("")
    def instruction_list(self, p):
        return []
    
    @_("expr '+' expr", "expr '-' expr", "expr '*' expr", "expr '/' expr", "expr '%' expr", 
       "expr AND expr", "expr OR expr", "expr EQEQ expr", "expr NEQ expr",
       "expr LT expr", "expr GT expr", "expr LE expr", "expr GE expr")
    def expr(self, p):
        return BinaryOp(operation=p[1], op_left=p[0], op_right=p[2], line=p.lineno)
    
    @_("expr PLUSPLUS", "expr MINUSMINUS")
    def expr(self, p):
        return ExprOp(operation=p[1], value=p[0], line=p.lineno)
    
    @_("NOT expr")
    def expr(self, p):
        return ExprOp(operation='!', value=p.expr, line=p.lineno)
    
    @_("'-' expr %prec UMINUS")
    def expr(self, p):
        return ExprOp(operation='-', value=p.expr, line=p.lineno)
    
    @_("RETURN expr ';'")
    def instruction(self, p):
        return Return(value=p.expr, line=p.lineno)

    @_("RETURN ';'")
    def instruction(self, p):
        return Return()
    
    @_("FOR '(' for_init ';' expr ';' expr ')' '{' instruction_list '}'")
    def instruction(self, p):
        return For(initial=p.for_init, condition=p.expr0, update=p.expr1, body=p.instruction_list, line=p.lineno)

    @_("return_type ID '=' expr")
    def for_init(self, p):
        return VariableDeclaration(type=p.return_type, name=p.ID, value=p.expr, line=p.lineno)

    @_("expr")
    def for_init(self, p):
        return p.expr
    
    @_("NEW return_type '{' array_items '}'")
    def expr(self, p):
        return NewArray(type=p.return_type, items=p.array_items, line=p.lineno)
    
    @_("array_items ',' expr")
    def array_items(self, p):
        return p.array_items + [p.expr]

    @_("expr")
    def array_items(self, p):
        return [p.expr]

    @_("")
    def array_items(self, p):
        return []
    
    @_("WHILE '(' expr ')' '{' instruction_list '}'")
    def instruction(self, p):
        return While(condition=p.expr, body=p.instruction_list, line=p.lineno)
    
    @_("DO '{' instruction_list '}' WHILE '(' expr ')' ';'")
    def instruction(self, p):
        return DoWhile(condition=p.expr, body=p.instruction_list, line=p.lineno)
    
    @_("INT_CONST")
    def expr(self, p):
        return Int(value=p.INT_CONST, line=p.lineno)
    
    @_("FLOAT_CONST")
    def expr(self, p):
        return Float(value=p.FLOAT_CONST, line=p.lineno)
    
    @_("CHAR_CONST")
    def expr(self, p):
        return Char(value=p.CHAR_CONST, line=p.lineno)
    
    @_("TRUE", "FALSE")
    def expr(self, p):
        return Boolean(value=p[0], line=p.lineno)
    
    @_("STR_CONST")
    def expr(self, p):
        return String(value=p.STR_CONST, line=p.lineno)
    
    @_("NULL")
    def expr(self, p):
        return Null(line=p.lineno)

    @_("ID")
    def expr(self, p):
        return VarRef(name=p.ID, line=p.lineno)
    
    @_("ID '=' expr")
    def expr(self, p):
        return Assign(name=p.ID, value=p.expr, line=p.lineno)
    
    @_("ID PLUSEQ expr", "ID MINUSEQ expr", "ID TIMESEQ expr", "ID DIVEQ expr", "ID MODEQ expr",)
    def expr(self, p):
        return CompoundAssign(name=p.ID, value=p.expr, operator=p[1], line=p.lineno)
    
    @_("return_type ID '=' expr ';'")
    def instruction(self, p):
        return VariableDeclaration(type=p.return_type, name=p.ID, value=p.expr, line=p.lineno)

    @_("return_type ID ';'")
    def instruction(self, p):
        return VariableDeclaration(type=p.return_type, name=p.ID, line=p.lineno)
    
    @_("ID '.' ID '(' arg_list ')'")
    def expr(self, p):
        return MethodCall(object=p[0], method_name=p[2], params=p.arg_list, line=p.lineno)

    @_("ID '(' arg_list ')'")
    def expr(self, p):
        return MethodCall(object='this', method_name=p.ID, params=p.arg_list, line=p.lineno)
    
    @_("expr")
    def arg_list(self, p):
        return [p.expr]

    @_("arg_list ',' expr")
    def arg_list(self, p):
        return p.arg_list + [p.expr]

    @_("")
    def arg_list(self, p):
        return []

    @_("'(' expr ')'")
    def expr(self, p):
        return p.expr
    
    @_("INT '[' ']'", "LONG '[' ']'", "BOOLEAN '[' ']'", "CHAR '[' ']'", "SHORT '[' ']'",
       "FLOAT '[' ']'", "DOUBLE '[' ']'", "STRINGTYPE '[' ']'", "ID '[' ']'")
    def return_type(self, p):
        return p[0].lower() + '[]'