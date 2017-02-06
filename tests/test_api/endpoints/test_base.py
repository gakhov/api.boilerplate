# -*- coding: utf-8 -*-

from tornado.gen import coroutine
from tornado.testing import AsyncTestCase
from tornado.testing import gen_test

from api.endpoints.base import BaseEndpoint
from api.exceptions import HealthError
from api.exceptions import HealthWarning


def _make_check(status, reason=None, **details):

    @coroutine
    def check():
        if status in ("warning", "error"):
            if status == "warning":
                exc_class = HealthWarning
            else:
                exc_class = HealthError

            raise exc_class(reason, details=details)

    return check


class TestBaseEndpoint(AsyncTestCase):

    def test_name(self):
        self.assertEqual(BaseEndpoint("foobar", {}).name, "foobar")

    def test_default_handlers(self):
        self.assertEqual(BaseEndpoint("foobar", {}).handlers, [])

    def test_add_health_checks(self):
        endpoint = BaseEndpoint("foobar", {})
        self.assertEqual(endpoint.health_checks, {})
        check1 = _make_check("ok")
        check2 = _make_check("ok")
        check3 = _make_check("ok")
        check4 = _make_check("ok")
        endpoint.add_health_check("a", check1)
        endpoint.add_health_check("b", check2)
        endpoint.add_health_check("c", check3)
        with self.assertRaises(ValueError):
            endpoint.add_health_check("", check4)

        self.assertEqual(endpoint.health_checks, {
            "a": check1,
            "b": check2,
            "c": check3
        })

    @gen_test
    def test_health_no_checks(self):
        endpoint = BaseEndpoint("foobar", {})
        result = yield endpoint.check_health()
        expected = {
            "status": "ok",
            "checks": []
        }
        self.assertEqual(result, expected)

    @gen_test
    def test_health_ok(self):
        check1 = _make_check("ok")
        check2 = _make_check("ok")
        check3 = _make_check("ok")
        endpoint = BaseEndpoint("foobar", {})
        endpoint.add_health_check("a", check1)
        endpoint.add_health_check("b", check2)
        endpoint.add_health_check("c", check3)
        result = yield endpoint.check_health()
        expected = {
            "status": "ok",
            "checks": [
                {
                    "name": "a",
                    "status": "ok"
                },
                {
                    "name": "b",
                    "status": "ok"
                },
                {
                    "name": "c",
                    "status": "ok"
                }
            ]
        }
        self.assertEqual(result, expected)

    @gen_test
    def test_health_warning(self):
        check1 = _make_check("ok")
        check2 = _make_check("warning", reason="Something went wrong ...")
        check3 = _make_check("ok")
        endpoint = BaseEndpoint("foobar", {})
        endpoint.add_health_check("a", check1)
        endpoint.add_health_check("b", check2)
        endpoint.add_health_check("c", check3)
        result = yield endpoint.check_health()
        expected = {
            "status": "warning",
            "checks": [
                {
                    "name": "a",
                    "status": "ok"
                },
                {
                    "name": "b",
                    "status": "warning",
                    "reason": "Something went wrong ..."
                },
                {
                    "name": "c",
                    "status": "ok"
                }
            ]
        }
        self.assertEqual(result, expected)

    @gen_test
    def test_health_warning_details(self):
        check1 = _make_check("ok")
        check2 = _make_check("warning", reason="Something went wrong ...",
                             host="localhost", port=4567)
        check3 = _make_check("ok")
        endpoint = BaseEndpoint("foobar", {})
        endpoint.add_health_check("a", check1)
        endpoint.add_health_check("b", check2)
        endpoint.add_health_check("c", check3)
        result = yield endpoint.check_health()
        expected = {
            "status": "warning",
            "checks": [
                {
                    "name": "a",
                    "status": "ok"
                },
                {
                    "name": "b",
                    "status": "warning",
                    "reason": "Something went wrong ...",
                    "host": "localhost",
                    "port": 4567
                },
                {
                    "name": "c",
                    "status": "ok"
                }
            ]
        }
        self.assertEqual(result, expected)

    @gen_test
    def test_health_error(self):
        check1 = _make_check("ok")
        check2 = _make_check("warning", reason="Something went wrong ...")
        check3 = _make_check("error", reason="Something went terribly wrong!")
        endpoint = BaseEndpoint("foobar", {})
        endpoint.add_health_check("a", check1)
        endpoint.add_health_check("b", check2)
        endpoint.add_health_check("c", check3)
        result = yield endpoint.check_health()
        expected = {
            "status": "error",
            "checks": [
                {
                    "name": "a",
                    "status": "ok"
                },
                {
                    "name": "b",
                    "status": "warning",
                    "reason": "Something went wrong ..."
                },
                {
                    "name": "c",
                    "status": "error",
                    "reason": "Something went terribly wrong!"
                }
            ]
        }
        self.assertEqual(result, expected)

    @gen_test
    def test_health_error_details(self):
        check1 = _make_check("ok")
        check2 = _make_check("warning", reason="Something went wrong ...")
        check3 = _make_check("error", reason="Something went terribly wrong!",
                             timeout=30)
        endpoint = BaseEndpoint("foobar", {})
        endpoint.add_health_check("a", check1)
        endpoint.add_health_check("b", check2)
        endpoint.add_health_check("c", check3)
        result = yield endpoint.check_health()
        expected = {
            "status": "error",
            "checks": [
                {
                    "name": "a",
                    "status": "ok"
                },
                {
                    "name": "b",
                    "status": "warning",
                    "reason": "Something went wrong ..."
                },
                {
                    "name": "c",
                    "status": "error",
                    "reason": "Something went terribly wrong!",
                    "timeout": 30
                }
            ]
        }
        self.assertEqual(result, expected)
