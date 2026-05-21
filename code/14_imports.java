import java.math.*;

public class SuperMain {
    public boolean variable = true;

    public static void main(int x, int y) {
        double res = Math.log(x);
        double res2 = Math.sin(x);
        double res3 = Math.cos(x);
        double res4 = Math.tan(y);
        double res5 = Math.sqrt(y);
    }
}

public class Main extends SuperMain {
    public void mainn(int x, int y) {
        super.main(x, y);
        variable = false;
    }
}