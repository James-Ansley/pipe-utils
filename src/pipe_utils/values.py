"""
Contains several utility functions to support processing single values
"""

import operator
from collections.abc import Callable
from typing import Any

from ._types import *

__all__ = [
    "and_",
    "clamp",
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
]

Cond1 = Callable[[T], V]
Cond2 = Callable[[T], R]
Cond = Callable[[T], V | R]


def and_(cond1: Cond1, cond2: Cond2) -> Cond:
    """Returns a predicate equal to (it) -> cond1(it) and cond2(it)"""
    return lambda item: cond1(item) and cond2(item)


def clamp(lower: T, upper: T) -> Callable[[T], T]:
    """
    Returns a callable that clamps a value between lower and upper.
    Equivalent to :code:`max(lower, min(item, upper))`
    """
    return lambda item: max(lower, min(item, upper))


def is_(obj: Any) -> Callable[[Any], bool]:
    """Returns a callable that takes a parameter x and returns x is n"""
    return lambda item: operator.is_(item, obj)


def is_even(item: int) -> bool:
    """Returns True if the give value is even and False otherwise"""
    return item % 2 == 0


def is_congruent(a: int, n: int) -> Callable[[int], bool]:
    """
    Returns a callable that takes a single integer value. The callable
    returns True of the given integer, i, is congruent a mod m. That is,
    (i - a) mod n == 0
    """
    return lambda item: (item - a) % n == 0


def is_none(item: Any) -> bool:
    """Returns True if the given item is None"""
    return item is None


def is_not(obj: Any) -> Callable[[Any], bool]:
    """Returns a callable that takes a parameter x and returns x is not n"""
    return lambda item: operator.is_not(item, obj)


def is_not_none(item: Any) -> bool:
    """Returns True if the given item is not None"""
    return item is not None


def is_odd(item: int) -> bool:
    """Returns True if the give value is odd and False otherwise"""
    return item % 2 == 1


def lclamp(lower: T) -> Callable[[T], T]:
    """
    Returns a callable that left clamps a value with a lower bound.
    Equivalent to :code:`max(lower, item)`
    """
    return lambda item: max(lower, item)


def not_(func: Predicate) -> Predicate:
    """Returns a predicate equal to (it) -> not func(it)"""
    return lambda item: not func(item)


def or_(cond1: Cond1, cond2: Cond2) -> Cond:
    """Returns a predicate equal to (it) -> cond1(it) or cond2(it)"""
    return lambda item: cond1(item) or cond2(item)


def raise_(exception: E | EType, *, from_: E | None = nothing):
    """
    Raise expression. Raises exceptions. If ``from`` is given, will raise the
    exception from that.
    """
    if from_ is nothing:
        raise exception
    else:
        raise exception from from_


def raises(exception: E | EType, *, from_: E | None = nothing):
    """
    Returns a callable that takes any args or kwargs, and raises the given
    exception. If ``from`` is given, will raise the exception from that.
    """
    return lambda *args, **kwargs: raise_(exception, from_=from_)


def rclamp(upper: T) -> Callable[[T], T]:
    """
    Returns a callable that right clamps a value with an upper bound.
    Equivalent to :code:`min(item, upper)`
    """
    return lambda item: min(item, upper)
