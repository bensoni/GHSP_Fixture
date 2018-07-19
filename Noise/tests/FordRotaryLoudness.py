from _test import Test

class FordRotaryLoudness(Test):
    pass

    def name(self):
        return "Ford Rotary Loudness"


    def load(self):
        sequence = [[ "Enable Motor", self.enable_motor, " -- " ],
                    [ "Setup", self.setup, " -- "],
                    [ "Park to Drive", self.park_to_drive, " -- " ],
                    [ "Drive to Park", self.drive_to_park, " -- " ]]
        
        self.loadSequence(sequence)
    
    def enable_motor(self):
        self.stm24.sendCmd('ME')
        
    def setup(self):
        # Basic stepper motor setup
        self.stm24.sendCmd('VE0.15')
        self.stm24.sendCmd('AC0.167')
        self.stm24.sendCmd('DE0.167')

    def park_to_drive(self):
        self.stm24.sendCmd('DI-9500')
        self.stm24.sendCmd('FP')

    def drive_to_park(self):
        self.stm24.sendCmd('DI0')
        self.stm24.sendCmd('FP')

    