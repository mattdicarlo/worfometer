from api import get_rotations_data, get_rotations_sum
from datetime import datetime, timedelta
from util import utc_now, ceil_dt, rotations_to_meters, meters_to_miles
import flask


bp = flask.Blueprint('routes', __name__)


@bp.route('/', methods=['GET'])
def index():
    now = utc_now()

    last_day_interval = timedelta(minutes=5)
    last_day_start = ceil_dt(now - timedelta(hours=24), last_day_interval)
    last_day_data = get_rotations_data(start=last_day_start, end=now, interval=last_day_interval)
    last_day_rotations = sum([ii['rotations'] for ii in last_day_data])
    last_day_distance = rotations_to_meters(last_day_rotations)

    last_week_interval = timedelta(hours=1)
    last_week_start = ceil_dt(now - timedelta(days=7), last_week_interval)
    last_week_data = get_rotations_data(start=last_week_start, end=now, interval=last_week_interval)
    last_week_rotations = sum([ii['rotations'] for ii in last_week_data])
    last_week_distance = rotations_to_meters(last_week_rotations)

    # The hedgie is nocturnal, so we treat day-by-day data as running from noon
    # of one day to noon of the next. To graph the last month, we want 1-day
    # chunks starting at either noon yesterday or today, depending on whether
    # it's past noon already.
    local_now = utc_now().astimezone()
    local_noon = datetime(local_now.year, local_now.month, local_now.day, hour=12).astimezone()
    last_month_end = local_noon if local_noon > local_now else local_noon - timedelta(days=1)
    last_month_start = last_month_end - timedelta(days=30)
    last_month_interval = timedelta(hours=24)
    last_month_data = get_rotations_data(start=last_month_start, end=last_month_end, interval=last_month_interval)
    last_month_rotations = sum([ii['rotations'] for ii in last_month_data])
    last_month_distance = rotations_to_meters(last_month_rotations)

    return flask.render_template(
        'index.html',
        last_day={
            'start_time': last_day_start,
            'end_time': now,
            'data': last_day_data,
            'interval': last_day_interval,
            'period': now - last_day_start,
            'rotations': last_day_rotations,
            'distance_meters': last_day_distance,
            'distance_miles': meters_to_miles(last_day_distance),
        },
        last_week={
            'start_time': last_week_start,
            'end_time': now,
            'data': last_week_data,
            'interval': last_week_interval,
            'period': now - last_week_start,
            'rotations': last_week_rotations,
            'distance_meters': last_week_distance,
            'distance_miles': meters_to_miles(last_week_distance),
        },
        last_month={
            'start_time': last_month_start,
            'end_time': last_month_end,
            'data': last_month_data,
            'interval': last_month_interval,
            'period': last_month_end - last_month_start,
            'rotations': last_month_rotations,
            'distance_meters': last_month_distance,
            'distance_miles': meters_to_miles(last_month_distance),
        }
    )
