"""
Contains several utility functions to support processing single values
"""

import operator
from collections.abc import Callable
from typing import Any, Protocol, TypeVar

T = TypeVar("T")
V = TypeVar("V")
R = TypeVar("R")

__all__ = [
    "is_even",
    "is_odd",
    "is_congruent",
    "is_non_negative",
    "is_non_positive",
    "is_none",
    "is_not_none",
    "add_by",
    "sub_by",
    "mul_by",
    "div_by",
    "fdiv_by",
    "mod_by",
    "matmul_by",
    "to_power",
    "eq",
    "ne",
    "lt",
    "le",
    "gt",
    "ge",
    "it_is",
    "it_is_not",
    "bit_and",
    "bit_or",
    "bit_xor",
    "rshift",
    "lshift",
]


class SupportsLE(Protocol[T, V]):
    def __le__(self: T, other: V) -> bool:
        ...


class SupportsGE(Protocol[T, V]):
    def __ge__(self: T, other: V) -> bool:
        ...


def is_even(item: int) -> bool:
    """Returns True if the give value is even and False otherwise"""
    return item % 2 == 0


def is_odd(item: int) -> bool:
    """Returns True if the give value is odd and False otherwise"""
    return item % 2 == 1


def is_congruent(a: int, n: int) -> Callable[[int], bool]:
    """
    Returns a callable that takes a single integer value. The callable
    returns True of the given integer, i, is congruent a mod m. That is,
    (i - a) mod n == 0
    """
    return lambda item: (item - a) % n == 0


def is_non_negative(item: SupportsGE) -> bool:
    """Returns True if the given item is greater than or equal to 0"""
    return item >= 0


def is_non_positive(item: SupportsLE) -> bool:
    """Returns True if the given item is less than or equal to 0"""
    return item <= 0


def is_none(item: Any) -> bool:
    """Returns True if the given item is None"""
    return item is None


def is_not_none(item: Any) -> bool:
    """Returns True if the given item is not None"""
    return item is not None


def add_by(n: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x + n"""
    return lambda item: operator.add(item, n)


def sub_by(n: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x - n"""
    return lambda item: operator.sub(item, n)


def mul_by(n: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x * n"""
    return lambda item: operator.mul(item, n)


def div_by(n: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x / n"""
    return lambda item: operator.truediv(item, n)


def fdiv_by(n: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x // n"""
    return lambda item: operator.floordiv(item, n)


def mod_by(n: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x % n"""
    return lambda item: operator.mod(item, n)


def matmul_by(n: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x @ n"""
    return lambda item: operator.matmul(item, n)


def to_power(n: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x ** n"""
    return lambda item: operator.pow(item, n)


def eq(other: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x == n"""
    return lambda item: operator.eq(item, other)


def ne(other: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x != n"""
    return lambda item: operator.ne(item, other)


def lt(other: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x < n"""
    return lambda item: operator.lt(item, other)


def le(other: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x <= n"""
    return lambda item: operator.le(item, other)


def gt(other: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x > n"""
    return lambda item: operator.gt(item, other)


def ge(other: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x >= n"""
    return lambda item: operator.ge(item, other)


def it_is(obj: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x is n"""
    return lambda item: operator.is_(item, obj)


def it_is_not(obj: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x is not n"""
    return lambda item: operator.is_not(item, obj)


def bit_and(value: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x & value"""
    return lambda item: operator.and_(item, value)


def bit_or(value: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x | value"""
    return lambda item: operator.or_(item, value)


def bit_xor(value: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x ^ value"""
    return lambda item: operator.xor(item, value)


def rshift(n: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x >> n"""
    return lambda item: operator.rshift(item, n)


def lshift(n: Any) -> Callable:
    """Returns a callable that takes a parameter x and returns x << n"""
    return lambda item: operator.lshift(item, n)
