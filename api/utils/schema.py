# -*- coding: utf-8 -*-

import json
import jsonschema
import logging
import tornado.escape
import tornado.gen

from functools import partial, wraps
from tornado.concurrent import is_future
from urllib.parse import parse_qs

from ..exceptions import APIClientError, APIServerError
from . import container

logger = logging.getLogger('api.utils')

__all__ = ['output_validate', 'input_validate_post']


def _parse_qs_value(string, encoding="UTF-8"):
    """Guess the type and parse qs value according to it."""
    if string in ("true", "false"):
        return string == "true"

    if string == "null":
        return None

    try:
        return int(string)
    except:
        pass

    try:
        return float(string)
    except:
        pass

    string = tornado.escape.url_escape(string)
    string = tornado.escape.to_unicode(string)
    string = string.encode("raw-unicode-escape")
    string = tornado.escape.url_unescape(string, encoding)

    stripped_string = string.strip("'\"")
    if stripped_string.startswith("{") and stripped_string.endswith("}"):
        try:
            return json.loads(string)
        except:
            pass

    return string


def _rename_qs_fields(params):
    """Renamed list-like fields into normal form.

    e.g.: fields[] -> fields
    """
    renamed = {}
    for key, values in params.items():
        if key.endswith("[]"):
            key = key[:-2]
        if key in renamed:
            renamed[key] += values
        else:
            renamed[key] = values
    return renamed


def _simplify_qs_values(params, encoding="UTF-8"):
    """Simplify query_string params from lists."""
    simplified = {}
    parse_value = partial(_parse_qs_value, encoding=encoding)
    for key, values in params.items():
        if key.endswith("s") and not key.endswith("ss"):
            if isinstance(values, list) and len(values) == 1:
                values = values[0]
            if isinstance(values, str) and "," not in values:
                simplified[key] = parse_value(values)
                continue
            if isinstance(values, str) and "," in values:
                values = values.strip(",").split(",")
            simplified[key] = list(map(parse_value, values))
            continue
        elif isinstance(values, list) and len(values) > 1:
            simplified[key] = list(map(parse_value, values))
            continue
        elif key.endswith("[]"):
            simplified[key] = list(map(parse_value, values))
            continue
        simplified[key] = parse_value(values[0])
    return simplified


def input_validate_get(input_schema=None):
    """Validator for JSON input from GET."""
    @container
    def _validate(rh_method):
        """Decorator for RequestHandler schema validation.

        This decorator:
            - Converts query_string to JSON and validates it
              against input schema of the method
        :type  rh_method: function
        :param rh_method: The RequestHandler method to be decorated
        :returns: The decorated method
        :raises APIClientError: If input is invalid
        """
        @wraps(rh_method)
        def _wrapper(self, *args, **kwargs):
            input_ = None

            try:
                input_ = parse_qs(self.request.query)
                input_ = _simplify_qs_values(input_)
                input_ = _rename_qs_fields(input_)
            except ValueError as e:
                logger.exception("Malformed GET")
                raise APIClientError(400, "Malformed GET", str(e))

            if input_schema is not None:
                try:
                    jsonschema.validate(
                        input_,
                        input_schema,
                        format_checker=jsonschema.FormatChecker()
                    )
                except jsonschema.ValidationError as e:
                    logger.exception("Invalid request")
                    error = str(e).split("\n\n")[0]
                    raise APIClientError(400, "Invalid request", error)

            # A json.loads'd version of self.request["body"] is now available
            # as self.json_body
            setattr(self, "json_body", input_)

            return rh_method(self, *args, **kwargs)

        setattr(_wrapper, "input_schema", input_schema)

        return _wrapper
    return _validate


def input_validate_post(input_schema=None, optional=False):
    """Validator for JSON input from POST.

    Credits: github.com/hfaran/Tornado-JSON/
    """
    @container
    def _validate(rh_method):
        """Decorator for RequestHandler schema validation.

        This decorator:
            - Validates request body against input schema of the method
        :type  rh_method: function
        :param rh_method: The RequestHandler method to be decorated
        :returns: The decorated method
        :raises APIClientError: If input is invalid
        """
        @wraps(rh_method)
        def _wrapper(self, *args, **kwargs):
            input_ = None

            try:
                if optional and not self.request.body:
                    input_ = {}
                else:
                    encoding = "UTF-8"
                    input_ = json.loads(self.request.body.decode(encoding))
            except ValueError:
                logger.exception("Malformed JSON")
                raise APIClientError(400, "Malformed JSON", "Malformed JSON")

            if input_schema is not None:
                try:
                    jsonschema.validate(
                        input_,
                        input_schema,
                        format_checker=jsonschema.FormatChecker()
                    )
                except jsonschema.ValidationError as e:
                    logger.exception("Invalid JSON request")
                    error = str(e).split("\n\n")[0]
                    raise APIClientError(400, "Invalid JSON request", error)

            # A json.loads'd version of self.request["body"] is now available
            # as self.json_body
            setattr(self, "json_body", input_)

            return rh_method(self, *args, **kwargs)

        setattr(_wrapper, "input_schema", input_schema)

        return _wrapper
    return _validate


def output_validate(output_schema=None):
    """Output validation by schema."""
    @container
    def _validate(rh_method):
        """Decorator for RequestHandler schema validation.

        This decorator:
            - Validates output against output_schema of the method
        :type  rh_method: function
        :param rh_method: The RequestHandler method to be decorated
        :returns: The decorated method
        :raises APIServerError: If output is invalid
        """
        @wraps(rh_method)
        @tornado.gen.coroutine
        def _wrapper(self, *args, **kwargs):
            # Call the requesthandler method
            output = rh_method(self, *args, **kwargs)

            # If the rh_method returned a Future a la `raise Return(value)`
            # we grab the output.
            if is_future(output):
                output = yield output

            if output_schema is not None:
                try:
                    jsonschema.validate(
                        output,
                        output_schema,
                        format_checker=jsonschema.FormatChecker()
                    )
                except jsonschema.ValidationError as e:
                    logger.exception("Invalid JSON response")
                    error = str(e).split("\n\n")[0]
                    raise APIClientError(500, "Invalid JSON response", error)
                except:
                    logger.exception("Response Validation Error")
                    raise APIServerError(
                        500, "Invalid JSON response", "Invalid JSON response")

            self.send_json(output)
            self.finish()

        setattr(_wrapper, "output_schema", output_schema)

        return _wrapper
    return _validate
