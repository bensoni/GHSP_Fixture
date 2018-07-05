from gui import Ui_MainWindow
import ctypes

class CAN(object):
    def __init__(self, services):
        (self.status, self.ui) = services

    def setup(self):
        self.ui.diagnostics_textEdit.append("Setting up CAN Communication...")

        # Load Vector API dll.
        #vxlapi = ctypes.WinDLL("vxlapi/vxlapi.dll")

        # Redefine functions from dll.
        #openDriver = vxlapi.xlOpenDriver
        
        # Attempt to open driver and append the return status.
        #self.status = openDriver()
        #self.ui.diagnostics_textEdit.append("xlOpenDriver Status: " + str(self.status))
