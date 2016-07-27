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

    @property
    def endpoint(self):
        return 'demo'

    @output_validate(GET_OUTPUT_SCHEMA)
    @tornado.gen.coroutine
    def get(self, document_id):

        future = self.execute(
            "get_document", document_id)

        def done(async_future):
            raise tornado.gen.Return(async_future.result())
        future.add_done_callback(done)

    @input_validate_post(PUT_INPUT_SCHEMA)
    @output_validate(PUT_OUTPUT_SCHEMA)
    @tornado.gen.coroutine
    def put(self, document_id):
        future = self.execute(
            "update_document", document_id, params=self.json_body)

        def done(async_future):
            raise tornado.gen.Return(async_future.result())
        future.add_done_callback(done)

    @output_validate(DELETE_OUTPUT_SCHEMA)
    @tornado.gen.coroutine
    def delete(self, document_id):
        future = self.execute(
            "delete_document", document_id)

        def done(async_future):
            raise tornado.gen.Return(async_future.result())
        future.add_done_callback(done)


class DemoCreateHandler(AbstractEndpointHandler):
    """Create Handler for /demo endpoint."""

    @property
    def endpoint(self):
        return 'demo'

    @input_validate_post(POST_INPUT_SCHEMA)
    @output_validate(POST_OUTPUT_SCHEMA)
    @tornado.gen.coroutine
    def post(self):
        future = self.execute(
            "create_document", params=self.json_body)

        def done(async_future):
            self.set_status(201)
            raise tornado.gen.Return(async_future.result())
        future.add_done_callback(done)
