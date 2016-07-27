# -*- encoding: utf-8 -*-
import unittest

from api.utils import canonicalize, merge


class TestUtils(unittest.TestCase):
    def test_update_settings(self):
        main_dict = {
            "flag": True,
            "section": {
                "flag": True
            }
        }
        custom_dict = {
            "section": {
                "flag": False,
                "debug": True
            }
        }
        expected = {
            "flag": True,
            "section": {
                "flag": False,
                "debug": True
            }
        }

        merge(main_dict, custom_dict)
        self.assertEqual(main_dict, expected)

    def test_update_setting_empty_custom_settings(self):
        main_dict = {
            "flag": True,
            "section": {
                "flag": True
            }
        }
        custom_dict = {}
        expected = {
            "flag": True,
            "section": {
                "flag": True
            }
        }

        merge(main_dict, custom_dict)
        self.assertEqual(main_dict, expected)

    def test_get_canonicalized_first_level(self):
        item = {
            "empty_dict": {},
            "empty_list": [],
            "empty_str": "",
            "none": None,
            "dict": {"hello": "world"},
            "list": ["hello", "world"],
            "str": "hello world",
        }
        expected = {
            "dict": {"hello": "world"},
            "list": ["hello", "world"],
            "str": "hello world"
        }

        canonical = canonicalize(item)
        self.assertEqual(canonical, expected)

    def test_get_canonicalized_second_level(self):
        item = {
            "empty_dict": {
                "empty_dict": {},
                "empty_list": [],
                "empty_str": "",
                "none": None,
            }
        }

        canonical = canonicalize(item)
        self.assertEqual(canonical, {})
