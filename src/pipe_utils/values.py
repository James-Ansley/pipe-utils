"""
Contains several utility functions to support processing single values
"""

import operator
from collections.abc import Callable
from typing import Any

from .curry import curry

__all__ = [
    "and_",
    "clamp",
    "instance_of",
    "is_",
    "is_even",
    "is_congruent",
    "is_none",
    "is_not",
    "is_not_none",
    "is_odd",
    "lclamp",
    "not_",
    "or_",
    "raise_",
    "raises",
    "rclamp",
    "returns",
]

nothing = object()


# TODO List
# - instance_of
# - subclass_of


@curry
def and_[T, V1, V2](
      cond1: Callable[[T], V1],
      cond2: Callable[[T], V2],
      item: T,
) -> V1 | V2:
    """Returns a predicate equal to (it) -> cond1(it) and cond2(it)"""
    return cond1(item) and cond2(item)


def clamp[T](lower: T, upper: T) -> Callable[[T], T]:
    """
    Returns a callable that clamps a value between lower and upper.
    Equivalent to :code:`max(lower, min(item, upper))`
    """
    return lambda item: max(lower, min(item, upper))


@curry
def instance_of(type_: type | tuple[type, ...], item) -> bool:
    """Returns True if the given item is an instance of the given types."""
    return isinstance(item, type_)


@curry
def is_(obj: Any, item: Any) -> bool:
    """Returns a callable that takes a parameter x and returns x is n"""
    return operator.is_(item, obj)


@curry
def is_even(item: int) -> bool:
    """Returns True if the give value is even and False otherwise"""
    return item % 2 == 0


@curry
def is_congruent(a: int, n: int, item: int) -> bool:
    """
    Returns a callable that takes a single integer value. The callable
    returns True of the given integer, i, is congruent a mod m. That is,
    (i - a) mod n == 0
    """
    return (item - a) % n == 0


@curry
def is_none(item: Any) -> bool:
    """Returns True if the given item is None"""
    return item is None


@curry
def is_not(obj: Any, item: Any) -> bool:
    """Returns a callable that takes a parameter x and returns x is not n"""
    return operator.is_not(item, obj)


@curry
def is_not_none(item: Any) -> bool:
    """Returns True if the given item is not None"""
    return item is not None


@curry
def is_odd(item: int) -> bool:
    """Returns True if the give value is odd and False otherwise"""
    return item % 2 == 1


@curry
def lclamp[T](lower: T, item: T) -> T:
    """
    Returns a callable that left clamps a value with a lower bound.
    Equivalent to :code:`max(lower, item)`
    """
    return max(lower, item)


@curry
def not_[T](func: Callable[[T], bool], item: T) -> bool:
    """Returns a predicate equal to (it) -> not func(it)"""
    return not func(item)


@curry
def or_[T, V1, V2](
      cond1: Callable[[T], V1],
      cond2: Callable[[T], V2],
      item: T,
) -> V1 | V2:
    """Returns a predicate equal to (it) -> cond1(it) or cond2(it)"""
    return cond1(item) or cond2(item)


@curry
def raise_[E: Exception | type[Exception]](
      exception: E,
      *,
      from_: E | None = nothing,
):
    """
    Raise expression. Raises exceptions. If ``from`` is given, will raise the
    exception from that.
    """
    if from_ is nothing:
        raise exception
    else:
        raise exception from from_


def raises[E: Exception | type[Exception]](
      exception: E,
      *,
      from_: E | None = nothing,
):
    """
    Returns a callable that takes any args or kwargs, and raises the given
    exception. If ``from`` is given, will raise the exception from that.
    """
    return lambda *args, **kwargs: raise_(exception, from_=from_)


@curry
def rclamp[T](upper: T, item: T) -> T:
    """
    Returns a callable that right clamps a value with an upper bound.
    Equivalent to :code:`min(item, upper)`
    """
    return min(item, upper)


@curry
def returns[T](value: T) -> T:
    """
    Returns a callable that ignores any parameters and returns the given value
    """
    return lambda *args, **kwargs: value
