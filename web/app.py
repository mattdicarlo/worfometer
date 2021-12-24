
import flask
import routes
import persistence


def create_app(extra_config=None):
    """ Create the flask application.
        Accepts an optional config dictionary, which allows overriding the
        configuration file for things like unit tests.
    """

    app = flask.Flask(__name__)

    # Unless the caller overrides the configuration, load it from file.
    app.config.from_pyfile('config.py')
    app.config.from_pyfile('local_config.py', silent=True)

    if extra_config is not None:
        app.config.from_mapping(extra_config)

    setup_logging(app)
    persistence.setup_context(app)

    # Apply blueprints to set up routing
    app.register_blueprint(routes.bp)

    register_filters(app)

    # register_error_handlers(app)
    # register_context_handlers(app)

    if app.config.get('FF_STRICT_TEMPLATES', False):
        from jinja2 import StrictUndefined
        app.jinja_env.undefined = StrictUndefined

    return app


def setup_logging(app):
    app.logger.setLevel(app.config.get('LOG_LEVEL'))


def register_filters(app):
    from datetime import datetime, timedelta

    def dt_iso(value: datetime):
        # YYYY-MM-DDTHH:mm:ss.sssZ
        # return value.strftime('%Y-%m-%dT%H:%M:%S.000%z')
        return value.isoformat()

    def humanize_filter(value):
        import humanize
        if isinstance(value, timedelta):
            return humanize.precisedelta(value, minimum_unit='seconds')
        elif isinstance(value, float):
            return humanize.intcomma(value, ndigits=1)
        elif isinstance(value, int):
            return humanize.intcomma(value)

    app.jinja_env.filters['dt_iso'] = dt_iso
    app.jinja_env.filters['humanize'] = humanize_filter
