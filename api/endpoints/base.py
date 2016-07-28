# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from abc import ABCMeta

import redis
import tornado.web

from ..handlers import RequestHandler
from ..utils.access import authorized, authenticated, rate_limited


class AbstractEndpoint(object):
    """Abstract base class for Endpoints."""

    __metaclass__ = ABCMeta

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)


class EndpointApplication(tornado.web.Application):
    """Base class for Endpoint Application."""

    def __init__(self, handlers, **settings):
        self.redis = redis.StrictRedis.from_url(settings["redis"]["host"])
        tornado.web.Application.__init__(self, handlers, **settings)


class AbstractEndpointHandler(RequestHandler):
    """Abstract base class for endpoint"s handlers."""

    __metaclass__ = ABCMeta

    def initialize(self, **kwargs):
        assert "endpoint" in kwargs, "Missing endpoint"
        self.endpoint = kwargs["endpoint"]

    @authenticated()
    @authorized()
    @rate_limited()
    @tornado.gen.coroutine
    def prepare(self, *args, **kwargs):
        return super(AbstractEndpointHandler, self).prepare(*args, **kwargs)
