# -*- coding: utf-8 -*-

import redis
from tornado.concurrent import futures
import tornado.web

from .. import __api__, __version__
from ..exceptions import APIServerError
from ..handlers import RequestHandler, DeprecatedHandler
from ..utils.ops import resolve_name, build_versioned_handlers


def _get_endpoints(endpoints, settings):
    registered = set(settings["registered_endpoints"])
    if endpoints is None:
        enabled = registered
    else:
        enabled = set(endpoints)

    unsupported = enabled - registered
    if unsupported:
        raise ValueError(
            "Unsupported endpoints: {}".format(", ".join(unsupported)))

    return enabled


class Application(tornado.web.Application):
    """Default server application."""

    def __init__(self, endpoints=None, **settings):
        self._settings = settings
        self._endpoints = _get_endpoints(endpoints, settings)

        self._executor = futures.ThreadPoolExecutor(
            settings["concurrency"].get("threads", 1))
        self._redis = redis.StrictRedis.from_url(
            settings["redis"]["url"])

        handlers = [
            (r"/", WelcomeHandler),
            (r"/_health", HealthHandler, dict(settings=settings)),
        ]

        endpoint_versions = {}
        for name in self._endpoints:
            endpoint_module = resolve_name("api.endpoints." + name)
            endpoint_cls = getattr(endpoint_module, "Endpoint")
            endpoint = endpoint_cls(name, settings)
            endpoint_versions[endpoint.name] = endpoint.version

            handlers.extend(
                build_versioned_handlers(
                    endpoint,
                    settings["api_version"],
                    settings["deprecated_api_versions"],
                    DeprecatedHandler)
            )

        handlers += [
            (r"/_version", VersionHandler, dict(endpoints=endpoint_versions)),
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

    def initialize(self, endpoints):
        self._endpoints = endpoints

    def get(self):
        response = {
            "version": "v{}".format(__api__),
            "build": __version__,
            "endpoints": self._endpoints
        }

        self.send_json(response)
        self.finish()


class WelcomeHandler(RequestHandler):
    """Welcome noop handler."""

    def get(self):
        self.send_json({
            "welcome": "API: v{} (build {}).".format(
                __api__, __version__)
        })
        self.finish()
