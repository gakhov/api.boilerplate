# -*- coding: utf-8 -*-

import tornado.gen

from ...utils.schema import (
    input_validate_post,
    output_validate
)
from ..base import AbstractEndpointHandler
from .schema import (
    DELETE_OUTPUT_SCHEMA,
    GET_OUTPUT_SCHEMA,
    POST_INPUT_SCHEMA,
    POST_OUTPUT_SCHEMA,
    PUT_INPUT_SCHEMA,
    PUT_OUTPUT_SCHEMA,
)

__all__ = [
    "DemoHandler",
    "DemoCreateHandler"
]


class DemoHandler(AbstractEndpointHandler):
    """Main Handler for /demo endpoint
    """

    @output_validate(GET_OUTPUT_SCHEMA)
    @tornado.gen.coroutine
    def get(self, document_id):
        result = yield self.endpoint.get_document(document_id)
        raise tornado.gen.Return(result)

    @input_validate_post(PUT_INPUT_SCHEMA)
    @output_validate(PUT_OUTPUT_SCHEMA)
    @tornado.gen.coroutine
    def put(self, document_id):
        result = yield self.endpoint.update_document(
            document_id, params=self.json_body)
        raise tornado.gen.Return(result)

    @output_validate(DELETE_OUTPUT_SCHEMA)
    @tornado.gen.coroutine
    def delete(self, document_id):
        result = yield self.endpoint.delete_document(document_id)
        raise tornado.gen.Return(result)


class DemoCreateHandler(AbstractEndpointHandler):
    """Create Handler for /demo endpoint."""

    @input_validate_post(POST_INPUT_SCHEMA)
    @output_validate(POST_OUTPUT_SCHEMA)
    @tornado.gen.coroutine
    def post(self):
        result = yield self.endpoint.create_document(params=self.json_body)
        self.set_status(201)
        raise tornado.gen.Return(result)
