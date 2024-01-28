"""
Contains several utility functions to support processing Mappings
"""
from collections import defaultdict
from collections.abc import Callable, ItemsView
from operator import itemgetter
from typing import Any, Iterable, KeysView, Mapping, ValuesView

from deprecated.sphinx import deprecated

from .curry import curry

__all__ = [
    "case_match",
    "case_when",
    "filter_keys",
    "filter_values",
    "get_value",
    "get_value_or_default",
    "item_view",
    "key_view",
    "map_keys",
    "map_values",
    "melt",
    "sorted_by_key",
    "sorted_by_key_by",
    "sorted_by_value",
    "sorted_by_value_by",
    "sorted_dict",
    "sorted_dict_by",
    "unmelt",
    "value_view",
]

nothing = object()


@curry
def case_match[K, V](
      cases: Mapping[K, V],
      data: K,
      *,
      default: V = nothing,
) -> V:
    """
    Maps the given data value using the cases.

    :raises ValueError: if no default is given and a matching case cannot be
        found
    """
    result = cases.get(data, default)
    if result is nothing:
        raise ValueError(f"item does not match any given case: {data}")
    else:
        return result


@curry
def case_when[T, V](
      cases: Mapping[Callable[[T], bool], V],
      data: V,
      *,
      default: Callable[[T], V] = nothing,
) -> V:
    """
    Maps the given data value using the cases. The value is checked against
    each predicate, if a match is found, the predicate's corresponding
    function is called.

    If a default is given, that is called if the value does not satisfy any
    of the given predicates.

    :raises ValueError: if no default is given and a matching case cannot be
        found
    """
    for case, then in cases.items():
        if case(data):
            return then(data)
    if default is nothing:
        raise ValueError(f"item does not match any given case: {data}")
    else:
        return default(data)


@curry
def filter_keys[K, V](
      func: Callable[[K], bool],
      data: Mapping[K, V],
) -> dict[K, V]:
    """Returns a callable that filters a mapping by keys"""
    return {k: v for k, v in data.items() if func(k)}


@curry
def filter_values[K, V](
      func: Callable[[V], bool],
      data: Mapping[K, V],
) -> dict[K, V]:
    """Returns a callable that filters a mapping by values"""
    return {k: v for k, v in data.items() if func(v)}


@curry
def get_value[K, V](
      key: K,
      data: Mapping[K, V],
      *,
      default: K = nothing,
) -> V:
    """Returns a callable that gets the value associated with the given key."""
    if default is nothing:
        return data[key]
    else:
        return data.get(key, default)


@deprecated("Use the default argument on get_value instead", "0.4.0")
def get_value_or_default[T, K, V](
      key: K,
      default: T,
) -> Callable[[Mapping[K, V]], Mapping[K, V | T]]:
    """Returns a callable that gets the value associated with the given key."""
    return lambda data: data.get(key, default)


@curry
def item_view[K, V](data: Mapping[K, V]) -> ItemsView[K, V]:
    """returns the mapping items view"""
    return data.items()


@curry
def key_view[K](data: Mapping[K, ...]) -> KeysView[K]:
    """returns the mapping keys view"""
    return data.keys()


@curry
def map_keys[T, K, V](
      func: Callable[[K], T],
      data: Mapping[K, V],
) -> Mapping[T, V]:
    """
    Returns a callable that maps the keys of a given mapping. If duplicate
    keys are yielded by the mapping function the only last key value pair is
    kept.
    """
    return {func(k): v for k, v in data.items()}


@curry
def melt[K, V](data: Mapping[K, Iterable[V]]) -> Iterable[tuple[K, V]]:
    """
    Melts a dictionary with iterable values into an iterable (Iterable[V])
    of tuples, where each tuple is of the form (<key>, <V>)
    """
    for key, values in data.items():
        for item in values:
            yield key, item


@curry
def map_values[T, K, V](
      func: Callable[[V], T],
      data: Mapping[K, V],
) -> Mapping[K, T]:
    """Returns a callable that maps the values of a given mapping"""
    return {k: func(v) for k, v in data.items()}


@curry
def sorted_by_key[K, V](data: Mapping[K, V]) -> dict[K, V]:
    """Returns a dictionary whose items are in sorted order by key value."""
    return dict(sorted(data.items(), key=itemgetter(0)))


@curry
def sorted_by_key_by[K, V](
      key: Callable[[K], Any],
      data: Mapping[K, V],
) -> dict[K, V]:
    """
    Returns a dictionary whose items are in sorted order by key value using
    the key function.
    """
    return dict(sorted(data.items(), key=lambda it: key(it[0])))


@curry
def sorted_by_value[K, V](data: Mapping[K, V]) -> dict[K, V]:
    """Returns a dictionary whose items are in sorted order by values."""
    return dict(sorted(data.items(), key=itemgetter(1)))


@curry
def sorted_by_value_by[K, V](
      key: Callable[[V], Any],
      data: Mapping[K, V],
) -> dict[K, V]:
    """
    Returns a dictionary whose items are in sorted order by values using the
    key function
    """
    return dict(sorted(data.items(), key=lambda it: key(it[1])))


@curry
def sorted_dict[K, V](data: Mapping[K, V]) -> dict[K, V]:
    """Returns a dictionary whose items are in sorted order."""
    return dict(sorted(data.items()))


@curry
def sorted_dict_by[K, V](
      key: Callable[[tuple[K, V]], Any],
      data: Mapping[K, V],
) -> dict[K, V]:
    """
    Returns a callable that returns a dictionary whose items are in sorted
    order using the given key function.
    """
    return dict(sorted(data.items(), key=key))


@curry
def unmelt[K, V](
      data: Iterable[tuple[K, V] | Iterable[K | V]]
) -> Mapping[K, list[V]]:
    """
    Unmelts an iterable of tuples (or iterables containing exactly two
    elements) of the form ``(K, V)`` and returns a mapping of the form
    ``{K, Iterable[V]}``
    """
    result = defaultdict(list)
    for k, v in data:
        result[k].append(v)
    return result


@curry
def value_view[V](data: Mapping[..., V]) -> ValuesView[V]:
    """returns the mapping values view"""
    return data.values()
