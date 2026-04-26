class classA:
    x = 0
    str = None
    
    def get_x(self):
        return self.x
class classB:
    param = -1
    array = [1, 2, 3]
    empty = []
    
    """
     * This is a javadoc for classB.
     * @param a Is a param of type classA.
     """
    def __init__(self, a: classA):
        self.param = a.get_x()