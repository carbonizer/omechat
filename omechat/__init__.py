"""
omechat
=======

Flask web backend app
"""
from datetime import datetime
import os

import flask
from flask_socketio import SocketIO

import omechat.config as cfg

__version__ = '0.1a1'

logr = cfg.logr


class JSONEncoderWrapper(object):
    """Add support for more types to the json encoder

    if `default` and `for_json` are used, then if an object has a
    `for_json` attribute, it will be used.  Otherwise, it will fallback on
    `default`

    flask uses a `TaggedJSONSerializer` on sessions which will be try
     converting various types before giving `default` a try.

    """

    def __new__(cls, *args, **kwargs):
        kwargs.update(dict(
            default=cls.default_override,
            for_json=True,
        ))
        return flask.json.JSONEncoder(*args, **kwargs)

    @staticmethod
    def default_override(o):
        # Create a dict of object instance variables and properties
        try:
            # Include instance variables
            d = dict(o.__dict__)
            # Include properties
            d.update({k: getattr(o, k)
                      for k, v in o.__class__.__dict__.items()
                      if isinstance(v, property)})
        except (AttributeError, TypeError):
            pass
        else:
            return d

        if isinstance(o, set):
            return list(o)

        if isinstance(o, datetime):
            return str(o)

        # If this method couldn't convert the object
        raise TypeError(repr(o) + " is not JSON serializable")


def create_app(config_obj=cfg.FlaskAppConfig):
    """Flask app factory

    Returns:
        flask.Flask: An app configured for various extensions
    """
    app = flask.Flask(__name__)
    app.config.from_object(config_obj)

    app.json_encoder = JSONEncoderWrapper

    # Override the flask logger
    # Note that logging the web server underneath has to be done separately
    app._logger = logr

    # Create a random secret key used for session security, unless already set
    if not os.path.exists(cfg.SECRET_KEY_PATH):
        with open(cfg.SECRET_KEY_PATH, 'wb') as fp:
            fp.write(os.urandom(24))

    with open(cfg.SECRET_KEY_PATH, 'rb') as fp:
        app.secret_key = fp.read()

    socketio = SocketIO(app)

    return app
