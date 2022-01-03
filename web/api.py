from datetime import timedelta, datetime
from persistence import use_cursor
from util import interval_dts, rotations_to_meters
import flask


bp = flask.Blueprint('api', __name__)


def get_rotations_data(start: datetime, end: datetime, interval: timedelta):
    datapoints = []

    with use_cursor() as cursor:
        for interval_start in interval_dts(start, interval, end):
            interval_end = interval_start + interval
            res = cursor.execute(
                """SELECT SUM(rotations)
                   FROM odometer_event
                   WHERE event_time >= ? AND event_time < ?;
                """,
                [interval_start, interval_end]
            )
            rotations = res.fetchone()[0] or 0
            datapoints.append([interval_start, rotations, rotations_to_meters(rotations)])

    return datapoints


def get_rotations_sum(start: datetime, end: datetime):
    with use_cursor() as cursor:
        res = cursor.execute(
            """SELECT SUM(rotations)
               FROM odometer_event
               WHERE event_time >= ? AND event_time < ?;
            """,
            [start, end]
        )
        rotations = res.fetchone()[0] or 0
        return rotations


@bp.route('/api/v1/rotations', methods=['GET'])
def get_rotations():
    pass
