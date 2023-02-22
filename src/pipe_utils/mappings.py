"""
Contains several utility functions to support processing Mappings
"""

from collections.abc import Callable, ItemsView, Mapping
from operator import itemgetter
from typing import Any, KeysView, ValuesView

from pipe_utils._types import *

__all__ = [
    "item_view",
    "key_view",
    "map_keys",
    "map_values",
    "sorted_by_key",
    "sorted_by_key_by",
    "sorted_by_value",
    "sorted_by_value_by",
    "sorted_dict",
    "sorted_dict_by",
    "value_view",
]


def item_view(data: Mapping[K, V]) -> ItemsView[K, V]:
    """returns the mapping items view"""
    return data.items()


def key_view(data: Mapping[K, ...]) -> KeysView[K]:
    """returns the mapping keys view"""
    return data.keys()


def map_keys(
        func: Callable[[K], T]) -> Callable[[Mapping[K, V]], Mapping[T, V]]:
    """
    Returns a callable that maps the keys of a given mapping. If duplicate
    keys are yielded by the mapping function the only last key value pair is
    kept.
    """
    return lambda data: {func(k): v for k, v in data.items()}


def map_values(
        func: Callable[[V], T]) -> Callable[[Mapping[K, V]], Mapping[K, T]]:
    """Returns a callable that maps the values of a given mapping"""
    return lambda data: {k: func(v) for k, v in data.items()}


def sorted_by_key(data: Mapping[K, V]) -> dict[K, V]:
    """Returns a dictionary whose items are in sorted order by key value."""
    return dict(sorted(data.items(), key=itemgetter(0)))


def sorted_by_key_by(key: Callable[[K], Any] = None) -> DictCurry:
    """
    Returns a dictionary whose items are in sorted order by key value using
    the key function.
    """
    return lambda data: dict(sorted(data.items(), key=lambda it: key(it[0])))


def sorted_by_value(data: Mapping[K, V]) -> dict[K, V]:
    """Returns a dictionary whose items are in sorted order by values."""
    return dict(sorted(data.items(), key=itemgetter(1)))


def sorted_by_value_by(key: Callable[[V], Any] = None) -> DictCurry:
    """
    Returns a dictionary whose items are in sorted order by values using the
    key function
    """
    return lambda data: dict(sorted(data.items(), key=lambda it: key(it[1])))


def sorted_dict(data: Mapping[K, V]) -> dict[K, V]:
    """Returns a dictionary whose items are in sorted order."""
    return dict(sorted(data.items()))


def sorted_dict_by(key: Callable[[tuple[K, V]], Any] = None):
    """
    Returns a callable that returns a dictionary whose items are in sorted
    order using the given key function.
    """
    return lambda data: dict(sorted(data.items(), key=key))


def value_view(data: Mapping[..., V]) -> ValuesView[V]:
    """returns the mapping values view"""
    return data.values()
