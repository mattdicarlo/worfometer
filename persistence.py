#!/usr/bin/env python3

from util import ceil_dt
from datetime import timedelta
import sqlite3


def init_db(db):
    cc = db.cursor()
    try:
        # If this fails, we need to set up the schema.
        cc.execute('SELECT 1 FROM odometer_event')
    except sqlite3.Error:
        print('Initializing new database...')
        cc.execute('CREATE TABLE odometer_event (event_time TIMESTAMP PRIMARY KEY, rotations INTEGER)')
        cc.execute('CREATE INDEX ix_odometer_event_time ON odometer_event (event_time);')
        db.commit()


default_event_delta = timedelta(minutes=1)


_upsert_query = """
    INSERT INTO odometer_event(event_time, rotations)
        VALUES(?, ?)
        ON CONFLICT(event_time) DO UPDATE SET rotations=rotations+?
"""


def add_rotations(db, rotations, timestamp, event_delta=default_event_delta):
    event_time = ceil_dt(timestamp, event_delta)

    cc = db.cursor()
    try:
        cc.execute(_upsert_query, (event_time, rotations, rotations))
        db.commit()
    finally:
        cc.close()
