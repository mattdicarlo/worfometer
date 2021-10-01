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
            datapoints.append([interval_start, rotations])
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

    return flask.render_template(
        'index.html',
        start_time=start_time,
        end_time=now,
        datapoints=datapoints,
        total_rotations=total_rotations,
    )
