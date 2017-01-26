# -*- coding: utf-8 -*-

import pytest

from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase

from api import __api__, __version__
from api.settings import settings
from api.server import Application as ServerApplication


@pytest.mark.integration
class TestServerWelcomeIntegration(AsyncHTTPTestCase):

    def get_new_ioloop(self):
        return IOLoop.instance()

    def get_app(self):
        return ServerApplication(**settings)

    def test_welcome_get(self):
        url = "/".format(settings["api_version"])
        expected = {
            "welcome": "API: v{} (build {}).".format(
                __api__, __version__)
        }

        response = self.fetch(
            url,
            method="GET",
            headers={"Content-Type": "application/json"})
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), expected)

    def test_welcome_post(self):
        url = "/".format(settings["api_version"])

        response = self.fetch(
            url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body='')
        self.assertEqual(response.code, 405)
