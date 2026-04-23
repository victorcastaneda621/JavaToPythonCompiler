from sly import Lexer

class JavaLexer(Lexer):

    tokens = {
        ID, 
        INT_CONST, FLOAT_CONST,
        SHORT, INT, LONG, BOOLEAN, FLOAT, DOUBLE,
        ELSE, IF, TRUE, FALSE
    }

    literals = {';', '='}

    ignore = ' \t'

    keywords = {
                "else", "if", "true", "false",
                "short", "int", "long", "boolean", "float", "double"
                }

    @_(r'[0-9]+\.[0-9]+f?')
    def FLOAT_CONST(self, t):
        return t

    @_(r'[0-9]+L?')
    def INT_CONST(self, t):
        return t

    @_(r'[A-Z_a-z][A-Z0-9_a-z]*') # Keywords, or any other word not previously handled
    def ID(self, t):
        if t.value in self.keywords:
            t.type = t.value.upper() 
        return t
    
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, _t):
        self.index += 1

    def handle_eof(self, text, *args, **kwargs):
        for tok in super().tokenize(text, *args, **kwargs):
            yield tok
            
        if self.__class__.__name__ == 'MatchingString':
            class EOFToken: pass
            t = EOFToken()
            t.type = "ERROR"
            t.value = '"EOF in string constant"'
            t.lineno = self.lineno
            yield t
            self.begin(JavaLexer) 

        elif self.__class__.__name__ == 'Comentario':
            class EOFToken: pass
            t = EOFToken()
            t.type = "ERROR"
            t.value = '"EOF in comment"'
            t.lineno = self.lineno
            yield t
            self.begin(JavaLexer)

    def tokenize(self, text):
        list_strings = []
        for token in self.handle_eof(text): 
            result = f'#{token.lineno} {token.type} '
            
            if token.type == 'ID':
                result += f"{token.value}"
            elif token.type in self.literals:
                result = f'#{token.lineno} \'{token.type}\' '
            elif token.type == 'STRING':
                result += token.value
            elif token.type in ['INT_CONST', 'FLOAT_CONST']:
                result += str(token.value)
            elif token.type == 'ERROR':
                result = f'#{token.lineno} {token.type} {token.value}'
            else:
                result = f'#{token.lineno} {token.type}'
                
            list_strings.append(result.strip())
        return list_strings