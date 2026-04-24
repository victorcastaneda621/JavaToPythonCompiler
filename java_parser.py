from java_lexer import JavaLexer
from sly import Parser
from classes import *

class JavaParser(Parser):
    tokens = JavaLexer.tokens

    # Precedencia de operadores de menor a mayor para resolver ambigüedades
    precedence = (
    )

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
        return Program(seq=p.class_list)
    
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

    @_("")
    def member_list(self, p):
        return []
    
    @_("visibility static_mod return_type ID '=' expr ';'")
    def member(self, p):
        return Field(
            visibility=p.visibility, 
            static=p.static_mod, 
            type=p.return_type, 
            name=p.ID, 
            value=p.expr
        )
    
    @_("visibility static_mod return_type ID ';'")
    def member(self, p):
        return Field(
            visibility=p.visibility, 
            static=p.static_mod, 
            type=p.return_type, 
            name=p.ID, 
            value=None
        )
    
    @_("visibility static_mod return_type ID '(' param_list ')' '{' instruction_list '}'")
    def member(self, p):
        return Method(
            visibility=p.visibility, 
            static=p.static_mod,
            return_type=p.return_type, 
            name=p.ID,
            params_list=p.param_list, 
            instructions_list=p.instruction_list
        )

    # Method with javadoc
    @_("javadoc visibility static_mod return_type ID '(' param_list ')' '{' instruction_list '}'")
    def member(self, p):
        return Method(
            javadoc=p.javadoc, 
            visibility=p.visibility, 
            static=p.static_mod,
            return_type=p.return_type, 
            name=p.ID,
            params_list=p.param_list, 
            instructions_list=p.instruction_list
        )
    
    @_("INLINE_COMMENT")
    def member(self, p):
        return InlineComment(contents=p.INLINE_COMMENT)

    @_("MULTILINE_COMMENT")
    def member(self, p):
        return MultilineComment(contents=p.MULTILINE_COMMENT)
    
    @_("JAVADOC")
    def javadoc(self, p):
        return Javadoc(
            contents=p.JAVADOC
        )
    
    @_("return_type ID")
    def param(self, p):
        return Param(
            type=p.return_type,
            name=p.ID
        )
    
    @_("expr ';'")
    def instruction(self, p):
        return p.expr
    
    @_("INLINE_COMMENT")
    def instruction(self, p):
        return InlineComment(contents=p.INLINE_COMMENT)

    @_("MULTILINE_COMMENT")
    def instruction(self, p):
        return MultilineComment(contents=p.MULTILINE_COMMENT)
    
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
    
    @_("instruction")
    def instruction_list(self, p):
        return [p.instruction]
    
    @_("instruction_list instruction")
    def instruction_list(self, p):
        return p.instruction_list + [p.instruction]

    @_("")
    def instruction_list(self, p):
        return []