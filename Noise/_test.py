#############################################################
# Interface for every test. Each test should extend this class
# and its methods.
#############################################################
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem

class Test(object):

    def __init__(self, services):
        (self.status, self.ui, self.stm24) = services

    ##
    # Load Sequence
    # Loads a test sequence as specified by the extended test.
    # @param Sequence The test sequence.
    #
    def loadSequence(self, sequence):
        self.currentStep = 0
        self.sequence = sequence
        self.updateSequenceTable()
        
    ##
    # Update Sequence Table
    # Updates the test sequence table and populates with steps
    # that correspond to that test.
    #
    def updateSequenceTable(self):
        self.ui.sequence_tableWidget.setRowCount(0)

        count = self.ui.sequence_tableWidget.rowCount()
        self.ui.diagnostics_textEdit.append(str(count))

        # Update with new test sequence
        for s in reversed(self.sequence):
            self.ui.sequence_tableWidget.insertRow(count)
            self.ui.sequence_tableWidget.setItem(count, 0, QTableWidgetItem(s[0]))
            self.ui.sequence_tableWidget.setItem(count, 1, QTableWidgetItem(s[2]))

    ##
    # Run
    # Runs the desired test sequence by executing each step in the
    # test sequence array.
    #
    def run(self):
        self.load()
        
        # Executes the test provided by sequence.
        for index, s in enumerate(reversed(self.sequence)):
            s[1]()
            self.currentStep = index
            self.updateStatus("Complete")

    ##
    # Update Status
    # Updates the status message for the current test step.
    # @param status The new step status.
    def updateStatus(self, status):
        self.sequence[self.currentStep][2] = status
        self.updateSequenceTable()

