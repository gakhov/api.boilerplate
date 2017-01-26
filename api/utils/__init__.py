# -*- coding: utf-8 -*-

from functools import wraps

__all__ = [
    "container",
    "canonicalize",
    "merge",
]


def canonicalize(item):
    """Convert dict objects to their canonical representation.

    Canonical representation is a form without keys with None values,
    empty lists, dicts or strings.
    """
    if type(item) != dict:
        return item

    output = []
    for key, value in item.items():
        canonical_value = canonicalize(value)
        if canonical_value in (None, [], {}, ''):
            continue
        output.append((key, canonical_value))
    return dict(output)


def container(dec):
    """Meta-decorator (for decorating decorators).

    Credits: http://stackoverflow.com/a/1167248/1798683
    """
    @wraps(dec)
    def meta_decorator(f):
        decorator = dec(f)
        decorator.orig_func = f
        return decorator
    return meta_decorator


def merge(main_dict, custom_dict, path=None):
    """Deep merge of custom_dict into main_dict.

    On collision, main_dict values will be overwritten by custom_dict.
    """
    if path is None:
        path = []

    for key in custom_dict:
        if key not in main_dict:
            main_dict[key] = custom_dict[key]
            continue

        if not all([
                isinstance(main_dict[key], dict),
                isinstance(custom_dict[key], dict)]):
            main_dict[key] = custom_dict[key]
            continue

        merge(main_dict[key], custom_dict[key], path + [str(key)])
    return main_dict
