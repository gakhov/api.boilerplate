# -*- coding: utf-8 -*-

import calendar
import logging

from datetime import datetime
from functools import wraps
from urlparse import parse_qs

from ..exceptions import APIClientError
from ..settings import settings
from . import container


logger = logging.getLogger('api.utils')


def authenticated():
    """Check if user is registered and can be authenticated."""
    @container
    def _authenticate(rh_method):
        @wraps(rh_method)
        def _wrapper(self, *args, **kwargs):
            keys = parse_qs(self.request.query).get("api_key")
            api_key = keys[0] if keys else None
            if api_key in settings["customers"].keys():
                customer_config = settings["customers"][api_key]
                setattr(self, "api_key", api_key)
                setattr(self, "customer", customer_config["customer"])
                setattr(self, "allowed_endpoints", customer_config.get(
                    "allowed_endpoints", {}))
                return rh_method(self, *args, **kwargs)

            logger.warning("Not Authenticated")
            raise APIClientError(
                401, "Not Authenticated", "Include a valid api_key")
        return _wrapper
    return _authenticate


def authorized():
    """Check if authenticated user can access the requested endpoint."""
    @container
    def _authorize(rh_method):
        @wraps(rh_method)
        def _wrapper(self, *args, **kwargs):
            assert all([
                hasattr(self, "endpoint"),
                hasattr(self, "customer"),
                hasattr(self, "allowed_endpoints")
            ]), "Missing authentication info"

            if self.endpoint in self.allowed_endpoints:
                endpoint_config = self.allowed_endpoints[self.endpoint]
                setattr(self, "rate_limit", endpoint_config.get("rate_limit"))
                setattr(self, "ttl", endpoint_config.get("ttl"))
                return rh_method(self, *args, **kwargs)

            logger.warning("Forbidden")
            raise APIClientError(
                403, "Forbidden", "Access denied")
        return _wrapper
    return _authorize


def rate_limited():
    """Check if user uses endpoint with allowed frequency."""
    @container
    def _limit(rh_method):
        @wraps(rh_method)
        def _wrapper(self, *args, **kwargs):
            assert all([
                hasattr(self, "endpoint"),
                hasattr(self, "rate_limit")
            ]), "Missing authorization info"

            if self.rate_limit is None or self.ttl is None:
                return rh_method(self, *args, **kwargs)

            now = int(calendar.timegm(datetime.utcnow().utctimetuple()))
            key = "api:{}:{}".format(self.api_key, self.endpoint)

            current = self.application.redis.get(key)
            if current is not None:
                remaining, ttl = (
                    int(self.application.redis.decr(key)),
                    int(self.application.redis.ttl(key))
                )
            else:
                remaining, ttl = self.rate_limit - 1, self.ttl
                self.application.redis.setex(key, ttl, remaining)

            if remaining >= 0:
                self.set_header("X-RateLimit-Limit", self.rate_limit)
                self.set_header("X-RateLimit-Remaining", max(0, remaining))
                self.set_header("X-RateLimit-Reset", now + ttl)
                return rh_method(self, *args, **kwargs)

            raise APIClientError(
                429, "Rate Limit exceeded", "Rate Limit exceeded")
        return _wrapper
    return _limit
