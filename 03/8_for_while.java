public class MoreNonsense {
    private int MAX_ITER = 3;

    public void nonsenseFunc() {
    int res = MAX_ITER;
    for (int i = 0; i <= MAX_ITER; i++) {
        res += 1;
    }
    for (int i = MAX_ITER; i < 0; i--) {
        res += 1;
    }
    while (res > 0) {
        res -= 1;
    }
    do {
        res += 1;
    } while (res >= MAX_ITER);
}
}