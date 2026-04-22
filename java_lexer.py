from sly import Lexer

class JavaLexer(Lexer):

    tokens = {
        OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
        ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
        INHERITS, ISVOID, LET, LOOP, NEW, OF,
        POOL, WHILE, STR_CONST, LE, DARROW, ASSIGN
    }

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

    def tokenize(self, file):
        return file