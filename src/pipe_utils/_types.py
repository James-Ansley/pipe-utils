from collections.abc import Callable, Hashable, Iterable, Mapping
from typing import Any, Type, TypeVar

__all__ = [
    # Singleton
    "nothing",

    # Generic Types
    "T",
    "V",
    "R",
    "K",
    "H",
    "E",
    "EType",
    "ExceptionHandler",
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
    "Action",
    "Function",
    "IndexedFunction",
    "Predicate",
    "IndexedPredicate",
]

nothing = object()

T = TypeVar("T")
V = TypeVar("V")
R = TypeVar("R")
K = TypeVar("K")
H = TypeVar("H", bound=Hashable)

E = TypeVar("E", bound=BaseException)
EType = Type[E] | tuple[Type[E], ...]
ExceptionHandler = Callable[[E], R]

NestedIter = Iterable[Iterable[T]]

IterCurry = Callable[[Iterable[T]], Iterable[T]]
NestedIterCurry = Callable[[Iterable[T]], NestedIter]
IterMapCurry = Callable[[Iterable[T]], Iterable[V]]
DictCurry = Callable[[Mapping[K, V]], dict[K, V]]

Reducer = Callable[[Iterable[T]], T]
OptionalReducer = Callable[[Iterable[T]], T | None]
BoolReducer = Callable[[Iterable[T]], bool]
IntReducer = Callable[[Iterable[T]], int]
StrReducer = Callable[[Iterable[T]], str]
Consumer = Callable[[Iterable[T]], None]

Action = Callable[[T], Any]
Function = Callable[[T], V]
IndexedFunction = Callable[[int, T], V]
Predicate = Callable[[T], bool]
IndexedPredicate = Callable[[int, T], bool]
