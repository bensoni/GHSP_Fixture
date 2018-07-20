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
    def __init__(self, services):
        (self.status, self.ui) = services

    def setup(self):
        self.ui.diagnostics_textEdit.append("Setting up CAN Communication...")
        self.receiveThread = CAN_ReceiveThread(2, "CAN-Thread", self.ui)
        self.receiveThread.start()



class CAN_ReceiveThread(threading.Thread):
    def __init__(self, threadID, threadName, ui):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = threadName
        self.ui = ui

    def run(self):
        try:
            # ['critical', 'error', 'warning', 'info', 'debug', 'subdebug'][min(5, verbosity)]
            logging_level_name = 'info'
            can.set_logging_level(logging_level_name)

            can_filters = []
            config = {"can_filters": can_filters, "single_handle": True}
            config["bustype"] = 'vector'
            #config["bitrate"] = 500000

            bus = can.interface.Bus(0, **config)
            #print('Connected to {}: {}'.format(bus.__class__.__name__, bus.channel_info))
            #print('Can Logger (Started on {})\n'.format(datetime.datetime.now()))

            prev_position = 0
            wakeup_msg = can.Message(arbitration_id=0x59e, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False)
            #self.ui.brakeEngaged_checkBox.setEnabled(False)
            #self.ui.canCom_checkBox.setEnabled(False)

            try:
                bus.send(wakeup_msg)

                while True:
                    msg = bus.recv(1)

                    if msg is not None:
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




                        if (msg.arbitration_id == 0x242):
                            brake = (msg.data[2] & 0x80) >> 7
                            if (brake == 0x01):
                                self.ui.brakeEngaged_checkBox.setChecked(True)
                            if (brake == 0x00):
                                self.ui.brakeEngaged_checkBox.setChecked(False)





            except KeyboardInterrupt:
                pass
            finally:
                bus.shutdown()
        except KeyboardInterrupt:
            pass
