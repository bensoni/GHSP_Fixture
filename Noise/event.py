#############################################################
# Event handler handles various events through
# the application.
#############################################################

class EventHandler(object):

    def __init__(self, services):
        (self.app, self.ui, self.testing, self.stm24) = services

        # Connect GUI form elements to event handlers.  
        self.ui.run_pushButton.clicked.connect(self.on_runButtonClick)
        self.ui.actionQuit.triggered.connect(self.on_actionQuit)
        self.ui.tests_comboBox.currentIndexChanged.connect(self.on_testChange)
        self.ui.stop_pushButton.clicked.connect(self.on_stopButtonClick)

    ##
    # On Test Change
    # When a test is changed in the drop down, the interface should
    # update to reflect the changes for the new test.
    #
    def on_testChange(self):
        index = self.ui.tests_comboBox.currentIndex()
        self.ui.diagnostics_textEdit.append(str(index))
        getTest = self.testing.getTestList()[index]
        getTest.load()

    ##
    # On Run Button Click
    # When the user presses the run button the selected test should
    # then execute.
    #
    def on_runButtonClick(self):
        index = self.ui.tests_comboBox.currentIndex()
        getTest = self.testing.getTestList()[index]
        self.ui.diagnostics_textEdit.append(str(getTest.name()))
        getTest.run()

    ##
    # On Stop Button Click
    # Attempts to stop movement. May not be possible in all situations.
    #
    def on_stopButtonClick(self):
        self.stm24.sendCmd('MT1')
        self.stm24.sendCmd('SMD')
        self.stm24.sendCmd('MD')

    ##
    # On Action Quit
    # Quites the application when the user presses File -> Quit.
    #
    def on_actionQuit(self):
        self.app.quit()