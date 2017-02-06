# -*- coding: utf-8 -*-

from ..endpoints.base import HealthHandler

__all__ = [
    'build_versioned_handlers',
    'resolve_name'
]

_HEALTH_PATH = "/_health"


def build_versioned_handlers(endpoint, active_version, deprecated_versions,
                             deprecated_handler):
    """Build versioned handlers.

    Connect handlers with the specified endpoint and add a special
    deprecated_handler for deprecated API paths.

    """
    endpoint_handlers = []
    for handler in endpoint.handlers:
        try:
            path, handler_cls, settings = handler
        except ValueError:
            path, handler_cls = handler
            settings = {}

        settings["endpoint"] = endpoint
        endpoint_handlers.append((path, handler_cls, settings))

    def make_path(sub_path, version=active_version):
        return "/v{}/{}{}".format(version, endpoint.name, sub_path)

    versioned = []
    if endpoint.health_checks:
        versioned.append((make_path(_HEALTH_PATH), HealthHandler, settings))

    for handler in endpoint_handlers:
        sub_path, handler_cls, settings = handler
        versioned.append((make_path(sub_path), handler_cls, settings))

    versioned_paths = set([handler[0] for handler in versioned])
    for version in deprecated_versions:
        for handler in endpoint_handlers:
            sub_path, _, _ = handler
            deprecated_path = make_path(sub_path, version=version)
            if deprecated_path not in versioned_paths:
                versioned.append((deprecated_path, deprecated_handler))

    return versioned


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
