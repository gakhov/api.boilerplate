# -*- encoding: utf-8 -*-

from tornado.web import HTTPError


class APIError(HTTPError):
    """General API Error."""

    def __init__(self, status_code, message=None, details=None):
        super(APIError, self).__init__(status_code, message)
        self.details = details


class APIClientError(APIError):
    """Client API Error."""

    pass


class APIServerError(APIError):
    """Server API Error."""

    pass
