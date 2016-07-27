# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import redis
import tornado.web

from ..exceptions import APIServerError

from .. import __version__
from ..handlers import RequestHandler, DeprecatedHandler
from ..utils.ops import resolve_name, build_versioned_handlers


class Application(tornado.web.Application):
    """Default server application."""

    def __init__(self, **settings):
        self._settings = settings
        self._endpoints = self._settings['registered_endpoints']
        self.redis = redis.StrictRedis.from_url(settings['redis']["host"])

        global_handlers = [
            (r'/_health', HealthHandler, dict(settings=settings)),
            (r'/_version', VersionHandler, dict(settings=settings)),
        ]

        handlers = [
            (r'/', WelcomeHandler, dict(version=settings["api_version"])),
        ]
        for name in self._endpoints:
            module = resolve_name('api.endpoints.' + name)
            handlers += getattr(module, 'ENDPOINT_HANDLERS')

        handlers = build_versioned_handlers(
            handlers,
            settings["api_version"],
            settings["deprecated_api_versions"],
            DeprecatedHandler)
        handlers += global_handlers

        tornado.web.Application.__init__(self, handlers, **settings)

        for name in self._endpoints:
            module = resolve_name('api.endpoints.' + name)
            endpoint = getattr(module, 'Endpoint').from_settings(settings)
            setattr(self, name, endpoint)


class HealthHandler(RequestHandler):
    """Check system's health status."""

    def initialize(self, settings):
        self._settings = settings

    @tornado.gen.coroutine
    def get(self):
        # TODO: implement a simple health check here.
        # Important! It shouldn't be too expensive, because this
        # endpoint suppose to be called by load balancers quite often.

        ok = True
        if not ok:
            raise APIServerError("Service is in the RED state")

        self.send_json({"ok": "true"})
        self.finish()


class VersionHandler(RequestHandler):
    """Provide current running version."""

    def initialize(self, settings):
        self._settings = settings

    def get(self):
        self.send_json({
            "version": self._settings["api_version"],
            "build": __version__
        })
        self.finish()


class WelcomeHandler(RequestHandler):
    """Welcome noop handler."""

    def initialize(self, version):
        self.version = version

    def get(self):
        self.send_json({
            "welcome": "API: version {} (build {}).".format(
                self.version, __version__)
        })
        self.finish()
