# -*- coding: utf-8 -*-

import tornado.gen

from ..base import BaseEndpoint

from .executors import DocumentEndpointExecutor
from .handlers import (
    DocumentHandler,
    DocumentCreateHandler
)


class Endpoint(BaseEndpoint):
    """Base class for /document endpoint namespace."""

    version = '1.0.0'

    @property
    def handlers(self):
        return [
            (r'/', DocumentCreateHandler),
            (r'/(?P<document_id>[^/]+)', DocumentHandler),
        ]

    @tornado.gen.coroutine
    def get_document(self, request_handler, document_id):
        executor = DocumentEndpointExecutor(
            request_handler._user_id,
            test=getattr(request_handler, "__is_test", None))
        result = executor.get(document_id)
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def create_document(self, request_handler, params):
        executor = DocumentEndpointExecutor(
            request_handler._user_id,
            test=getattr(request_handler, "__is_test", None))
        result = executor.create(params)
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def update_document(self, request_handler, document_id, params):
        executor = DocumentEndpointExecutor(
            request_handler._user_id,
            test=getattr(request_handler, "__is_test", None))
        result = executor.update(document_id, params)
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def delete_document(self, request_handler, document_id):
        executor = DocumentEndpointExecutor(
            request_handler._user_id,
            test=getattr(request_handler, "__is_test", None))
        result = executor.delete(document_id)
        raise tornado.gen.Return(result)
