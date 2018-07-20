#############################################################
# Return to Park
# Rotates the shifter until the drive position is reached.
#############################################################
from _test import Test

class ReturnToParkSetup(Test):
    pass

    ##
    # Name
    # The name of the test.
    #
    def name(self):
        return "Setup Return To Park (Drive Position)"

    ##
    # Load
    # Loads the sequence for this test.
    #
    def load(self):
        sequence = [[ "Move to Drive", self.move_to_drive, " -- " ]]
        
        self.loadSequence(sequence)
    
    ##
    # Move to Drives
    # Moves the shifter to the drive position. This program is stored
    # in Segment #4 of the stepper motor.
    #
    def move_to_drive(self):
        self.stm24.sendCmd('QX4')
    