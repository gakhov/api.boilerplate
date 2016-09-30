# -*- coding: utf-8 -*-

import tornado.gen

from ...utils.access import authorized
from ...utils.schema import (
    input_validate_get,
    input_validate_post,
    output_validate
)
from ..base import BaseEndpointHandler
from .schema import (
    DELETE_OUTPUT_SCHEMA,
    GET_INPUT_SCHEMA,
    GET_OUTPUT_SCHEMA,
    POST_INPUT_SCHEMA,
    POST_OUTPUT_SCHEMA,
    PUT_INPUT_SCHEMA,
    PUT_OUTPUT_SCHEMA,
)

__all__ = [
    "DocumentHandler",
    "DocumentCreateHandler"
]


class DocumentHandler(BaseEndpointHandler):
    """Main Handler for /document endpoint."""

    @authorized(["get-document", "update-document"])
    @input_validate_get(GET_INPUT_SCHEMA)
    @output_validate(GET_OUTPUT_SCHEMA)
    @tornado.gen.coroutine
    def get(self, document_id):
        result = yield self.endpoint.get_document(self, document_id)
        raise tornado.gen.Return(result)

    @authorized(["update-document"])
    @input_validate_post(PUT_INPUT_SCHEMA)
    @output_validate(PUT_OUTPUT_SCHEMA)
    @tornado.gen.coroutine
    def put(self, document_id):
        result = yield self.endpoint.update_document(
            self,
            document_id,
            params=self.json_body)
        raise tornado.gen.Return(result)

    @authorized(["delete-document"])
    @output_validate(DELETE_OUTPUT_SCHEMA)
    @tornado.gen.coroutine
    def delete(self, document_id):
        result = yield self.endpoint.delete_document(self, document_id)
        raise tornado.gen.Return(result)


class DocumentCreateHandler(BaseEndpointHandler):
    """Create Handler for /document endpoint."""

    @authorized(["create-document"])
    @input_validate_post(POST_INPUT_SCHEMA)
    @output_validate(POST_OUTPUT_SCHEMA)
    @tornado.gen.coroutine
    def post(self):
        result = yield self.endpoint.create_document(
            self, params=self.json_body)
        self.set_status(201)
        raise tornado.gen.Return(result)
