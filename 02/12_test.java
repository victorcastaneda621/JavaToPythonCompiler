public class Test {
    private Test other = null;
    private String msg = "hello\nworld";

    public Test getOther() {
        return other;
    }

    public int compute(Test obj) {
        other.getOther();
        return compute(obj);
    }

    public void empty() {
    }
}