public class classA {
    private int x = 0;
    public String str = null;

    public int get_x() {
        return x;
    }
}

public class classB {
    private int param = -1;
    private int[] array = new int[] {1,2,3};
    private int[] empty = new int[] {};
    
    /**
     * This is a javadoc for classB.
     * @param a Is a param of type classA.
     */
    public classB(classA a) {
        param = a.get_x();
    }
}
