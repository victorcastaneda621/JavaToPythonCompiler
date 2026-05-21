class AClass:
    
    @staticmethod
    def doSomething(x: int, y: int, z: bool):
        res = 0
        if z:
            return y
        else:
            return 2 * x