# GHSP - Noise application for Ford Rotary Shifter.
# Combines GUI elements and event handlers into the main python
# script.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_MainWindow
from event import EventHandler
from can_log import CAN
from stm24 import STM24
from testing import Tests
from status import Status, StatusThread
import threading
import time



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    status = Status()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
	
    # Handles CAN communication
    can = CAN((status, ui))
    can.setup()

    # Handles TCP/IP Communication
    stm24 = STM24((status, ui))

    # Setup Tests
    tests = Tests((status, ui, stm24))

    # Handles Events
    events = EventHandler((app, status, ui, stm24, tests))

    # Start up a status thread. This monitors the system.
    statusThread = StatusThread(1, "SystemStatus", status, ui, stm24)
    statusThread.start()


    MainWindow.show()
    sys.exit(app.exec_())