import importlib

import eventlet
from eventlet import wsgi
import flask
from werkzeug.wsgi import DispatcherMiddleware

from omechat import cfg


def create_app_dispatcher():

    # Create mounts dict from config info
    mounts = {}
    for route, qualname in cfg.DISPATCHER_MOUNTS:
        module_qualname, obj_qualname = qualname.split(':', 1)
        print(module_qualname, obj_qualname)
        module = importlib.import_module(module_qualname)
        obj = module
        for name in obj_qualname.split('.'):
            obj = getattr(obj, name)
        app = obj
        mounts[route] = app


    # Base app should just redirect to the first app listed
    base_app = flask.Flask('base')
    base_app.add_url_rule('/', view_func=lambda: flask.redirect(
        cfg.DISPATCHER_MOUNTS[0][0]))

    return DispatcherMiddleware(base_app, mounts=mounts)

app_dispatcher = create_app_dispatcher()
