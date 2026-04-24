public class Complicated {
    private boolean a = true;
    private boolean b = false;
    private boolean c = true;

    public boolean complex() {
    if (a && b) {
        return a && b;
    } else if (a || b) {
        return a || b;
    } else if (a || b && c) {
        return (a || b && c);
    } else if ((a || c) && (b || c)) {
        return (a || c) && (b || c);
    } else if (a || (b || c)) {
        return a || (b || c);
    } else {
        return a && b || c;
    }
}
}
