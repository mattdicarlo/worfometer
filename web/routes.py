from datetime import datetime, timedelta
from persistence import get_db
from util import utc_now, ceil_dt
import flask


bp = flask.Blueprint('routes', __name__)


def interval_dts(start: datetime, interval: timedelta, stop: datetime):
    nn = start
    while nn <= stop:
        yield nn
        nn += interval


def rotations_to_meters(rotations: int) -> float:
    # The wheel is 10.5" at the outside and 9.5" at the inside, so
    # let's call it 10" or .254 meters, which makes the circumference
    # 2 × pi × (0.254 m / 2) = 0.797964534 m
    return rotations * 0.797964534


@bp.route('/', methods=['GET'])
def index():
    datapoints = []
    total_rotations = 0

    db = get_db()
    cur = db.cursor()
    try:
        now = utc_now()
        interval = timedelta(minutes=5)
        start_time = ceil_dt(now - timedelta(hours=24), interval)
        for interval_start in interval_dts(start_time, interval, now):
            interval_end = interval_start + interval
            res = cur.execute(
                """SELECT SUM(rotations)
                   FROM odometer_event
                   WHERE event_time >= ? AND event_time < ?;
                """,
                [interval_start, interval_end]
            )
            rotations = res.fetchone()[0] or 0
            datapoints.append([interval_start, rotations, rotations_to_meters(rotations)])
            total_rotations += rotations
        #start_time = now - timedelta(hours=12)
        #res = cur.execute(
        #    """SELECT event_time, rotations
        #       FROM odometer_event
        #       WHERE event_time >= ?;
        #    """,
        #    [start_time]
        #)
        #
        #datapoints = [{'x': ii[0], 'y': ii[1]} for ii in res]

    finally:
        cur.close()

    total_distance = rotations_to_meters(total_rotations)

    return flask.render_template(
        'index.html',
        start_time=start_time,
        end_time=now,
        datapoints=datapoints,
        total_rotations=total_rotations,
        total_distance=total_distance,
    )
