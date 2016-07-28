# -*- encoding: utf-8 -*-
import unittest

from api.utils.ops import (
    _is_versioned_path,
    build_versioned_handlers,
    get_endpoint_app,
    resolve_name
)


class TestUtilsOps(unittest.TestCase):
    def test_is_versioned_path(self):
        path = "/v1/test"

        is_versioned = _is_versioned_path(path)
        self.assertTrue(is_versioned)

    def test_is_versioned_path_not_versioned(self):
        path = "/test"

        is_versioned = _is_versioned_path(path)
        self.assertFalse(is_versioned)

    def test_is_versioned_path_almost_versioned(self):
        path = "/vq/test"

        is_versioned = _is_versioned_path(path)
        self.assertFalse(is_versioned)

    def test_build_versioned_handlers(self):
        handlers = [
            ("/test0", "TEST0"),
            ("/test1", "TEST1"),
        ]
        active_version = '2'
        deprecated_versions = ['1']
        deprecated_handler = "DEPRECATED"
        expected = [
            ("/v2/test0", "TEST0", {"endpoint": None}),
            ("/v2/test1", "TEST1", {"endpoint": None}),
            ("/v1/test0", "DEPRECATED"),
            ("/v1/test1", "DEPRECATED"),
        ]

        versioned = build_versioned_handlers(
            None,
            handlers,
            active_version,
            deprecated_versions,
            deprecated_handler)
        self.assertEqual(versioned, expected)

    def test_build_versioned_handlers_long_handler(self):
        handlers = [
            ("/test0", "TEST0", {"ADDITIONAL": True}),
            ("/test1", "TEST1"),
        ]
        active_version = '2'
        deprecated_versions = ['1']
        deprecated_handler = "DEPRECATED"
        expected = [
            ("/v2/test0", "TEST0", {"ADDITIONAL": True, "endpoint": None}),
            ("/v2/test1", "TEST1", {"endpoint": None}),
            ("/v1/test0", "DEPRECATED"),
            ("/v1/test1", "DEPRECATED"),
        ]

        versioned = build_versioned_handlers(
            None,
            handlers,
            active_version,
            deprecated_versions,
            deprecated_handler)
        self.assertEqual(versioned, expected)

    def test_build_versioned_handlers_no_deprecated(self):
        handlers = [
            ("/test0", "TEST0"),
            ("/test1", "TEST1"),
        ]
        active_version = '2'
        deprecated_versions = []
        deprecated_handler = "DEPRECATED"
        expected = [
            ("/v2/test0", "TEST0", {"endpoint": None}),
            ("/v2/test1", "TEST1", {"endpoint": None}),
        ]

        versioned = build_versioned_handlers(
            None,
            handlers,
            active_version,
            deprecated_versions,
            deprecated_handler)
        self.assertEqual(versioned, expected)

    def test_build_versioned_handlers_not_override_deprecated(self):
        handlers = [
            ("/test0", "TEST0"),
            ("/v1/test1", "TEST1"),
        ]
        active_version = '2'
        deprecated_versions = ['1']
        deprecated_handler = "DEPRECATED"
        expected = [
            ("/v2/test0", "TEST0", {"endpoint": None}),
            ("/v1/test1", "TEST1", {"endpoint": None}),
            ("/v1/test0", "DEPRECATED"),
        ]

        versioned = build_versioned_handlers(
            None,
            handlers,
            active_version,
            deprecated_versions,
            deprecated_handler)
        self.assertEqual(versioned, expected)

    def test_resolve_name(self):
        module = resolve_name("api.endpoints.demo")
        self.assertIsNotNone(module)
        self.assertEqual(module.__name__, "api.endpoints.demo")

    def test_resolve_name_missing(self):
        with self.assertRaises(ImportError):
            resolve_name("api.endpoints.missing")

    def test_resolve_name_empty(self):
        with self.assertRaises(ValueError):
            resolve_name("")

    def test_get_endpoint_app(self):
        name = "demo"
        app = get_endpoint_app(name)
        self.assertIsNotNone(app)
        self.assertEqual(app.__name__, "Application")
