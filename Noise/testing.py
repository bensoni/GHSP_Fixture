#############################################################
# Populates UI with available tests and allows the user to
# select between tests using a drop-down.
#############################################################

# Import tests
from tests import FordRotaryLoudness
from tests import ReturnToParkSetup
from tests import SeekHome
from tests import Calibration

class Tests(object):

    ##
    # Constructor for Tests class
    # @param services Injected UI and STM24 services
    def __init__(self, services):
        (self.status, self.ui, self.stm24) = services
        
        # List of available tests
        self.testList = [
            Calibration(services),
            SeekHome(services),
            FordRotaryLoudness(services),
            ReturnToParkSetup(services)
        ]

        # Load up the first test to populate the test sequence table.
        self.testList[0].load()
        
        # Add each test to the combo box.
        for t in self.testList:
            self.ui.tests_comboBox.addItem(t.name())

    ##
    # Get Test List - Returns a list of the available tests.
    #
    def getTestList(self):
        return self.testList


