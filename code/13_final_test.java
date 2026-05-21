public class StressTest {
    private int counter = 0;
    private String status = "READY";

    /**
     * This is a javadoc test
     * it should become a triple-quoted string
     */
    public void runComplexLogic(int counter, boolean flag) {
        /* * Multiline comment test
         * with multiple lines
         */
        // Field access
        this.counter = 10;
        // Local param access
        counter = counter + 1;

        if (flag && (counter > 0 || status == "READY")) {
            status = "BUSY";
            for (int i = 0; i < 5; i++) {
                this.counter += i;
            }
        } else {
            int x = 0;
            do {
                x++;
                // inline test
            } while (x < 10);
        }

        this.finish();
    }

    public void finish() {
        this.status = "DONE";
    }
}
