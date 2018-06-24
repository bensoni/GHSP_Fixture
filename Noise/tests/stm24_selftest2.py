from _test import Test

class STM24_SelfTest2(Test):
    pass

    def name(self):
        return "STM24 Self-Test #2"


    def load(self):
        sequence = [[ "Setup", self.run_setup, "Running setup..." ],
                    [ "Rotating shifter", self.run_rotateShifter, " -- " ]]
        
        self.loadSequence(sequence)
        
    def run_setup(self):
        # Basic stepper motor test.
        self.stm24.sendCmd('AC25')
        self.stm24.sendCmd('DE25')
        self.stm24.sendCmd('VE5')

    def run_rotateShifter(self):
        self.stm24.sendCmd('FL5000')

    