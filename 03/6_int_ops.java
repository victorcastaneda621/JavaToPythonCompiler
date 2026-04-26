public class Nonsense {
    private int var1 = 1;
    private int var2 = -5;
    private int var3 = 8 + 4;
    private int var4 = var3 - var1;
    private int var5 = 6 + var2;
    private int var6 = 5 % 3;

    public void method() {
        var5 = var5 * 2;
        var5 = var5 / var3;
        var4 += 1;
        var4 -= 1;
        var4 *= 2;
        var4 /= 2;
        var5 = var5 % 4;
        var3 %= 2;
    }
}