# -*- coding: utf-8 -*-

import json
import pytest

from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase

from api import __version__
from api.settings import settings
from api.server import Application as ServerApplication


@pytest.mark.integration
class TestServerVersionIntegration(AsyncHTTPTestCase):

    def get_new_ioloop(self):
        return IOLoop.instance()

    def get_app(self):
        return ServerApplication(**settings)

    def test_version_get(self):
        url = "/_version"
        expected = {
            "version": settings["api_version"],
            "build": __version__
        }

        response = self.fetch(
            url,
            method="GET",
            headers={"Content-Type": "application/json"})
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), expected)

    def test_version_post(self):
        url = "/_version"

        response = self.fetch(
            url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body='')
        self.assertEqual(response.code, 405)
