class Nonsense:
    var1 = 1
    var2 = -5
    var3 = 8 + 4
    var4 = var3 - var1
    var5 = 6 + var2
    var6 = 5 % 3
    
    def method(self):
        self.var5 = self.var5 * 2
        self.var5 = self.var5 / self.var3
        self.var4 += 1
        self.var4 -= 1
        self.var4 *= 2
        self.var4 /= 2
        self.var5 = self.var5 % 4
        self.var3 %= 2