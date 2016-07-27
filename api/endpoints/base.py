# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from abc import ABCMeta, abstractproperty

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

    def __init__(self, cls, handlers, **settings):
        self.redis = redis.StrictRedis.from_url(settings['redis']["host"])
        tornado.web.Application.__init__(self, handlers, **settings)
        setattr(self, cls.name, cls.from_settings(settings))


class EndpointMixin(object):
    """Mixin for executor selection."""

    def executor(self, endpoint, method):
        endpoint = getattr(self.application, endpoint)
        return getattr(endpoint, method)


class AbstractEndpointHandler(RequestHandler, EndpointMixin):
    """Abstract base class for endpoint's handlers."""

    __metaclass__ = ABCMeta

    @abstractproperty
    def endpoint(self):
        pass

    @authenticated()
    @authorized()
    @tornado.gen.coroutine
    def prepare(self, *args, **kwargs):
        return super(AbstractEndpointHandler, self).prepare(*args, **kwargs)

    @rate_limited()
    def execute(self, method, *args, **kwargs):
        executor = self.executor(self.endpoint, method)
        return executor(*args, **kwargs)
