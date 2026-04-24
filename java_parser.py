from java_lexer import JavaLexer
from sly import Parser

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