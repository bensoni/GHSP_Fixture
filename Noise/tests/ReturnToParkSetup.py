from _test import Test
import time

class ReturnToParkSetup(Test):
    pass

    def name(self):
        return "Setup Return To Park (Drive Position)"


    def load(self):
        sequence = [[ "Move to Drive", self.move_to_drive, " -- " ]]
        
        self.loadSequence(sequence)
    
    def move_to_drive(self):
        self.stm24.sendCmd('QX4')
    