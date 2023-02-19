"""
Contains several utility functions to support processing Mappings
"""

from collections.abc import ItemsView, Mapping
from typing import KeysView, TypeVar, ValuesView

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


__all__ = ["items", "keys", "values"]


def items(data: Mapping[K, V]) -> ItemsView[K, V]:
    """returns the mapping items view"""
    return data.items()


def keys(data: Mapping[K, ...]) -> KeysView[K]:
    """returns the mapping keys view"""
    return data.keys()


def values(data: Mapping[..., V]) -> ValuesView[V]:
    """returns the mapping values view"""
    return data.values()
