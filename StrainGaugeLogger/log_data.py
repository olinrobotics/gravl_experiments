#!/usr/bin/env python3.6

from argparse import ArgumentParser
import csv
import re

from serial import Serial
from time import sleep

def wait_for_units(ser):
    """Waits for unit msg from serial port obj.

    Args:
        ser: (serial.Serial) port obj from which to get msgs

    Returns:
        str: of units

    """
    while True:
        data_re = re.search("\(([a-zA-Z]*)\)", str(ser.readline()))
        if data_re is not None:
            return data_re.group(1)


def capture_data(port, file, dur=0, baud=9600, display=False):
    """Record playing data to file f for duration d.

    Args:
        port: (string) port to which to connect
        file: (pathlib Path) csv file to which to write
        duration: (int) seconds to log - 0 logs indefinitely
        baud: (int) baud rate to use for serial connection
        display: (bool) printing to the terminal

    """
    ser = Serial(port, baud)
    units = wait_for_units(ser)
    print(f"Units: {units}")
    with open(file, mode='w') as io_obj:
        writer = csv.writer(
            io_obj, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Time (s)", f"Units ({units})"])
        while True:
            data_re = re.search("([0-9.-]+) ([0-9.-]+)", str(ser.readline()))
            if data_re is not None:
                data = [float(data_re.group(1)), float(data_re.group(2))]
                writer.writerow(data)
                if display:
                    print(data)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('data_file', type=str,
        help='filepath of new file to which to write')
    parser.add_argument('-d', '--duration', type=int, default=0,
        help='Number of seconds for which to record data')
    parser.add_argument('-p', '--print', action='store_true',
        help='Flag for printing to terminal')

    args = vars(parser.parse_args())
    data_file = args['data_file']
    duration = args['duration']
    display = args['print']
    capture_data('/dev/ttyACM0', data_file, display=display)
