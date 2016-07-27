# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import errno
import json
import logging
import sys
import tornado.ioloop

from .settings import settings
from .server import Application as ServerApplication
from .utils import merge
from .utils.ops import get_endpoint_app

__all__ = ['start_server', 'start_endpoint']

logger = logging.getLogger('api.start')


def start_server():
    """Start server process with all supported endpoints."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--name', dest='name')
    arg_parser.add_argument('--port', dest='port', type=int, default=None)
    arg_parser.add_argument('--settings', dest='settings', default='{}')
    args = arg_parser.parse_args()

    name = args.name or settings['default_server_name']
    port = args.port or settings['default_server_port']
    server_settings = json.loads(args.settings)
    server_settings = merge(settings, server_settings)

    try:
        logger.info("Starting server '%s' on port %i", name, port)
        application = ServerApplication(**server_settings)
        application.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except:
        logger.exception("Failed to start server '%s' on port %i", name, port)
        sys.exit(errno.EINTR)


def start_endpoint():
    """Start process for a specific endpoint."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('name')
    arg_parser.add_argument('port', type=int)
    arg_parser.add_argument('--settings', dest='settings', default='{}')
    args = arg_parser.parse_args()

    name = args.name
    port = args.port
    endpoint_settings = json.loads(args.settings)
    endpoint_settings = merge(settings, endpoint_settings)

    if name not in settings['registered_endpoints']:
        logger.info("Unsupported endpoint '%s'", name)
        logger.info("Possible values: %s",
                    json.dumps(settings['registered_endpoints']))
        sys.exit(errno.EACCES)

    try:
        logger.info("Starting server '%s' on port %i", name, port)
        application = get_endpoint_app(name)(**endpoint_settings)
        application.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except:
        logger.exception("Failed to start server '%s' on port %i", name, port)
        sys.exit(errno.EINTR)


if __name__ == '__main__':
    start_server()
