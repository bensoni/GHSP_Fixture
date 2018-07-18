from _test import Test
import time


class FordRotaryLoudness(Test):
    pass

    def name(self):
        return "Ford Rotary Loudness"


    def load(self):
        sequence = [[ "Setup", self.run_setup, "Running setup..." ],
                    [ "Rotating shifter", self.run_rotateShifter, " -- " ]]
        
        self.loadSequence(sequence)
        
    def run_setup(self):
        # Basic stepper motor test.
        #self.stm24.sendCmd('MC2.5')
        #self.stm24.sendCmd('CP3.0')
        #self.stm24.sendCmd('GC100')
        self.stm24.sendCmd('SF450')
        self.stm24.sendCmd('EG51200')
        self.stm24.sendCmd('MR15')
        self.stm24.sendCmd('VE0.05')
        self.stm24.sendCmd('AC0.1')
        self.stm24.sendCmd('DE0.1')

    def run_rotateShifter(self):
        self.stm24.sendCmd('MC')
        #self.stm24.sendCmd('SH')
        self.stm24.sendCmd('EP0')
        self.stm24.sendCmd('VE0.05')
        self.stm24.sendCmd('FP-9500')
        #self.stm24.sendCmd('WT1')
        self.stm24.sendCmd('FP0')

    