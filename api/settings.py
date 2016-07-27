# -*- encoding: utf-8 -*-

import logging
import os

from .logconfig import initialize_logging
from .handlers import ErrorHandler


class EnvironmentType:
    """Environment Configuration."""

    PRODUCTION = "production"
    STAGING = "staging"
    TESTING = "testing"
    LOCAL = "local"
    dict = {
        LOCAL: 1,
        PRODUCTION: 2,
        TESTING: 3,
        STAGING: 4
    }

ROOT = os.path.dirname(os.path.abspath(__file__))
ENV = os.environ.get("API_ENV", EnvironmentType.LOCAL)

settings = {}
settings["debug"] = ENV != EnvironmentType.PRODUCTION
settings["default_response_timeout"] = 60
settings["default_handler_class"] = ErrorHandler
settings["default_handler_args"] = dict(status_code=404)
settings["default_server_name"] = "server5570"
settings["default_server_port"] = 5570
settings["registered_endpoints"] = [
    "demo",
]

settings["customers"] = {
    "customer01.1461678154.46K8LelsimIXzQp1PRc": {
        "customer": "customer01",
        "allowed_endpoints": {
            "demo": {
                "rate_limit": 100,
                "ttl": 86400  # 1 day in seconds
            }
        }
    },
    "test.1461680306.HeEEI73nvembtLHk2eM": {
        "customer": "test",
        "allowed_endpoints": {
            "test": {
                "rate_limit": 1000,
                "ttl": 86400  # 1 day in seconds
            }
        }
    }
}

settings["api_version"] = "1"
settings["deprecated_api_versions"] = []

settings["redis"] = {
    "host": "redis://localhost:6379/2",
}

SYSLOG_TAG = "api"
SYSLOG_FACILITY = logging.handlers.SysLogHandler.LOG_LOCAL2

# See PEP 391 and logconfig for formatting help.  Each section of LOGGERS
# will get merged into the corresponding section of log_settings.py.
# Handlers and log levels are set up automatically based on LOG_LEVEL and DEBUG
# unless you set them here. Messages will not propagate through a logger
# unless propagate: True is set.
LOGGERS = {
    "loggers": {
        "api": {},
        "tornado": {}
    },
}

LOG_LEVEL = logging.DEBUG if settings["debug"] else logging.INFO
USE_SYSLOG = ENV != EnvironmentType.LOCAL
initialize_logging(SYSLOG_TAG, SYSLOG_FACILITY, LOGGERS, LOG_LEVEL, USE_SYSLOG)
