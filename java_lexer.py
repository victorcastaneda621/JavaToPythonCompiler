from sly import Lexer

class JavaLexer(Lexer):

    tokens = {
        ID, RETURN, CLASS, STATIC,
        ELSE, IF, TRUE, FALSE, AND, OR, EQEQ,
        PLUSEQ, MINUSEQ, TIMESEQ, DIVEQ, MODEQ,
        INT_CONST, FLOAT_CONST, CHAR_CONST, STR_CONST,
        PLUSPLUS, MINUSMINUS,
        PUBLIC, PRIVATE, VOID, NULL, NEW,
        LE, LT, GE, GT, NEQ, NOT,
        INLINE_COMMENT, MULTILINE_COMMENT, JAVADOC, STRINGTYPE, CHAR,
        SHORT, INT, LONG, BOOLEAN, FLOAT, DOUBLE,
        FOR, WHILE, DO
    }

    literals = {';', '=', '(', ')', '{', '}', '+', '-', '*', '/', '%', ',', '.', '[', ']'}

    ignore = ' \t'

    keywords = {
                "return", "class", "static",
                "else", "if", "true", "false",
                "short", "int", "long", "boolean", "float", "double", "char", "String",
                "public", "private", "void", "null", "new",
                "for", "while", "do"
                }
    
    @_(r'"([^"\\\n]|\\.)*(\"|\n|$)')
    def STR_CONST(self, t):
        if not t.value.endswith("\""):
            t.type = 'ERROR'
            t.value = "Unterminated string constant"
            self.lineno += 1
            return t
        t.type = "STR_CONST"
        return t
    
    @_(r'\'.\'')
    def CHAR_CONST(self, t):
        t.type = "CHAR_CONST"
        return t
    
    @_(r'//.*')
    def INLINE_COMMENT(self, t):
        t.type = "INLINE_COMMENT"
        return t

    @_(r'/\*\*[\s\S]*?\*/')
    def JAVADOC(self, t):
        self.lineno += t.value.count('\n')
        t.type = "JAVADOC"
        return t
    
    @_(r'/\*[\s\S]*?(\*/|$)')
    def MULTILINE_COMMENT(self, t):
        self.lineno += t.value.count('\n')
        if not t.value.endswith('*/'):
            t.type = 'ERROR'
            t.value = 'EOF in comment'
            return t
        return t
    
    @_(r'&&')
    def AND(self, t):
        t.type = "AND"
        return t
    
    @_(r'\|\|')
    def OR(self, t):
        t.type = "OR"
        return t
    
    @_(r'==')
    def EQEQ(self, t):
        t.type = "EQEQ"
        return t
    
    @_(r'\+=')
    def PLUSEQ(self, t):
        t.type = "PLUSEQ"
        return t
    
    @_(r'-=')
    def MINUSEQ(self, t):
        t.type = "MINUSEQ"
        return t
    
    @_(r'\*=')
    def TIMESEQ(self, t):
        t.type = "TIMESEQ"
        return t
    
    @_(r'/=')
    def DIVEQ(self, t):
        t.type = "DIVEQ"
        return t
    
    @_(r'%=')
    def MODEQ(self, t):
        t.type = "MODEQ"
        return t
    
    @_(r'\+\+')
    def PLUSPLUS(self, t):
        t.type = "PLUSPLUS"
        return t
    
    @_(r'--')
    def MINUSMINUS(self, t):
        t.type = "MINUSMINUS"
        return t
    
    @_(r'<=')
    def LE(self, t):
        t.type = "LE"
        return t
    
    @_(r'<')
    def LT(self, t):
        t.type = "LT"
        return t
    
    @_(r'>=')
    def GE(self, t):
        t.type = "GE"
        return t
    
    @_(r'>')
    def GT(self, t):
        t.type = "GT"
        return t
    
    @_(r'!=')
    def NEQ(self, t):
        t.type = "NEQ"
        return t
    
    @_(r'!')
    def NOT(self, t):
        t.type = "NOT"
        return t

    @_(r'[0-9]+\.[0-9]+f?')
    def FLOAT_CONST(self, t):
        return t

    @_(r'[0-9]+L?')
    def INT_CONST(self, t):
        return t

    @_(r'[A-Z_a-z][A-Z0-9_a-z]*') # Keywords, or any other word not previously handled
    def ID(self, t):
        if t.value in self.keywords:
            t.type = t.value.upper() if t.value != "String" else "STRINGTYPE"
        return t
    
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        t.type = 'ERROR'
        t.value = t.value[0]
        self.index += 1
        return t

    def handle_eof(self, text, *args, **kwargs):
        for tok in super().tokenize(text, *args, **kwargs):
            yield tok

    def tokenize(self, text):
        list_strings = []
        for token in self.handle_eof(text): 
            result = f'#{token.lineno} {token.type} '
            
            if token.type == 'ID':
                result += f"{token.value}"
            elif token.type in self.literals:
                result = f'#{token.lineno} \'{token.type}\' '
            elif token.type in ['STR_CONST', 'CHAR_CONST', 'INLINE_COMMENT', 'MULTILINE_COMMENT', 'JAVADOC']:
                result += token.value
            elif token.type in ['INT_CONST', 'FLOAT_CONST']:
                result += str(token.value)
            elif token.type == 'ERROR':
                result = f'#{token.lineno} {token.type} {token.value}'
            else:
                result = f'#{token.lineno} {token.type}'
                
            list_strings.append(result.strip())
        return list_strings