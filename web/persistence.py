import flask
import sqlite3
import datetime


def get_db():
    """ Returns the database connection for the request context.
    """

    if 'db' not in flask.g:
        flask.g.db = sqlite3.connect(flask.current_app.config['DB_PATH'],
                                     detect_types=sqlite3.PARSE_DECLTYPES)
        sqlite3.register_converter("timestamp", _sqlite_convert_timestamp)

    return flask.g.db


def close_db(e=None):
    """ Closes the database connection for the request context, if there is one.
    """

    db = flask.g.pop('db', None)
    if db is not None:
        db.close()


def setup_context(app):
    """ Sets up the context management for the database session. This only needs
        to be called once on application creation, not each time get_db is used.
    """

    # This makes sure we clean up the database session at the end of the request.
    app.teardown_appcontext(close_db)


def _sqlite_convert_timestamp(val):
    """ Builtin timestamp converter barfs on "aware" timestamps if
        microseconds are 0.
        https://bugs.python.org/issue29099
    """

    datepart, timepart = val.split(b" ")

    # this is the patch
    timepart = timepart.split(b'+', 1)[0].split(b'-', 1)[0]

    year, month, day = map(int, datepart.split(b"-"))
    timepart_full = timepart.split(b".")
    hours, minutes, seconds = map(int, timepart_full[0].split(b":"))
    if len(timepart_full) == 2:
        microseconds = int('{:0<6.6}'.format(timepart_full[1].decode()))
    else:
        microseconds = 0
    val = datetime.datetime(year, month, day, hours, minutes, seconds,
                            microseconds)
    return val
