class Test:
    other = None
    msg = "hello\nworld"
    
    def getOther(self):
        return self.other
    
    def compute(self, obj: Test):
        self.other = obj.getOther()
        return self.compute(obj)
    
    def empty(self):
        pass