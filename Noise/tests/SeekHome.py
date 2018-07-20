#############################################################
# Seek
# Seeks the home position or origin.
#############################################################
from _test import Test

class SeekHome(Test):
    pass

    ##
    # Name
    # The name of the test.
    #
    def name(self):
        return "Move to Park"

    ##
    # Load
    # Loads the sequence for this test.
    #
    def load(self):
        sequence = [[ "Return to Park", self.seek_home, " -- " ]]
        
        self.loadSequence(sequence)
    
    ##
    # Seek Home
    # Seeks home by rotating the shifter until the encoder position
    # is near 0. This is stored in Segment #2.
    def seek_home(self):
        self.stm24.sendCmd('QX2')

    