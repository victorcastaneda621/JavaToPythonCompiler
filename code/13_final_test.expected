class StressTest:
    counter = 0
    status = "READY"
    
    """
     * This is a javadoc test
     * it should become a triple-quoted string
     """
    def runComplexLogic(self, counter: int, flag: bool):
        #Multiline comment test
        #with multiple lines
        #
        # Field access
        self.counter = 10
        # Local param access
        counter = counter + 1
        if flag and (counter > 0 or self.status == "READY"):
            self.status = "BUSY"
            for i in range(0, 5, 1):
                self.counter = i
        else:
            x = 0
            while True:
                x += 1
                # inline test
                if not (x < 10):
                    break
        self.finish()
    
    def finish(self):
        self.status = "DONE"