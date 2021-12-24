from datetime import datetime, timezone, timedelta


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def to_utc(dt) -> datetime:
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


datetime_min_utc = to_utc(datetime.min)


def ceil_dt(dt: datetime, delta: timedelta) -> datetime:
    """ Round a datetime up to the nearest interval, as determined by delta.
        ex: delta=timedelta(minutes=1) will round up to the nearest minute
    """
    minimum = datetime.min
    if dt.tzinfo is not None:
        if dt.tzinfo != timezone.utc:
            raise ValueError("I didn't write any code to handle non-UTC timezones")
        minimum = datetime_min_utc
    return dt + (minimum - dt) % delta


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


def meters_to_miles(meters: float) -> float:
    return meters / 1609.344
