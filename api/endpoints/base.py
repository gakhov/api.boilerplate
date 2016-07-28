# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import redis
import tornado.web

from ..handlers import RequestHandler
from ..utils.access import authorized, authenticated, rate_limited


class BaseEndpoint(object):
    """Base class for Endpoints."""

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)


class BaseEndpointApplication(tornado.web.Application):
    """Base class for Endpoint Application."""

    def __init__(self, handlers, **settings):
        self.redis = redis.StrictRedis.from_url(settings["redis"]["host"])
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseEndpointHandler(RequestHandler):
    """Base class for endpoint"s handlers."""

    def initialize(self, **kwargs):
        assert "endpoint" in kwargs, "Missing endpoint"
        self.endpoint = kwargs["endpoint"]

    @authenticated()
    @authorized()
    @rate_limited()
    @tornado.gen.coroutine
    def prepare(self, *args, **kwargs):
        return super(BaseEndpointHandler, self).prepare(*args, **kwargs)
