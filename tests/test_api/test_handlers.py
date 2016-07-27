# -*- coding: utf-8 -*-

import mock
import unittest

from tornado.web import HTTPError

from api.version import __version__
from api.exceptions import APIError
from api.handlers import RequestHandler, DeprecatedHandler


class TestRequestHandler(unittest.TestCase):

    def setUp(self):
        app = mock.MagicMock()
        app.ui_methods.return_value = {}
        request = mock.MagicMock()
        request.connection.side_effect = None
        self._rh = RequestHandler(app, request)

        mock_write = mock.MagicMock(**{"return_value": True})
        self._rh.write = mock_write

        mock_set_header = mock.MagicMock(**{"return_value": True})
        self._rh.set_header = mock_set_header

        mock_set_status = mock.MagicMock(**{"return_value": True})
        self._rh.set_status = mock_set_status

        mock_clear = mock.MagicMock(**{"return_value": True})
        self._rh.clear = mock_clear

        mock_finish = mock.MagicMock(**{"return_value": True})
        self._rh.finish = mock_finish

    def test_set_default_headers(self):
        self._rh.set_default_headers()
        self._rh.set_header.assert_any_call(
            "X-API-Version", __version__)
        self._rh.set_header.assert_any_call(
            "Server", "API")
        self._rh.set_header.assert_any_call(
            "Content-Type", "application/json")

    def test_send_json(self):
        value = {
            "test": ["test"]
        }

        self._rh.send_json(value)
        self._rh.write.assert_called_once_with('{"test": ["test"]}')

    def test_write_error(self):
        kwargs = {
            "exc_info": (None, Exception(), None)
        }

        self._rh.write_error(301, **kwargs)
        self._rh.set_status.assert_called_once_with(301)
        self._rh.write.assert_called_once_with(
            '{"message": "OK", "code": 301}')

    def test_write_error_no_exception(self):
        with self.assertRaises(KeyError):
            self._rh.write_error(301)

    def test_write_error_api_exception(self):
        kwargs = {
            "exc_info": (None, APIError(400, "API ERROR", "ERROR"), None)
        }

        self._rh.write_error(400, **kwargs)
        self._rh.set_status.assert_called_once_with(400)
        self._rh.write.assert_called_once_with(
            '{"message": "OK", "code": 400, "details": "ERROR"}')

    def test_write_error_http_error(self):
        kwargs = {
            "exc_info": (None, HTTPError(400, "HTTP ERROR"), None)
        }

        self._rh.write_error(400, **kwargs)
        self._rh.set_status.assert_called_once_with(400)
        self._rh.write.assert_called_once_with(
            '{"message": "OK", "code": 400, "details": "HTTP ERROR"}')


class TestDeprecatedHandler(unittest.TestCase):

    def setUp(self):
        app = mock.MagicMock()
        app.ui_methods.return_value = {}
        request = mock.MagicMock()
        request.connection.side_effect = None
        self._rh = DeprecatedHandler(app, request)

        mock_write = mock.MagicMock(**{"return_value": True})
        self._rh.write = mock_write

        mock_set_header = mock.MagicMock(**{"return_value": True})
        self._rh.set_header = mock_set_header

        mock_set_status = mock.MagicMock(**{"return_value": True})
        self._rh.set_status = mock_set_status

        mock_clear = mock.MagicMock(**{"return_value": True})
        self._rh.clear = mock_clear

        mock_finish = mock.MagicMock(**{"return_value": True})
        self._rh.finish = mock_finish

    def test_get(self):
        self._rh.get()
        self._rh.clear.assert_called_once_with()
        self._rh.set_status.assert_called_once_with(410)
        self._rh.write.assert_called_once_with('{"error": "Deprecated"}')
        self._rh.finish.assert_called_once_with()

    def test_post(self):
        self._rh.post()
        self._rh.clear.assert_called_once_with()
        self._rh.set_status.assert_called_once_with(410)
        self._rh.write.assert_called_once_with('{"error": "Deprecated"}')
        self._rh.finish.assert_called_once_with()
