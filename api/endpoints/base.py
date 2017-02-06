# -*- coding: utf-8 -*-

from operator import attrgetter
from operator import itemgetter

from tornado.gen import Return
from tornado.gen import coroutine

from ..exceptions import HealthError
from ..exceptions import HealthWarning
from ..handlers import RequestHandler
from ..utils.access import authenticated
from ..utils.schema import output_validate
from .schema import HEALTH_SCHEMA


class BaseEndpoint(object):
    """Base class for Endpoints."""

    def __init__(self, name, settings):
        self.name = name
        self.settings = settings
        self._health_checks = {}

    @property
    def handlers(self):
        return []

    @property
    def health_checks(self):
        return self._health_checks.copy()

    def add_health_check(self, name, check):
        if not name:
            raise ValueError("name must not be empty")

        self._health_checks[name] = check
        return self

    @coroutine
    def check_health(self):
        checks = []
        caugth = []
        for name, check in self._health_checks.items():
            result = {"name": name}
            try:
                yield check()
            except (HealthError, HealthWarning) as exc:
                caugth.append(exc)
                if exc.details:
                    result.update(exc.details)

                result.update({
                    "status": exc.status,
                    "reason": str(exc)
                })
            else:
                result["status"] = "ok"

            checks.append(result)

        if not caugth:
            status = "ok"
        else:
            status = max(caugth, key=attrgetter("weight")).status

        checks.sort(key=itemgetter("name"))
        raise Return({
            "status": status,
            "checks": checks
        })


class BaseEndpointHandler(RequestHandler):
    """Base class for endpoint"s handlers."""

    def initialize(self, **kwargs):
        assert "endpoint" in kwargs, "Missing endpoint"
        self.endpoint = kwargs["endpoint"]
        self.set_header("X-Endpoint-Name", self.endpoint.name)
        self.set_header("X-Endpoint-Version", self.endpoint.version)

    @authenticated()
    @coroutine
    def prepare(self, *args, **kwargs):
        return super(BaseEndpointHandler, self).prepare(*args, **kwargs)


class HealthHandler(BaseEndpointHandler):

    @output_validate(HEALTH_SCHEMA)
    def get(self):
        return self.endpoint.check_health()
