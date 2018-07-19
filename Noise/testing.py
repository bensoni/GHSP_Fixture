from gui import Ui_MainWindow
from stm24 import STM24


# Import tests
from tests import FordRotaryLoudness
from tests import ReturnToParkSetup

class Tests(object):
    def __init__(self, services):
        (self.status, self.ui, self.stm24) = services

        # Test list
        self.testList = [
            FordRotaryLoudness(services),
            ReturnToParkSetup(services)
        ]

        # Load up the first test to populate the test sequence table.
        self.testList[0].load()
        
        # Add each test to the combo box.
        for t in self.testList:
            self.ui.tests_comboBox.addItem(t.name())

    def getTestList(self):
        return self.testList


