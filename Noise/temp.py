from __future__ import print_function
import datetime
import argparse
import socket
import os

import can
from can.io.logger import Logger


def main():
    #['critical', 'error', 'warning', 'info', 'debug', 'subdebug'][min(5, verbosity)]
    logging_level_name = 'info'
    can.set_logging_level(logging_level_name)

    can_filters = []
    config = {"can_filters": can_filters, "single_handle": True}
    config["bustype"] = 'vector'
    config["bitrate"] = 500000

    bus = can.interface.Bus(0, **config)
    print('Connected to {}: {}'.format(bus.__class__.__name__, bus.channel_info))
    print('Can Logger (Started on {})\n'.format(datetime.datetime.now()))

    prev_position = 0
    wakeup_msg = can.Message(arbitration_id=0x59e, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False)

    try:
        bus.send(wakeup_msg)
        while True:
            msg = bus.recv(1)
            if msg is not None:
                if msg.arbitration_id == 0x5a:
                    position = (msg.data[3] & 0xf8) >> 3
                    bus.send(wakeup_msg)
                    if (prev_position != position):
                        if (position == 0x01):
                            print("Park")
                        if (position == 0x02):
                            print("Reverse")
                        if (position == 0x04):
                            print("Neutral")
                        if (position == 0x08):
                            print("Drive")
                        if (position == 0x16):
                            print("Sport")

                    prev_position = position

    except KeyboardInterrupt:
        pass
    finally:
        bus.shutdown()

if __name__ == "__main__":
    main()
