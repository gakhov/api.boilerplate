# -*- encoding: utf-8 -*-
import unittest

from api.utils.schema import (
    _parse_qs_value,
    _rename_qs_fields,
    _simplify_qs_values
)


class TestUtilsSchema(unittest.TestCase):

    def test_parse_qs_value_int(self):
        self.assertEqual(_parse_qs_value("123"), 123)
        self.assertEqual(_parse_qs_value("-123"), -123)

    def test_parse_qs_value_boolean(self):
        self.assertEqual(_parse_qs_value("true"), True)
        self.assertEqual(_parse_qs_value("false"), False)

    def test_parse_qs_value_null(self):
        self.assertIsNone(_parse_qs_value("null"))

    def test_parse_qs_value_float(self):
        self.assertEqual(_parse_qs_value("2.3"), 2.3)
        self.assertEqual(_parse_qs_value("-2.3"), -2.3)
        self.assertEqual(_parse_qs_value("-1e+2"), -100)

    def test_parse_qs_value_dict(self):
        self.assertEqual(_parse_qs_value('{"test": 2.3}'), {"test": 2.3})
        self.assertEqual(_parse_qs_value('{"test": "a"}'), {"test": "a"})

    def test_parse_qs_value_unknown(self):
        self.assertEqual(_parse_qs_value("2.3test"), "2.3test")
        self.assertEqual(_parse_qs_value("2 test"), "2 test")
        self.assertEqual(_parse_qs_value("True"), "True")

    def test_rename_qs_fields(self):
        qs = {
            "test": [1, ],
            "tests[]": [1, 2, 3],
            "tests": [1, 2]
        }
        expected = {
            "test": [1, ],
            "tests": [1, 2, 1, 2, 3]
        }

        renamed = _rename_qs_fields(qs)
        self.assertEqual(sorted(renamed.keys()), sorted(expected.keys()))
        self.assertEqual(sorted(renamed["test"]), sorted(expected["test"]))
        self.assertEqual(sorted(renamed["tests"]), sorted(expected["tests"]))

    def test_simplify_qs_values(self):
        qs = {
            "flag": ["true", ],
            "test": ["1", "2", "3.3", "null", "boo"],
            "tests": ["1", ],
            "testss": ["1,4", ],
            "languages": "en,de",
            "platforms": "twitter,facebook"
        }
        expected = {
            "flag": True,
            "test": [1, 2, 3.3, None, "boo"],
            "tests": 1,
            "testss": "1,4",
            "languages": ["en", "de"],
            "platforms": ["twitter", "facebook"]
        }

        renamed = _simplify_qs_values(qs)
        self.assertEqual(renamed, expected)
