from _test import Test

class FordRotaryLoudness(Test):
    pass

    def name(self):
        return "Ford Rotary Loudness"


    def load(self):
        sequence = [[ "Run Ford Loudness", self.run_ford_loudness, " -- " ]]
        
        self.loadSequence(sequence)
    
    def run_ford_loudness(self):
        self.stm24.sendCmd('QX3')
    