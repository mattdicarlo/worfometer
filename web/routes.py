from datetime import timedelta
from persistence import get_db
from util import utc_now, ceil_dt, interval_dts, rotations_to_meters, meters_to_miles
import flask
import humanize


bp = flask.Blueprint('routes', __name__)


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

        # start_time = now - timedelta(hours=12)
        # res = cur.execute(
        #     """SELECT event_time, rotations
        #        FROM odometer_event
        #        WHERE event_time >= ?;
        #     """,
        #     [start_time]
        # )
        # datapoints = [{'x': ii[0], 'y': ii[1]} for ii in res]

    finally:
        cur.close()

    total_distance = rotations_to_meters(total_rotations)

    return flask.render_template(
        'index.html',
        start_time=start_time,
        end_time=now,
        datapoints=datapoints,
        datapoints_interval=interval,
        total_rotations=total_rotations,
        total_distance_meters=total_distance,
        total_distance_miles=meters_to_miles(total_distance),
    )
