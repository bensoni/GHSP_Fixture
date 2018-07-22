#############################################################
# Manages the status of the test fixture.
#############################################################

from PyQt5.QtCore import QThread
import time

class Status(object):
    def __init__(self):
        self.isStmConnected = False
        self.lastTime = time.time()

    ##
    # Set STM24 Status
    # Sets the current status of the STM24 stepper motor.
    # @param isConnected Is there stepper motor communication.
    #
    def setStmStatus(self, isConnected):
        self.isStmConnected = isConnected
    
    ##
    # Get STM24 Status
    # Returns the status of the stepper motor COM.
    def getStmStatus(self):
        return self.isStmConnected

    ##
    # Update Last Packet Time
    # Updates the last packet time with the current time. This is
    # used to determine if the host is still receiving packets from
    # the STM24.
    #
    def updateLastPacketTime(self):
        self.lastTime = time.time()

    ##
    # Get Last Packet Time
    # Retrieves the last packet time.
    # @return The last packet time in seconds.
    #
    def getLastPacketTime(self):
        return self.lastTime
    
    ##
    # Is STM24 Online
    # Determines if the host is still receiving packets from the STM24
    # based on the last packet that was recieved.
    # @return Status of STM24 communication.
    #
    def isStmOnline(self):
        return self.lastTime > (time.time() - 1)


##
# Status Thread
# Determines the current status of the test fixture by sending
# commands over CAN or UDP.
#
class StatusThread(QThread):
    def __init__(self, threadID, threadName, stm24, status, ui):
        QThread.__init__(self)
        self.threadID = threadID
        self.name = threadName
        self.stm24 = stm24
        self.status = status
        self.ui = ui

    def run(self):
        while True:
            self.stm24.sendCmd("IT")
            self.stm24.sendCmd("RXe")

        
            self.ui.stm24Com_checkBox.setChecked(self.status.isStmOnline())

            time.sleep(0.05)
