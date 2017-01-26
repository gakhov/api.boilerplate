# -*- coding: utf-8 -*-

import pytest

from tornado.escape import json_decode
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

        json_response = json_decode(response.body)

        self.assertIn("endpoints", json_response)
        self.assertIn("document", json_response['endpoints'])

        for key, value in expected.items():
            self.assertIn(key, json_response)
            self.assertEqual(json_response[key], value)

    def test_version_post(self):
        url = "/_version"

        response = self.fetch(
            url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body='')
        self.assertEqual(response.code, 405)
