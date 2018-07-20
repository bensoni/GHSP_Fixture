from _test import Test

class Calibration(Test):
    pass

    def name(self):
        return "Calibrate (Run on startup)"


    def load(self):
        sequence = [[ "Determine Origin", self.find_origin, " -- " ]]
        
        self.loadSequence(sequence)
    
    def find_origin(self):
        self.stm24.sendCmd('QX1')

    