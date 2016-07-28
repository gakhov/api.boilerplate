# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tornado.gen
from datetime import datetime

from ...handlers import DeprecatedHandler
from ...utils.ops import build_versioned_handlers
from ..base import (
    BaseEndpoint,
    BaseEndpointApplication
)

from .handlers import (
    DemoHandler,
    DemoCreateHandler
)


ENDPOINT_HANDLERS = [
    (r'/demo', DemoCreateHandler),
    (r'/demo/(?P<document_id>[^/]+)', DemoHandler),
]


class Endpoint(BaseEndpoint):
    """Base class for /demo endpoint namespace."""

    name = 'demo'

    def __init__(self, settings):
        self._settings = settings

    @tornado.gen.coroutine
    def get_document(self, document_id):
        result = {
            "id": "lu165gsQI9cxly2J3MM",
            "text": (
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                "sed do eiusmod tempor incididunt ut labore et dolore magna"
                " aliqua."
            ),
            "created_at": "2007-07-07T13:30:00Z"
        }
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def create_document(self, params):
        result = {
            "id": "lu165gsQI9cxly2J3MM",
            "created_at": "2016-07-07T13:30:00Z"
        }
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def update_document(self, document_id, params):
        result = {
            "id": document_id,
            "updated_at": "2016-07-27T13:30:00Z"
        }
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def delete_document(self, document_id):
        result = {
            "id": document_id,
            "deleted_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        raise tornado.gen.Return(result)


class Application(BaseEndpointApplication):
    """Main application for /demo endpoint namespace."""

    def __init__(self, **settings):
        endpoint = Endpoint.from_settings(settings)
        handlers = build_versioned_handlers(
            endpoint,
            ENDPOINT_HANDLERS,
            settings["api_version"],
            settings["deprecated_api_versions"],
            DeprecatedHandler)

        super(Application, self).__init__(handlers, **settings)
