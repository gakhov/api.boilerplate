# -*- coding: utf-8 -*-

import redis
import tornado.web

from tornado.concurrent import futures


from .. import __version__
from ..exceptions import APIServerError
from ..handlers import RequestHandler, DeprecatedHandler
from ..utils.ops import resolve_name, build_versioned_handlers


class Application(tornado.web.Application):
    """Default server application."""

    def __init__(self, **settings):
        self._settings = settings
        self._endpoints = self._settings["registered_endpoints"]

        self._executor = futures.ThreadPoolExecutor(
            settings["concurrency"].get("threads", 1))
        self._redis = redis.StrictRedis.from_url(
            settings["redis"]["url"])

        handlers = [
            (r"/", WelcomeHandler, dict(version=settings["api_version"])),
            (r"/_health", HealthHandler, dict(settings=settings)),
        ]

        endpoint_versions = {}
        for name in self._endpoints:
            module = resolve_name("api.endpoints." + name)
            endpoint = getattr(module, "Endpoint").from_settings(settings)
            endpoint_versions[endpoint.name] = endpoint.version

            endpoint_handlers = getattr(module, "ENDPOINT_HANDLERS")
            handlers.extend(
                build_versioned_handlers(
                    endpoint,
                    endpoint_handlers,
                    settings["api_version"],
                    settings["deprecated_api_versions"],
                    DeprecatedHandler)
            )

        handlers += [
            (r"/_version", VersionHandler, dict(
                settings=settings, endpoint_versions=endpoint_versions)),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)


class HealthHandler(RequestHandler):
    """Check system"s health status."""

    def initialize(self, settings):
        self._settings = settings

    @tornado.gen.coroutine
    def get(self):
        # TODO: implement a simple health check here.
        # Important! It shouldn"t be too expensive, because this
        # endpoint suppose to be called by load balancers quite often.

        ok = True
        if not ok:
            raise APIServerError("Service is in the RED state")

        self.send_json({"ok": "true"})
        self.finish()


class VersionHandler(RequestHandler):
    """Provide current running version."""

    def initialize(self, settings, endpoint_versions):
        self._settings = settings
        self._endpoint_versions = endpoint_versions

    def get(self):
        response = {
            "version": self._settings["api_version"],
            "build": __version__,
            "endpoints": self._endpoint_versions
        }

        self.send_json(response)
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
