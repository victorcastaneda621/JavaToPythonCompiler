class foo:
    bar = 0
    baz = True
    
    @staticmethod
    def qux(other_bar: int):
        if foo.bar != other_bar:
            return foo.baz
        return not foo.baz