import flask

from omechat import logr


def config_socketio_events(app):
    try:
        socketio = app.extensions['socketio']
    except KeyError:
        raise AssertionError('App must be initialized with SocketIO')

    @socketio.on('my event')
    def handle_my_custom_event(json):
        print('received json: ' + str(json))

    @socketio.on('message')
    def handle_message(msg):
        logr.debug('Received message {!r}'.format(msg))
        socketio.emit('message', {
            'body': msg,
            'from': 'user' + flask.request.sid[:6],
        })
