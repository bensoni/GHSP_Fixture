from gui import Ui_MainWindow
from stm24 import STM24


# Import tests
from tests import STM24_SelfTest
from tests import STM24_SelfTest2

class Tests(object):
    def __init__(self, services):
        (self.status, self.ui, self.stm24) = services

        self.testList = [
            STM24_SelfTest(services),
            STM24_SelfTest2(services)
        ]
        
        for t in self.testList:
            self.ui.tests_comboBox.addItem(t.name())

    def getTestList(self):
        return self.testList


