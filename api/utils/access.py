# -*- coding: utf-8 -*-

import json
import logging

from datetime import timedelta
from functools import wraps

from ..exceptions import APIClientError
from . import container


logger = logging.getLogger("api.utils")

_DEFAULT_TTL_FOR_ACCESS = timedelta(days=1)
_SUPERADMIN_SCOPE = "__all"
_TEST_SCOPE = "__test"


def authenticated():
    """Check if user is registered and can be authenticated."""
    @container
    def _authenticate(rh_method):
        @wraps(rh_method)
        def _wrapper(self, *args, **kwargs):
            access_token = self.get_query_argument("access_token", None)
            if not access_token:
                logger.warning("Missing access token")
                raise APIClientError(
                    401, "Not Authenticated", "Include a valid access_token")

            access_cache_key = "api:access:{}".format(access_token)
            cached_details = self.application._redis.get(access_cache_key)
            if cached_details is not None:
                access_details = json.loads(cached_details)
            else:
                # TODO: Implement how you would like to authenticate
                # the user and get allowed scopes, e.g. make
                # request to the remove AUTH server with the access_token
                access_details = {
                    "id": 1,
                    "role": "admin",
                    "scopes": [_SUPERADMIN_SCOPE],
                }

                cached_details = json.dumps(access_details)
                self.application._redis.setex(
                    access_cache_key,
                    _DEFAULT_TTL_FOR_ACCESS,
                    cached_details)

            setattr(self, "_access_token", access_token)
            setattr(self, "_user_id", str(access_details["id"]))
            setattr(self, "_user_role", access_details["role"])
            setattr(self, "_scopes", access_details["scopes"])
            return rh_method(self, *args, **kwargs)
        return _wrapper
    return _authenticate


def authorized(required_scopes=None):
    """Check if authenticated user can access the requested method."""
    @container
    def _authorize(rh_method):
        @wraps(rh_method)
        def _wrapper(self, *args, **kwargs):
            assert all([
                hasattr(self, "_access_token"),
                hasattr(self, "_user_id"),
                hasattr(self, "_scopes")
            ]), "Missing authentication info"

            is_test = self.get_query_argument("_test", None)
            if is_test and any([
                _SUPERADMIN_SCOPE in self._scopes,
                _TEST_SCOPE in self._scopes,
            ]):
                setattr(self, "__is_test", True)

            if _SUPERADMIN_SCOPE in self._scopes:
                setattr(self, "__is_super", True)
                return rh_method(self, *args, **kwargs)

            # NOTE: Allow access if user has at least one of required scopes
            _required_scopes = required_scopes or []
            for scope in _required_scopes:
                if scope in self._scopes:
                    return rh_method(self, *args, **kwargs)

            logger.warning("Forbidden")
            raise APIClientError(403, "Forbidden", "Access denied")
        return _wrapper
    return _authorize
