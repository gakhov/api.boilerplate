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


class HealthError(Exception):

    def __init__(self, reason, details=None):
        super(HealthError, self).__init__(reason)
        self.details = details

    @property
    def status(self):
        return "error"

    @property
    def weight(self):
        return 2


class HealthWarning(Exception):

    def __init__(self, reason, details=None):
        super(HealthWarning, self).__init__(reason)
        self.details = details

    @property
    def status(self):
        return "warning"

    @property
    def weight(self):
        return 1
