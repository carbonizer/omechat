"""
omechat.app
===========

Create and configure the global app instance

Production servers usually need to access the global app instance.
"""
from werkzeug.wsgi import DispatcherMiddleware

from omechat import create_app
from omechat.routes import config_hello_route, config_routes
from omechat.socketio_ import config_socketio_events


def create_and_config_hello_app():
    """Create and configure a simple app, helpful for some unit testing

    Returns:
        flask.Flask: Simple hello app
    """
    return config_hello_route(create_app())


def create_and_config_app():
    """Create and configure the main app

        Returns:
            flask.Flask: Main app instance
    """
    app_ = config_routes(create_app())
    config_socketio_events(app_)
    return app_


app = create_and_config_app()
