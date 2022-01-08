from datetime import timedelta, datetime
from persistence import use_cursor
from util import interval_dts, rotations_to_meters, meters_to_miles, utc_now, ceil_dt
import flask
import humanize


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


@bp.route('/api/v1/rotations/summary', methods=['GET'])
def get_rotations():
    now = utc_now()

    last_day_start = now - timedelta(hours=24)
    last_day_rotations = get_rotations_sum(last_day_start, now)
    last_day_distance = rotations_to_meters(last_day_rotations)

    last_week_start = now - timedelta(days=7)
    last_week_rotations = get_rotations_sum(last_week_start, now)
    last_week_distance = rotations_to_meters(last_week_rotations)

    last_month_start = now - timedelta(days=30)
    last_month_rotations = get_rotations_sum(last_month_start, now)
    last_month_distance = rotations_to_meters(last_month_rotations)

    htd = lambda td: humanize.precisedelta(td, minimum_unit='seconds')

    return flask.jsonify({
        'last_day': {
            'start_time': last_day_start,
            'end_time': now,
            'period': htd(now - last_day_start),
            'rotations': last_day_rotations,
            'distance_meters': last_day_distance,
            'distance_miles': meters_to_miles(last_day_distance),
        },
        'last_week': {
            'start_time': last_week_start,
            'end_time': now,
            'period': htd(now - last_week_start),
            'rotations': last_week_rotations,
            'distance_meters': last_week_distance,
            'distance_miles': meters_to_miles(last_week_distance),
        },
        'last_month': {
            'start_time': last_month_start,
            'end_time': now,
            'period': htd(now - last_month_start),
            'rotations': last_month_rotations,
            'distance_meters': last_month_distance,
            'distance_miles': meters_to_miles(last_month_distance),
        }
    })
