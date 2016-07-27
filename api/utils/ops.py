# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re

__all__ = [
    'build_versioned_handlers',
    'get_endpoint_app',
    'resolve_name'
]


VERSION_RE = re.compile(r'^/v(?P<version>\d+)/')


def _is_versioned_path(path):
    """Check if path contains API version information."""
    if not path.startswith("/v"):
        return False

    parsed = VERSION_RE.match(path)
    return parsed is not None


def build_versioned_handlers(handlers, active_version, deprecated_versions,
                             deprecated_handler):
    """Build versioned handlers and add a special deprecated_handler for
    paths in deprecated API versions.
    """
    versioned = []
    for handler in handlers:
        if _is_versioned_path(handler[0]):
            versioned.append(handler)
            continue
        versioned.append(
            ("/v{}{}".format(active_version, handler[0]), ) + handler[1:]
        )

    versioned_paths = set([h[0] for h in versioned])
    for version in deprecated_versions:
        for handler in handlers:
            if _is_versioned_path(handler[0]):
                continue
            deprecated_path = "/v{}{}".format(version, handler[0])
            if deprecated_path not in versioned_paths:
                versioned.append(
                    (deprecated_path, deprecated_handler)
                )
    return versioned


def get_endpoint_app(name):
    """Return Application class for the endpoint."""
    module = resolve_name('api.endpoints.' + name)
    return getattr(module, 'Application')


def resolve_name(name):
    """Resolve module by its name."""
    parts = name.split('.')
    used = parts.pop(0)
    found = __import__(used)
    for part in parts:
        used += '.' + part
        try:
            found = getattr(found, part)
        except AttributeError:
            __import__(used)
            found = getattr(found, part)
    return found
