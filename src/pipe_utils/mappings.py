from collections.abc import ItemsView, Mapping
from typing import KeysView, TypeVar, ValuesView

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def items(data: Mapping[K, V]) -> ItemsView[K, V]:
    return data.items()


def keys(data: Mapping[K, ...]) -> KeysView[K]:
    return data.keys()


def values(data: Mapping[..., V]) -> ValuesView[V]:
    return data.values()
