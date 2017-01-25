# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import redis
import tornado.web

from tornado.concurrent import futures

from ..handlers import DeprecatedHandler, RequestHandler
from ..utils.access import authenticated
from ..utils.ops import build_versioned_handlers


class BaseEndpoint(object):
    """Base class for Endpoints."""

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)


class BaseEndpointApplication(tornado.web.Application):
    """Base class for Endpoint Application."""

    def __init__(self, endpoint_cls, endpoint_handlers, **settings):
        # TODO: initalize clients for DB, ES, etc. here
        # for available in the case then endpoints executed
        # without server (standalone)
        # NOTE: for server case, see api.server.__init__

        self._executor = futures.ThreadPoolExecutor(
            settings["concurrency"].get("threads", 1))
        self._redis = redis.StrictRedis.from_url(
            settings["redis"]["url"])

        endpoint = endpoint_cls.from_settings(settings)
        handlers = build_versioned_handlers(
            endpoint,
            endpoint_handlers,
            settings["api_version"],
            settings["deprecated_api_versions"],
            DeprecatedHandler)

        tornado.web.Application.__init__(self, handlers, **settings)


class BaseEndpointHandler(RequestHandler):
    """Base class for endpoint"s handlers."""

    def initialize(self, **kwargs):
        assert "endpoint" in kwargs, "Missing endpoint"
        self.endpoint = kwargs["endpoint"]
        self.add_header("X-Endpoint-Name", self.endpoint.name)
        self.add_header("X-Endpoint-Version", self.endpoint.version)

    @authenticated()
    @tornado.gen.coroutine
    def prepare(self, *args, **kwargs):
        return super(BaseEndpointHandler, self).prepare(*args, **kwargs)
