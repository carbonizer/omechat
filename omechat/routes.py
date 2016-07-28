"""
omechat.routes
==============

Configures the routes of the application

Routes are usually configured on the global app instance directly.  However,
doing so in functions aids unit testing and debugging.
"""
import flask


def config_hello_route(app):
    """Configure the single route, hello

    Args:
        app (flask.Flask): App to configure

    Returns:
        flask.Flask: Same object that was passed in
    """

    @app.route('/hello')
    def hello():
        """Good to keep around for sanity checks"""
        return 'Hello World!'

    return app


def config_routes(app):
    """Configure all app routes

    Args:
        app (flask.Flask): App to configure

    Returns:
        flask.Flask: Same object that was passed in
    """
    config_hello_route(app)

    @app.route('/')
    def my_index():
        return flask.render_template('omechat/index.jinja')

    return app
