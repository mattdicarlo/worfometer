from api import get_rotations_data
from datetime import timedelta
from util import utc_now, ceil_dt, rotations_to_meters, meters_to_miles
import flask


bp = flask.Blueprint('routes', __name__)


@bp.route('/', methods=['GET'])
def index():
    now = utc_now()
    last_day_interval = timedelta(minutes=5)
    last_day_start = ceil_dt(now - timedelta(hours=24), last_day_interval)

    last_day_data = get_rotations_data(start=last_day_start, end=now, interval=last_day_interval)
    last_day_rotations = sum([ii[1] for ii in last_day_data])
    last_day_distance = rotations_to_meters(last_day_rotations)

    last_week_interval = timedelta(hours=1)
    last_week_start = ceil_dt(now - timedelta(days=7), last_week_interval)
    last_week_data = get_rotations_data(start=last_week_start, end=now, interval=last_week_interval)
    last_week_rotations = sum([ii[1] for ii in last_week_data])
    last_week_distance = rotations_to_meters(last_week_rotations)

    return flask.render_template(
        'index.html',
        last_day={
            'start_time': last_day_start,
            'end_time': now,
            'data': last_day_data,
            'interval': last_day_interval,
            'rotations': last_day_rotations,
            'distance_meters': last_day_distance,
            'distance_miles': meters_to_miles(last_day_distance),
        },
        last_week={
            'start_time': last_week_start,
            'end_time': now,
            'data': last_week_data,
            'interval': last_week_interval,
            'rotations': last_week_rotations,
            'distance_meters': last_week_distance,
            'distance_miles': meters_to_miles(last_week_distance),
        },
    )
