#############################################################
# GHSP - Noise application for Ford Rotary Shifter.
# Handles communication between the Forder Rotary shifter over
# CAN and simulates rotation movement using a stepper
# motor over UDP.
#############################################################
import sys
from PyQt5 import QtWidgets
from gui import Ui_MainWindow
from event import EventHandler
from can_log import CAN
from stm24 import STM24
from testing import Tests
from status import Status, StatusThread

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    # Status of the test fixture
    status = Status()

    # User interface
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # Adjust sequence table header columns
    ui.sequence_tableWidget.setColumnWidth(0, 300)
    ui.sequence_tableWidget.setColumnWidth(1, 300)

    # Handles CAN communication
    can = CAN((status, ui))
    can.setup()

    # Handles TCP/IP Communication
    stm24 = STM24((status, ui))

    # Setup Tests
    tests = Tests((status, ui, stm24))

    # Handles Events
    events = EventHandler((app, ui, tests, stm24))

    # Start up a status thread. This monitors the system.
    statusThread = StatusThread(1, "SystemStatus", stm24)
    statusThread.start()

    MainWindow.show()
    sys.exit(app.exec_())