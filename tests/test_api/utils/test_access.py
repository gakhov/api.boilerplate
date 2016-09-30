# -*- encoding: utf-8 -*-

import unittest

from api.exceptions import APIClientError
from api.utils.access import (
    _SUPERADMIN_SCOPE,
    _TEST_SCOPE,
    authorized
)


class AccessTest(object):
    """Test class with different variants of using access decorators."""

    def __init__(self, test=None):
        self._test = test

    def get_query_argument(self, name, default=None):
        return getattr(self, name, default)

    @authorized()
    def f_authorized(self):
        pass

    @authorized(["some-get"])
    def f_authenticated_authorized_scopes(self):
        pass


class TestUtilsAccess(unittest.TestCase):

    def test_authorized_not_authenticated(self):
        access = AccessTest()

        with self.assertRaises(AssertionError):
            access.f_authorized()

    def test_authenticated_authorized_test(self):
        access = AccessTest(test=True)

        access._access_token = "token-123"
        access._user_id = "user123"
        access._scopes = [_TEST_SCOPE, "some-get"]

        access.f_authenticated_authorized_scopes()
        self.assertTrue(hasattr(access, "__is_test"))
        self.assertTrue(getattr(access, "__is_test"))

    def test_authenticated_authorized_superadmin_no_required_scopes(self):
        access = AccessTest()

        access._access_token = "token-123"
        access._user_id = "user123"
        access._scopes = [_SUPERADMIN_SCOPE]

        access.f_authorized()
        self.assertTrue(hasattr(access, "__is_super"))
        self.assertTrue(getattr(access, "__is_super"))

    def test_authenticated_authorized_superadmin_with_required_scopes(self):
        access = AccessTest()

        access._access_token = "token-123"
        access._user_id = "user123"
        access._scopes = [_SUPERADMIN_SCOPE]

        access.f_authenticated_authorized_scopes()
        self.assertTrue(hasattr(access, "__is_super"))
        self.assertTrue(getattr(access, "__is_super"))

    def test_authenticated_authorized_noscopes_no_required_scopes(self):
        access = AccessTest()

        access._access_token = "token-123"
        access._user_id = "user123"
        access._scopes = []

        with self.assertRaises(APIClientError):
            access.f_authorized()

    def test_authenticated_authorized_noscopes_with_required_scopes(self):
        access = AccessTest()

        access._access_token = "token-123"
        access._user_id = "user123"
        access._scopes = []

        with self.assertRaises(APIClientError):
            access.f_authenticated_authorized_scopes()

    def test_authenticated_authorized_badscopes_no_required_scopes(self):
        access = AccessTest()

        access._access_token = "token-123"
        access._user_id = "user123"
        access._scopes = ["some-scope"]

        with self.assertRaises(APIClientError):
            access.f_authorized()

    def test_authenticated_authorized_badscopes_with_required_scopes(self):
        access = AccessTest()

        access._access_token = "token-123"
        access._user_id = "user123"
        access._scopes = ["some-scope"]

        with self.assertRaises(APIClientError):
            access.f_authenticated_authorized_scopes()

    def test_authenticated_authorized_validscopes_with_required_scopes(self):
        access = AccessTest()

        access._access_token = "token-123"
        access._user_id = "user123"
        access._scopes = ["some-get"]

        access.f_authenticated_authorized_scopes()
        self.assertFalse(hasattr(access, "__is_super"))
