# -*- coding: utf-8 -*-

import json
import pytest

from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase

from api.settings import settings
from api.server import Application as ServerApplication


@pytest.mark.integration
class TestServerHealthIntegration(AsyncHTTPTestCase):

    def get_new_ioloop(self):
        return IOLoop.instance()

    def get_app(self):
        return ServerApplication(**settings)

    def test_health_get(self):
        url = "/_health"
        expected = {
            "ok": "true"
        }

        response = self.fetch(
            url,
            method="GET",
            headers={"Content-Type": "application/json"})
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), expected)

    def test_health_post(self):
        url = "/_health"

        response = self.fetch(
            url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body='')
        self.assertEqual(response.code, 405)
