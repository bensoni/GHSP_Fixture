#!/usr/bin/env python
"""
logger.py logs CAN traffic to the terminal and to a file on disk.

    logger.py can0

See candump in the can-utils package for a C implementation.
Efficient filtering has been implemented for the socketcan backend.
For example the command

    logger.py can0 F03000:FFF000

Will filter for can frames with a can_id containing XXF03XXX.

Dynamic Controls 2010
"""
from __future__ import print_function
import datetime
import argparse
import socket
import os

import can
from can.io.logger import Logger


def main():
    parser = argparse.ArgumentParser(
        "python -m can.logger",
        description="Log CAN traffic, printing messages to stdout or to a given file")

    parser.add_argument("-f", "--file_name", dest="log_file",
                        help="""Path and base log filename, extension can be .txt, .asc, .csv, .db, .npz""",
                        default=None)

    parser.add_argument("-v", action="count", dest="verbosity",
                        help='''How much information do you want to see at the command line?
                        You can add several of these e.g., -vv is DEBUG''', default=2)

    parser.add_argument('-c', '--channel', help='''Most backend interfaces require some sort of channel.
    For example with the serial interface the channel might be a rfcomm device: "/dev/rfcomm0"
    With the socketcan interfaces valid channel examples include: "can0", "vcan0"''')

    parser.add_argument('-i', '--interface', dest="interface",
                        help='''Specify the backend CAN interface to use. If left blank,
                        fall back to reading from configuration files.''',
                        choices=can.VALID_INTERFACES)

    parser.add_argument('--filter', help='''Comma separated filters can be specified for the given CAN interface:
        <can_id>:<can_mask> (matches when <received_can_id> & mask == can_id & mask)
        <can_id>~<can_mask> (matches when <received_can_id> & mask != can_id & mask)
    ''', nargs=argparse.REMAINDER, default='')

    parser.add_argument('-b', '--bitrate', type=int,
                        help='''Bitrate to use for the CAN bus.''')

    results = parser.parse_args()

    verbosity = results.verbosity

    logging_level_name = ['critical', 'error', 'warning', 'info', 'debug', 'subdebug'][min(5, verbosity)]
    can.set_logging_level(logging_level_name)

    can_filters = []
    if len(results.filter) > 0:
        print('Adding filter/s', results.filter)
        for filt in results.filter:
            if ':' in filt:
                _ = filt.split(":")
                can_id, can_mask = int(_[0], base=16), int(_[1], base=16)
            elif "~" in filt:
                can_id, can_mask = filt.split("~")
                can_id = int(can_id, base=16) | 0x20000000    # CAN_INV_FILTER
                can_mask = int(can_mask, base=16) & socket.CAN_ERR_FLAG
            can_filters.append({"can_id": can_id, "can_mask": can_mask})

    config = {"can_filters": can_filters, "single_handle": True}
    if results.interface:
        config["bustype"] = results.interface
    if results.bitrate:
        config["bitrate"] = results.bitrate
    bus = can.interface.Bus(results.channel, **config)
    print('Connected to {}: {}'.format(bus.__class__.__name__, bus.channel_info))
    print('Can Logger (Started on {})\n'.format(datetime.datetime.now()))
    logger = Logger(results.log_file)
	
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
                            os.system('cls')
                            print("Park")
                        if (position == 0x02):
                            os.system('cls')
                            print("Reverse")
                        if (position == 0x04):
                            os.system('cls')
                            print("Neutral")
                        if (position == 0x08):
                            os.system('cls')
                            print("Drive")
                        if (position == 0x16):
                            os.system('cls')
                            print("Sport")

                    prev_position = position