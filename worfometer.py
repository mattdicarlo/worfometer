#!/usr/bin/env python3

from datetime import timedelta
from persistence import init_db, add_rotations
from util import utc_now
import board
import digitalio
import os
import sqlite3
import sys
import time


def main():
    db_path = os.path.join(os.path.dirname(__file__), 'worfometer.sqlite')

    reed_switch = digitalio.DigitalInOut(board.D16)
    reed_switch.direction = digitalio.Direction.INPUT
    reed_switch.pull = digitalio.Pull.UP

    # The particular reed switch I have returns True when open,
    # False when closed.
    open_state = True

    # I don't think he can run quiiiiite this fast.
    debounce = timedelta(milliseconds=100)

    try:
        connection = sqlite3.connect(db_path)
        init_db(connection)

        previous_time = utc_now()
        previous_state = open_state
        total_rotations = 0
        while True:
            current_time = utc_now()
            delta = current_time - previous_time
            if delta < debounce:
                continue

            current_state = reed_switch.value
            if current_state != previous_state:
                previous_time = current_time
                previous_state = current_state
                if current_state != open_state:
                    add_rotations(connection, current_time, 1)
                    total_rotations += 1
                    print(f'count: {total_rotations}\tdelta: {delta.total_seconds() * 1000}ms')

            time.sleep(0.001)
    finally:
        connection.close()


if __name__ == '__main__':
    """ Called if this script is invoked directly.
    """

    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
