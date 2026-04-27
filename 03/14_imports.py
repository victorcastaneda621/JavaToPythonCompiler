import math
class SuperMain:
    variable = True
    
    @staticmethod
    def main(x: int, y: int):
        res = math.log(x)
        res2 = math.sin(x)
        res3 = math.cos(x)
        res4 = math.tan(y)
        res5 = math.sqrt(y)
class Main(SuperMain):
    
    def mainn(self, x: int, y: int):
        super().main(x, y)
        self.variable = False