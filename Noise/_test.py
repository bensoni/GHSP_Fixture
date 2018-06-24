from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem

class Test(object):

    def __init__(self, services):
        (self.status, self.ui, self.stm24) = services

    def loadSequence(self, sequence):
        self.currentStep = 0
        self.sequence = sequence
        self.updateSequenceTable()
        

    def updateSequenceTable(self):
        self.ui.sequence_tableWidget.setRowCount(0)

        count = self.ui.sequence_tableWidget.rowCount()
        self.ui.diagnostics_textEdit.append(str(count))

        for s in reversed(self.sequence):
            self.ui.sequence_tableWidget.insertRow(count)
            self.ui.sequence_tableWidget.setItem(count, 0, QTableWidgetItem(s[0]))
            self.ui.sequence_tableWidget.setItem(count, 1, QTableWidgetItem(s[2]))

    def run(self):
        # Executes the test provided by sequence.
        for index, s in enumerate(reversed(self.sequence)):
            s[1]()
            self.currentStep = index

    def updateStatus(self, status):
        self.sequence[self.currentStep][2] = status
        self.updateSequenceTable()

