"""
Contains several utility functions to support processing Mappings
"""

from collections.abc import Callable, ItemsView, Mapping
from operator import itemgetter
from typing import Any, KeysView, TypeVar, ValuesView

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")
Dict = Callable[[dict[K, V]], dict[K, V]]

__all__ = [
    "item_view",
    "key_view",
    "value_view",
    "sorted_dict",
    "sorted_by_key",
    "sorted_by_value",
    "sorted_dict_by",
    "sorted_by_key_by",
    "sorted_by_value_by",
]


def item_view(data: Mapping[K, V]) -> ItemsView[K, V]:
    """returns the mapping items view"""
    return data.items()


def key_view(data: Mapping[K, ...]) -> KeysView[K]:
    """returns the mapping keys view"""
    return data.keys()


def value_view(data: Mapping[..., V]) -> ValuesView[V]:
    """returns the mapping values view"""
    return data.values()


def sorted_dict(data: Mapping[K, V]) -> dict[K, V]:
    """Returns a dictionary whose items are in sorted order."""
    return dict(sorted(data.items()))


def sorted_dict_by(key: Callable[[tuple[K, V]], Any] = None):
    """
    Returns a callable that returns a dictionary whose items are in sorted
    order using the given key function.
    """
    return lambda data: dict(sorted(data.items(), key=key))


def sorted_by_key(data: Mapping[K, V]) -> dict[K, V]:
    """Returns a dictionary whose items are in sorted order by key value."""
    return dict(sorted(data.items(), key=itemgetter(0)))


def sorted_by_key_by(key: Callable[[K], Any] = None) -> Dict:
    """
    Returns a dictionary whose items are in sorted order by key value using
    the key function.
    """
    return lambda data: dict(sorted(data.items(), key=lambda it: key(it[0])))


def sorted_by_value(data: Mapping[K, V]) -> dict[K, V]:
    """Returns a dictionary whose items are in sorted order by values."""
    return dict(sorted(data.items(), key=itemgetter(1)))


def sorted_by_value_by(key: Callable[[V], Any] = None) -> Dict:
    """
    Returns a dictionary whose items are in sorted order by values using the
    key function
    """
    return lambda data: dict(sorted(data.items(), key=lambda it: key(it[1])))
