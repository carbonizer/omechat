"""
omechat.__main__
================

Entry-point for running the web app
"""
import argparse
import os
import sys

import parawrap
from werkzeug.serving import run_simple

from omechat import cfg
from omechat.dispatcher import app_dispatcher


class MixedHelpFormatter(argparse.ArgumentDefaultsHelpFormatter,
                         argparse.RawDescriptionHelpFormatter):
    """Combo of arg default and raw description help formatters"""
    pass


def parse_args(args):
    parser = argparse.ArgumentParser()
    # subparsers = parser.add_subparsers()
    # config_web_parser(subparsers.add_parser('web'))
    config_web_parser(parser, is_primary=True)
    return parser.parse_args(args)


def config_web_parser(parser: argparse.ArgumentParser, is_primary=False):
    """Configure the argument parser for the web command

    Args:
        parser: The parser to configure
        is_primary: True if configuring as the main command.  False if
            configuring as a sub-command.
    """
    parser.description = parawrap.fill(
        'Run builtin dev server or print a command that would run the server '
        'if the command were evaluated.  Although the production server will '
        'not be run directly, it could be run with:\n'
        '\n'
        '\t\'eval $({}{} web [OPTIONS] <production-server>)\''
        ''.format(cfg.PKG_NAME, '' if is_primary else ' web')
    )
    parser.formatter_class = MixedHelpFormatter
    parser.add_argument('--debug', '-d',
                        action='store_true',
                        help='Run the dev server with debug web iface and '
                             'reload server on source file changes')
    parser.add_argument('--host',
                        default=cfg.WEB_HOST,
                        help='Server host/name')
    parser.add_argument('--port', '-p',
                        type=int, default=cfg.WEB_PORT,
                        help='Port on which the server listens')
    parser.add_argument('server',
                        choices=('builtin', 'eventlet', 'gunicorn'), default='builtin',
                        help='Run builtin dev server or print command '
                             'related to running a specific production server')
    parser.set_defaults(func=web_cmd)


def web_cmd(pargs):
    """Run web server"""
    host = pargs.host
    port = pargs.port

    for app in app_dispatcher.mounts.values():
        app.debug = pargs.debug
    d = {
        'use_reloader': pargs.debug,
        'use_debugger': pargs.debug,
    }

    # If ssl cert and key are in place, add an ssl context
    # if all((pargs.ssl, all(map(os.path.exists, (cfg.SERVER_CRT_PATH,
    #                                             cfg.SERVER_KEY_PATH))))):
    #     d['ssl_context'] = (cfg.SERVER_CRT_PATH, cfg.SERVER_KEY_PATH)

    if pargs.server == 'builtin':
        # Since app is a DispatcherMiddleware object, it doesn't have a run()
        # method, so we use run_simple() instead (which is the method that run()
        # ultimately calls.
        run_simple(host, port, app_dispatcher, **d)
    elif pargs.server == 'eventlet':
        import eventlet
        import eventlet.wsgi

        eventlet.wsgi.server(eventlet.listen(('', 5000)), app_dispatcher)
    else:
        print('Unable to run server internally, you can run:', file=sys.stderr)
        cmd = None
        if pargs.server == 'gunicorn':
            chunks = ['gunicorn -b{host}:{port}']
            # if 'ssl_context' in d:
            #     chunks.append(
            #         '--certfile {ssl_context[0]} --keyfile {ssl_context[1]}'
            #     )
            chunks.append('omechat.dispatcher:app_dispatcher')
            cmd = ' '.join(chunks).format(host=host, port=port, **d)
        return cmd


def main(args=sys.argv[1:]):
    pargs = parse_args(args)
    web_cmd(pargs)


if __name__ == '__main__':
    main()
