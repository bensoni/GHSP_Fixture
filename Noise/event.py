# Event handler handles various events through
# the application.
import sys
from gui import Ui_MainWindow
from stm24 import STM24

class EventHandler(object):

    def __init__(self, services):
        (self.app, self.status, self.ui, self.stm24, self.testing) = services

        # Handle various user interaction with the GUI.    
        self.ui.run_pushButton.clicked.connect(self.on_runButtonClick)
        self.ui.actionQuit.triggered.connect(self.on_actionQuit)
        self.ui.tests_comboBox.currentIndexChanged.connect(self.on_testChange)


    def on_testChange(self):
        index = self.ui.tests_comboBox.currentIndex()
        self.ui.diagnostics_textEdit.append(str(index))
        getTest = self.testing.getTestList()[index]
        getTest.load()

    def on_runButtonClick(self):
        index = self.ui.tests_comboBox.currentIndex()
        getTest = self.testing.getTestList()[index]
        self.ui.diagnostics_textEdit.append(str(getTest.name()))
        getTest.run()

    def on_actionQuit(self):
        self.app.quit()