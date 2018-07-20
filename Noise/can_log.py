"""
Title:          CAN Logger
Filename:       can_log.py
Authors:        Isaac Benson & Ryan Borgeson
Version:        1.0

Description:    This python script handles monitoring the CAN bus, it is currently configured to automatically connect
                to CAN channel 1 and update checkboxes for CAN communication status and brake status, as well as
                updating the shifter position dial.

                TO CHANGE CAN CHANNELS:

                line 64:  CAN_channel = 1;
                ^^^^^^^^^^^^^^^^^^^^^^^^^^
                change the CAN channel on line 64 to the CAN channel you are physically connected to on the CAN box.
"""

from gui import Ui_MainWindow
import ctypes

import threading
import datetime
import argparse
import socket
import os

import can
from can.io.logger import Logger

class CAN(object):
    #Initialize script, pass ui file into script to allow it to update the GUI
    def __init__(self, services):
        (self.status, self.ui) = services

    #Start receive thread
    def setup(self):
        self.ui.diagnostics_textEdit.append("Setting up CAN Communication...")
        self.receiveThread = CAN_ReceiveThread(2, "CAN-Thread", self.ui)
        self.receiveThread.start()


#Monitors the CAN bus, and sends wakeup frames to the shifter
class CAN_ReceiveThread(threading.Thread):
    def __init__(self, threadID, threadName, ui):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = threadName
        self.ui = ui

    def run(self):
        try:
            #Set logging level to info
            logging_level_name = 'info'
            can.set_logging_level(logging_level_name)

            #Set up filters, currently the logger will not filter any messages out
            can_filters = []
            config = {"can_filters": can_filters, "single_handle": True}

            #Use vector box backend
            config["bustype"] = 'vector'

            #Choose a CAN channel to connect to
            CAN_channel = 1;

            #Connect to the chosen CAN channel, index is moved back by one because physical CAN channels
            #Range from (1, 2, 3, 4, 5....N) whereas the index of the channels is (0, 1, 2, 3, 4...N-1)
            bus = can.interface.Bus(CAN_channel - 1, **config)

            prev_position = 0
            wakeup_msg = can.Message(arbitration_id=0x59e, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False)

            try:
                #Send wakeup message
                bus.send(wakeup_msg)

                while True:
                    #Wait for a CAN message
                    msg = bus.recv(1)

                    #If a valid message was received
                    if msg is not None:

                        #If message received was Gear_Shift_by_Wire, obtain the current position and update dial
                        if (msg.arbitration_id == 0x5a):
                            position = (msg.data[3] & 0xf8) >> 3
                            bus.send(wakeup_msg)
                            if (prev_position != position):
                                if (position == 0x01):
                                    self.ui.dial.setProperty("value", 1)
                                if (position == 0x02):
                                    self.ui.dial.setProperty("value", 2)
                                if (position == 0x04):
                                    self.ui.dial.setProperty("value", 3)
                                if (position == 0x08):
                                    self.ui.dial.setProperty("value", 4)
                                if (position == 0x16):
                                    self.ui.dial.setProperty("value", 5)
                            prev_position = position
                            self.ui.canCom_checkBox.setChecked(True)

                        #If message received was Body_Info_4_HS2, obtain brake status and update brake checkbox
                        if (msg.arbitration_id == 0x242):
                            brake = (msg.data[2] & 0x80) >> 7
                            if (brake == 0x01):
                                self.ui.brakeEngaged_checkBox.setChecked(True)
                            if (brake == 0x00):
                                self.ui.brakeEngaged_checkBox.setChecked(False)




            #Handle keyboard interrupts (mainly for proper exit upon Ctrl + C shutdown)
            except KeyboardInterrupt:
                pass
            finally:
                bus.shutdown()
        except KeyboardInterrupt:
            pass
