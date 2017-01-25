# -*- coding: utf-8 -*-

import logging
import tornado.web

from tornado.escape import json_encode

from . import __version__
from .exceptions import APIError


__all__ = [
    "DeprecatedHandler",
    "ErrorHandler",
    "RequestHandler",
]

logger = logging.getLogger('api.handlers')


class RequestHandler(tornado.web.RequestHandler):
    """Extention of the tornado"s RequestHandler with helpers."""

    def set_default_headers(self):
        self.set_header("X-API-Version", __version__)
        self.set_header("Server", "API")
        self.set_header("Content-Type", "application/json")

    def write_error(self, status_code, **kwargs):

        def get_exc_message(exception):
            if hasattr(exception, "details") and exception.details:
                return exception.details
            if hasattr(exception, "log_message") and exception.log_message:
                return exception.log_message
            if hasattr(exception, "message") and exception.message:
                return exception.message
            return str(exception)

        self.clear()
        self.set_status(status_code)

        exception = kwargs["exc_info"][1]

        if isinstance(exception, APIError):
            error = {
                "message": self._reason,
                "code": status_code,
                "details": get_exc_message(exception)
            }
        elif isinstance(exception, tornado.web.HTTPError):
            error = {
                "message": self._reason,
                "details": get_exc_message(exception),
                "code": status_code
            }
        else:
            error = {
                "message": self._reason,
                "code": status_code
            }

        self.send_json(error)

    def send_json(self, value):
        self.write(json_encode(value))


class DeprecatedHandler(RequestHandler):
    """Special type of handler to raise HTTP Error 410 Gone."""

    def get(self, *args, **kwargs):
        self.clear()
        self.set_status(410)
        self.send_json({"error": "Deprecated"})
        self.finish()

    def post(self, *args, **kwargs):
        self.clear()
        self.set_status(410)
        self.send_json({"error": "Deprecated"})
        self.finish()

    def put(self, *args, **kwargs):
        self.clear()
        self.set_status(410)
        self.send_json({"error": "Deprecated"})
        self.finish()

    def delete(self, *args, **kwargs):
        self.clear()
        self.set_status(410)
        self.send_json({"error": "Deprecated"})
        self.finish()


class ErrorHandler(tornado.web.ErrorHandler, RequestHandler):
    """Default handler in case of 404 error."""

    pass
