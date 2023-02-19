from collections.abc import Callable
from typing import Protocol, TypeVar

T = TypeVar("T")
V = TypeVar("V")


__all__ = [
    "is_even",
    "is_odd",
    "is_congruent",
    "is_non_negative",
    "is_non_positive",
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
