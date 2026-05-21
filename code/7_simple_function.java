public class Funcs {
    public int func() {
        return 3;
    }

    public void func2(int x, int y) {
        x += y;
    }

    private double func3(boolean bool_value) {
        double res = 0.0;
        if (bool_value) {
            res += 1.0;
        } else {
            res += 0.0;
        }
        return res;
    }
}
