#############################################################
# Calibration Test
# Calibrates the test fixture by rotating the shifter CCW
# until it stalls. This is considered the origin or home
# position.
#############################################################

from _test import Test

class Calibration(Test):
    pass

    ##
    # Name
    # The name of the test.
    #
    def name(self):
        return "Calibrate (Run on startup)"

    ##
    # Load
    # Loads the sequence for this test.
    #
    def load(self):
        sequence = [[ "Determine Origin", self.find_origin, " -- " ]]
        
        self.loadSequence(sequence)
    
    ##
    # Find Origin
    # Finds the origin or home position for the test fixture.
    # This is done by executing Segment #1 on the stepper motor.
    # 
    # This test can be updated using Q Programmer and updating Segment #1.
    #
    
    def find_origin(self):
        self.stm24.sendCmd('QX1')

    