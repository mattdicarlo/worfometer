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
