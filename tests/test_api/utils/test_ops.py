# -*- encoding: utf-8 -*-
import unittest
from unittest.mock import MagicMock

from api.utils.ops import (
    build_versioned_handlers,
    resolve_name
)


class TestUtilsOps(unittest.TestCase):

    def test_build_versioned_handlers(self):
        endpoint = MagicMock()
        endpoint.name = "foobar"
        endpoint.handlers = [
            ("/test0", "TEST0"),
            ("/test1", "TEST1"),
        ]
        active_version = '2'
        deprecated_versions = ['1']
        deprecated_handler = "DEPRECATED"
        expected = [
            ("/v2/foobar/test0", "TEST0", {"endpoint": endpoint}),
            ("/v2/foobar/test1", "TEST1", {"endpoint": endpoint}),
            ("/v1/foobar/test0", "DEPRECATED"),
            ("/v1/foobar/test1", "DEPRECATED"),
        ]

        versioned = build_versioned_handlers(
            endpoint,
            active_version,
            deprecated_versions,
            deprecated_handler)
        self.assertEqual(versioned, expected)

    def test_build_versioned_handlers_long_handler(self):
        endpoint = MagicMock()
        endpoint.name = "foobar"
        endpoint.handlers = [
            ("/test0", "TEST0", {"ADDITIONAL": True}),
            ("/test1", "TEST1"),
        ]
        active_version = '2'
        deprecated_versions = ['1']
        deprecated_handler = "DEPRECATED"
        expected = [
            ("/v2/foobar/test0", "TEST0", {"ADDITIONAL": True,
                                           "endpoint": endpoint}),
            ("/v2/foobar/test1", "TEST1", {"endpoint": endpoint}),
            ("/v1/foobar/test0", "DEPRECATED"),
            ("/v1/foobar/test1", "DEPRECATED"),
        ]

        versioned = build_versioned_handlers(
            endpoint,
            active_version,
            deprecated_versions,
            deprecated_handler)
        self.assertEqual(versioned, expected)

    def test_build_versioned_handlers_no_deprecated(self):
        endpoint = MagicMock()
        endpoint.name = "foobar"
        endpoint.handlers = [
            ("/test0", "TEST0"),
            ("/test1", "TEST1"),
        ]
        active_version = '2'
        deprecated_versions = []
        deprecated_handler = "DEPRECATED"
        expected = [
            ("/v2/foobar/test0", "TEST0", {"endpoint": endpoint}),
            ("/v2/foobar/test1", "TEST1", {"endpoint": endpoint}),
        ]

        versioned = build_versioned_handlers(
            endpoint,
            active_version,
            deprecated_versions,
            deprecated_handler)
        self.assertEqual(versioned, expected)

    def test_resolve_name(self):
        module = resolve_name("api.endpoints.document")
        self.assertIsNotNone(module)
        self.assertEqual(module.__name__, "api.endpoints.document")

    def test_resolve_name_missing(self):
        with self.assertRaises(ImportError):
            resolve_name("api.endpoints.missing")

    def test_resolve_name_empty(self):
        with self.assertRaises(ValueError):
            resolve_name("")
