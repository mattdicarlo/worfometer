#!/usr/bin/env python3

from argparse import ArgumentParser
from odometer import Odometer, MockOdometer
from persistence import init_db, add_rotations
import os
import sqlite3
import sys
import time


def main():
    parser = ArgumentParser(description="Monitor Worf's wheel and write stats to a database.")
    parser.add_argument('--mock', action='store_true',
                        help='Use the mock odometer instead of reading the hardware.')
    parser.add_argument('--db', help='The path to the database file.')
    args = parser.parse_args()

    db_path = args.db or os.path.join(os.path.dirname(__file__), '..', 'worfometer.sqlite')

    try:
        connection = sqlite3.connect(db_path)
        init_db(connection)

        odometer = MockOdometer() if args.mock else Odometer()

        while True:
            rotations, timestamp = odometer.check_rotations()
            if rotations > 0:
                add_rotations(connection, rotations, timestamp)

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
