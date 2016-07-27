# -*- encoding: utf-8 -*-

import unittest
import mock

from api.exceptions import APIClientError
from api.utils.access import (
    authorized,
    authenticated,
    rate_limited
)


class AccessTest(object):
    """Test class with different variants of using access decorators."""

    @authenticated()
    def f_authenticated(self):
        pass

    @authenticated()
    @authorized()
    def f_authenticated_authorized(self):
        pass

    @authorized()
    def f_authorized(self):
        pass

    @authenticated()
    @authorized()
    @rate_limited()
    def f_authenticated_authorized_limited(self):
        pass

    @authenticated()
    @rate_limited()
    def f_authenticated_limited(self):
        pass


class TestUtilsAccess(unittest.TestCase):

    def test_authenticated(self):
        request = mock.PropertyMock()
        request.query = "api_key=test.1461680306.HeEEI73nvembtLHk2eM"

        access = AccessTest()
        access.request = request

        access.f_authenticated()

    def test_authenticated_nokey(self):
        access = AccessTest()

        request = mock.PropertyMock()
        request.query = "missing=test"
        access.request = request

        with self.assertRaises(APIClientError):
            access.f_authenticated()

    def test_authenticated_invalidkey(self):
        access = AccessTest()

        request = mock.PropertyMock()
        request.query = "api_key=invalid"
        access.request = request

        with self.assertRaises(APIClientError):
            access.f_authenticated()

    def test_authorized(self):
        access = AccessTest()

        request = mock.PropertyMock()
        request.uri = "/v1/tester"
        request.query = "api_key=test.1461680306.HeEEI73nvembtLHk2eM"

        access.request = request
        access.endpoint = "test"
        access.application = mock.MagicMock(return_value=None)
        access.set_header = mock.MagicMock(return_value=None)

        access.f_authenticated_authorized()

        self.assertTrue(hasattr(access, "rate_limit"))
        self.assertEqual(access.rate_limit, 1000)

        self.assertTrue(hasattr(access, "ttl"))
        self.assertEqual(access.ttl, 86400)

    def test_authorized_noaccess_endpoint(self):
        access = AccessTest()

        request = mock.PropertyMock()
        request.uri = "/v1/noaccess"
        request.query = "api_key=test.1461680306.HeEEI73nvembtLHk2eM"

        access.request = request
        access.endpoint = "noaccess"
        access.application = mock.MagicMock(return_value=None)
        access.set_header = mock.MagicMock(return_value=None)

        with self.assertRaises(APIClientError):
            access.f_authenticated_authorized()

    def test_authorized_not_authenticated(self):
        access = AccessTest()
        access.request = mock.PropertyMock()

        with self.assertRaises(AssertionError):
            access.f_authorized()

    def test_limited(self):
        access = AccessTest()

        request = mock.PropertyMock()
        request.uri = "/v1/test"
        request.query = "api_key=test.1461680306.HeEEI73nvembtLHk2eM"

        redis = mock.MagicMock()
        redis.get = mock.MagicMock(return_value=None)
        redis.setex = mock.MagicMock(return_value=True)

        access.request = request
        access.endpoint = "test"
        access.application = mock.MagicMock(return_value=None)
        access.application.redis = redis
        access.set_header = mock.MagicMock(return_value=None)

        access.f_authenticated_authorized_limited()

        access.set_header.assert_any_call("X-RateLimit-Limit", 1000)
        access.set_header.assert_any_call("X-RateLimit-Remaining", 999)

    def test_limited_exceeded(self):
        access = AccessTest()

        request = mock.PropertyMock()
        request.uri = "/v1/test"
        request.query = "api_key=test.1461680306.HeEEI73nvembtLHk2eM"

        redis = mock.MagicMock()
        redis.get = mock.MagicMock(return_value=True)
        redis.decr = mock.MagicMock(return_value=-1)
        redis.ttl = mock.MagicMock(return_value=100)

        access.request = request
        access.endpoint = "test"
        access.application = mock.MagicMock()
        access.application.redis = redis
        access.set_header = mock.MagicMock(return_value=None)

        with self.assertRaises(APIClientError):
            access.f_authenticated_authorized_limited()

    def test_limited_not_authorized(self):
        access = AccessTest()

        request = mock.PropertyMock()
        request.uri = "/v1/test"
        request.query = "api_key=test.1461680306.HeEEI73nvembtLHk2eM"
        access.request = request
        access.endpoint = "test"

        with self.assertRaises(AssertionError):
            access.f_authenticated_limited()
