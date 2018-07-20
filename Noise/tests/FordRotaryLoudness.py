#############################################################
# Ford Rotary Loudness Test
# Rotates the Ford rotary shifter CW.
#############################################################
from _test import Test

class FordRotaryLoudness(Test):
    pass

    ##
    # Name
    # The name of the test.
    #
    def name(self):
        return "Ford Rotary Loudness"

    ##
    # Load
    # Loads the sequence for this test.
    #
    def load(self):
        sequence = [[ "Run Ford Loudness", self.run_ford_loudness, " -- " ]]
        
        self.loadSequence(sequence)
    
    ##
    # Run Ford Loudness
    # Executes Ford Loudness test that is stored in Segment #3 of
    # the stepper motor.
    #
    def run_ford_loudness(self):
        self.stm24.sendCmd('QX3')
    