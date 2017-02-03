# -*- coding: utf-8 -*-

import tornado.web

from ..handlers import RequestHandler
from ..utils.access import authenticated


class BaseEndpoint(object):
    """Base class for Endpoints."""

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)


class BaseEndpointHandler(RequestHandler):
    """Base class for endpoint"s handlers."""

    def initialize(self, **kwargs):
        assert "endpoint" in kwargs, "Missing endpoint"
        self.endpoint = kwargs["endpoint"]
        self.set_header("X-Endpoint-Name", self.endpoint.name)
        self.set_header("X-Endpoint-Version", self.endpoint.version)

    @authenticated()
    @tornado.gen.coroutine
    def prepare(self, *args, **kwargs):
        return super(BaseEndpointHandler, self).prepare(*args, **kwargs)
