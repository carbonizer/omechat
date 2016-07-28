import os
import logging.config

PKG_NAME = 'omechat'
PKG_VAR_ROOT = os.path.join(os.path.expandvars('$HOME'), '.{}'.format(PKG_NAME))
PKG_LOG_ROOT = os.path.join(PKG_VAR_ROOT, 'logs')
PKG_LOG_PATH = os.path.join(PKG_LOG_ROOT, '{}.log'.format(PKG_NAME))

for dir_path in (PKG_LOG_ROOT,):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            # 10, 1 MB logs max
            'filename': PKG_LOG_PATH,
            'mode': 'a',
            'maxBytes': 1024**2,
            'backupCount': 10,
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'DEBUG',
    }
})

logr = logging.getLogger()


WEB_HOST = '0.0.0.0'
WEB_PORT = '5000'

SECRET_KEY_PATH = os.path.join(PKG_VAR_ROOT, 'secret_key')

DISPATCHER_MOUNTS = (
    ('/omechat', 'omechat.app:app.wsgi_app'),
)
"""Sequence of route/__qualname__ pairs for the DispatcherMiddleware"""


class FlaskAppConfig(object):
    # http://flask.pocoo.org/docs/latest/config/
    pass
