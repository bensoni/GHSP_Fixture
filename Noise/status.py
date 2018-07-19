from PyQt5.QtCore import QThread
import time

class Status(object):
    def __init__(self):
        self.isStmConnected = False
        self.encoderPosition = 0
        

    def setStmStatus(self, isConnected):
        self.isStmConnected = isConnected
    
    def getStmStatus(self):
        return self.isStmConnected

    def setEncoderPosition(self, position):
        self.encoderPosition = position

    def getEncoderPosotion(self):
        return self.encoderPosition








    
class StatusThread(QThread):
    def __init__(self, threadID, threadName, status, ui, stm24):
        QThread.__init__(self)
        self.threadID = threadID
        self.name = threadName
        self.status = status
        self.ui = ui
        self.stm24 = stm24

    def run(self):

        while True:

            if self.status.getStmStatus():                
                self.stm24.sendCmd("IT")
                self.stm24.sendCmd("SP")
                self.ui.stm24Com_checkBox.setChecked(True)
            else:
                self.ui.stm24Com_checkBox.setChecked(False)
            

            time.sleep(0.1)
