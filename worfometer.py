#!/usr/bin/env python3

from odometer import Odometer
from persistence import init_db, add_rotations
import os
import sqlite3
import sys
import time


def main():
    db_path = os.path.join(os.path.dirname(__file__), 'worfometer.sqlite')

    try:
        connection = sqlite3.connect(db_path)
        init_db(connection)

        odometer = Odometer()

        while True:
            rotations, timestamp = odometer.check_rotations()
            if rotations > 0:
                add_rotations(connection, timestamp, rotations)

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
