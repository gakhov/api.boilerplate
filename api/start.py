# -*- coding: utf-8 -*-

import argparse
import errno
import json
import logging
import sys
import tornado.ioloop

from .settings import settings
from .server import Application as ServerApplication
from .utils import merge

__all__ = ['start_server']

logger = logging.getLogger('api.start')


def start_server():
    """Start server process with all supported endpoints."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--name', dest='name')
    arg_parser.add_argument('--port', dest='port', type=int, default=None)
    arg_parser.add_argument('--settings', dest='settings', default='{}')
    arg_parser.add_argument('--endpoint', dest='endpoints', action='append')
    args = arg_parser.parse_args()

    name = args.name or settings['default_server_name']
    port = args.port or settings['default_server_port']
    server_settings = json.loads(args.settings)
    server_settings = merge(settings, server_settings)

    try:
        logger.info("Starting server '%s' on port %i", name, port)
        application = ServerApplication(endpoints=args.endpoints,
                                        **server_settings)
        application.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except:
        logger.exception("Failed to start server '%s' on port %i", name, port)
        sys.exit(errno.EINTR)
