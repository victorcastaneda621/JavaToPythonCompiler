public class foo {
    private int bar = 0;
    private boolean baz = true;
    public static boolean qux(int other_bar) {
        if (bar != other_bar) {
            return baz;
        }
        return !baz;
    }
}