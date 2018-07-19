from _test import Test
import time

class ReturnToParkSetup(Test):
    pass

    def name(self):
        return "Setup Return To Park (Drive Position)"


    def load(self):
        sequence = [[ "Enable Motor", self.enable_motor, " -- " ],
                    [ "Set to drive position", self.setup, " -- "],
                    [ "Disable Motor", self.disable_motor, " -- " ]]
        
        self.loadSequence(sequence)
    
    def enable_motor(self):
        self.ui.diagnostics_textEdit.append("Sending Motor Enable")
        self.stm24.sendCmd('ME')
        
    def setup(self):
        # Basic stepper motor setup
        self.ui.diagnostics_textEdit.append("Feed to position")
        self.stm24.sendCmd('DI-9500')
        self.stm24.sendCmd('FP')
        time.sleep(5)


    def disable_motor(self):
        self.ui.diagnostics_textEdit.append("Sending Motor Disable")
        self.stm24.sendCmd('MD')

    