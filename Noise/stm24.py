#############################################################
# STM24 Handles communication between the host and the
# STM24-IP 3EE by opening a socket to the stepper motor.
# Commands are sent over UDP.
#############################################################
import socket
import binascii
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QWidget


class STM24(QWidget):

    ##
    # Initializes STM24 and opens a socket to the stepper motor.
    # @param services Injects services into class.
    #
    def __init__(self, services):
        (self.status, self.ui) = services

        self.ui.diagnostics_textEdit.append("Setting up communication with STM24...")
                
        # UDP IP & Port
        self.UDP_IP = "10.10.10.11"
        self.UDP_PORT = 7777

        # Stepper motor IP & Port
        self.STM_IP = "10.10.10.10"
        self.STM_PORT = 7775

        # Attempt to connect to STM24 and send command.
        try:
            # Open socket to stepper motor.
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.UDP_IP, self.UDP_PORT))
            self.sock.connect((self.STM_IP, self.STM_PORT))

            # Step up thread to handle STM24 responses.
            self.receiveThread = STM24_ReceiveThread(1, "STM24-IP", self.sock, self.ui, self.status)
            self.receiveThread.start()
            self.status.setStmStatus(True)

        except Exception:
            self.ui.diagnostics_textEdit.append("Failed to setup communication with STM24...")
            self.status.setStmStatus(False)
 
    ##
    # Send - Used to send data to the STM24
    # @param data Data or command to send.
    #
    def send(self, data):
        self.sock.sendto(bytes.fromhex(data), (self.STM_IP, self.STM_PORT))

    ##
    # Send command
    # Sends a command to the STM24 over the specified UDP socket. Commands
    # are converted from ASCII to hex automatically.
    # @param cmd The command in ASCII format.
    def sendCmd(self, cmd):
        sclString = cmd.encode('utf-8').hex()
        sendBytes = "0007"
        sendBytes = sendBytes + sclString + "0d"
        self.send(sendBytes)


##
# STM24 Receive Thread
# Handles recieved packets over the socket and updates the user interface
# were necessary.
#
class STM24_ReceiveThread(QThread):

    def __init__(self, threadID, threadName, sock, ui, status):
        QThread.__init__(self)
        self.threadID = threadID
        self.name = threadName
        self.sock = sock
        self.ui = ui
        self.status = status

    def __del__(self):
        self.wait()

    def run(self):
        # Continue to receive responses from the STM24
        while True:
            response, addr = self.sock.recvfrom(1024)
            asciiResp = bytearray.fromhex(bytearray.fromhex(binascii.hexlify(response).hex()).decode()).decode().replace("\r","").replace("\n","")

            # Immediate Temperature
            if "IT" in asciiResp:
                data = asciiResp.split("=")
                temp = int(data[1], 16)
                self.ui.temperature_label.setText(str(round(temp * 0.1, 2)))

            # Encoder Position data register
            if "RXe" in asciiResp:
                data = asciiResp.split("=")
                position = int(data[1], 10)
                self.ui.position_label.setText(str(position))


            self.status.updateLastPacketTime()
            