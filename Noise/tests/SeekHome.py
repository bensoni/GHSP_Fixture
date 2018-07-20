from _test import Test

class SeekHome(Test):
    pass

    def name(self):
        return "Move to Park"


    def load(self):
        sequence = [[ "Return to Park", self.seek_home, " -- " ]]
        
        self.loadSequence(sequence)
    
    def seek_home(self):
        self.stm24.sendCmd('QX2')

    