public class AClass {
    public static int doSomething(int x, int y, boolean z) {
        int res = 0;
        if (z) {
            return y;
        } else {
            return 2 * x;
        }
    }
}