from collections.abc import Callable, Hashable, Iterable
from typing import Type, TypeVar

__all__ = [
    # Singleton
    "nothing",

    # Generic Types
    "T",
    "V",
    "K",
    "H",
    "E",
    "EType",
    "NestedIter",

    # Curry
    "IterCurry",
    "NestedIterCurry",
    "IterMapCurry",
    "DictCurry",

    # Reducers
    "BoolReducer",
    "IntReducer",
    "StrReducer",
    "Reducer",
    "OptionalReducer",
    "Consumer",

    # FuncUtils
    "Function",
    "Predicate",
]

nothing = object()

T = TypeVar("T")
V = TypeVar("V")
K = TypeVar("K")
H = TypeVar("H", bound=Hashable)

E = TypeVar("E", bound=BaseException)
EType = Type[E] | tuple[Type[E], ...]

NestedIter = Iterable[Iterable[T]]

IterCurry = Callable[[Iterable[T]], Iterable[T]]
NestedIterCurry = Callable[[Iterable[T]], NestedIter]
IterMapCurry = Callable[[Iterable[T]], Iterable[V]]
DictCurry = Callable[[dict[K, V]], dict[K, V]]

Reducer = Callable[[Iterable[T]], T]
OptionalReducer = Callable[[Iterable[T]], T | None]
BoolReducer = Callable[[Iterable[T]], bool]
IntReducer = Callable[[Iterable[T]], int]
StrReducer = Callable[[Iterable[T]], str]
Consumer = Callable[[Iterable[T]], None]

Function = Callable[[T], V]
Predicate = Callable[[T], bool]
