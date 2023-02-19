import functools
import itertools
from collections import defaultdict, deque
from collections.abc import Callable, Hashable, Iterable, Mapping, Sequence
from typing import Type, TypeVar, overload

T = TypeVar("T")
V = TypeVar("V")
K = TypeVar("K")
H = TypeVar("H", bound=Hashable)

E = TypeVar("E", bound=BaseException)
EType = Type[E] | tuple[Type[E], ...]

Iter = Callable[[Iterable[T]], Iterable[T]]
NestedIter = Callable[[Iterable[T]], Iterable[Iterable[T]]]
Map = Callable[[T], V]
IterMap = Callable[[Iterable[T]], Iterable[V]]

Predicate = Callable[[T], bool]
BoolReducer = Callable[[Iterable[T]], bool]

IntReducer = Callable[[Iterable[T]], int]
StrReducer = Callable[[Iterable[T]], str]

Reducer = Callable[[Iterable[T]], T]
OptionalReducer = Callable[[Iterable[T]], T | None]

Consumer = Callable[[Iterable[T]], None]

__all__ = [
    "all_",
    "any_",
    "associate",
    "associate_with",
    "chunked",
    "concat",
    "concat_after",
    "contains",
    "contains_all",
    "count",
    "distinct",
    "distinct_by",
    "drop",
    "drop_last",
    "drop_last_while",
    "drop_while",
    "filter_",
    "filter_false",
    "find",
    "find_last",
    "first",
    "flatten",
    "flat_map",
    "fold",
    "for_each",
    "group_by",
    "get",
    "get_or_default",
    "is_empty",
    "is_not_empty",
    "index_of",
    "index_of_last",
    "join_to_str",
    "last",
    "map_",
    "max_by",
    "min_by",
    "none",
    "partition",
    "peek",
    "reduce",
    "scan",
    "slice_",
    "sorted_by",
    "sorted_desc",
    "sorted_desc_by",
    "starmap",
    "take",
    "take_last",
    "take_last_while",
    "take_while",
    "try_map",
    "windowed",
    "unzip",
]


def all_(func: Predicate) -> BoolReducer:
    """
    Returns a callable that returns True iff all items in an iterable satisfy
    the given predicate
    """
    return lambda data: all(func(e) for e in data)


def any_(func: Predicate) -> BoolReducer:
    """
    Returns a callable that returns True iff any item in an iterable satisfies
    the given predicate
    """
    return lambda data: any(func(e) for e in data)


def associate(
        func: Callable[[T], tuple[K, V]],
) -> Callable[[Iterable[T]], Mapping[K, V]]:
    """
    Returns a callable that returns a mapping of key value pairs produced from
    func(t) -> (k, v)

    If more than one item maps to the key, the last item is selected.
    """
    return lambda data: dict(func(e) for e in data)


def associate_with(func: Map) -> Callable[[Iterable[T]], Mapping[T, V]]:
    """
    Returns a callable that returns a mapping of key value pairs produced from
    func(t) -> v

    Duplicate key items are ignored.
    """
    return lambda data: {k: func(k) for k in data}


def chunked(n: int) -> NestedIter:
    """Returns a callable that yields items split into chunks of size n"""
    if n <= 0:
        raise ValueError("Cannot yield non-positive chunk sizes")

    def _func(data):
        data = iter(data)
        while chunk := tuple(itertools.islice(data, n)):
            yield chunk

    return _func


def concat(other: Iterable[T]) -> Iter:
    """Returns a callable that yield [*data, *other]"""
    return lambda data: itertools.chain(data, other)


def concat_after(other: Iterable[T]) -> Iter:
    """Returns a callable that yield [*other, *data]"""
    return lambda data: itertools.chain(other, data)


def contains(value: T) -> BoolReducer:
    """
    Returns a callable that returns True if the given iterable contains the
    value
    """
    return lambda data: any(e == value for e in data)


def contains_all(values: Iterable[T]) -> BoolReducer:
    """
    Returns a callable that returns True if the given iterable contains all
    the given values
    """
    return lambda data: set(values).issubset(data)


def count(value: T) -> IntReducer:
    """
    Returns a callable that returns the number of occurrences of value in a
    given iterable
    """
    return lambda data: sum(e == value for e in data)


def distinct(data: Iterable[H]) -> Iterable[H]:
    """
    Returns the distinct items from a given iterable. Items must be hashable.
    """
    return dict.fromkeys(data).keys()


def distinct_by(func: Callable[[T], K]) -> Iter:
    """
    Returns a callable that returns items from a given iterable with distinct
    keys. Keys must be hashable.

    If duplicate keys exist, the first item associated with the key is used
    """

    def _func(data):
        seen = set()
        for e in data:
            if (key := func(e)) not in seen:
                seen.add(key)
                yield e

    return _func


def drop(n: int) -> Iter:
    """
    Returns a callable that drops n items from a given iterable

    :raises ValueError: if n is negative
    """
    if n < 0:
        raise ValueError("Cannot drop negative items")

    def _func(data):
        it = iter(data)
        next(itertools.islice(it, n, n), None)
        return it

    return _func


def drop_last(n: int) -> Iter:
    """
    Returns a callable that drops the last n items from a given iterable

    :raises ValueError: if n is negative
    """
    if n < 0:
        raise ValueError("Cannot drop negative items")
    elif n == 0:
        return lambda data: data

    def _func(data):
        it = iter(data)
        window = deque(itertools.islice(it, n), maxlen=n)
        for e in it:
            value = window.popleft()
            window.append(e)
            yield value

    return _func


def drop_last_while(func: Predicate) -> Iter:
    """
    Returns a callable that drops the items of an iterable except the last
    items that satisfy the predicate
    """

    def _func(data):
        it = iter(data)
        queue = deque()
        for e in it:
            if func(e):
                queue.append(e)
            else:
                yield from queue
                queue = deque()
                yield e

    return _func


def drop_while(func: Predicate) -> Iter:
    """
    Returns a callable that drops the items of an iterable except the first
    items that satisfy the predicate
    """
    return lambda data: itertools.dropwhile(func, data)


def filter_(func: Predicate) -> Iter:
    """
    Returns a callable that returns an iterator yielding those items of
    the iterable for which func(item) is true.
    """
    return lambda data: filter(func, data)


def filter_false(func: Predicate) -> Iter:
    """
    Returns a callable that returns an iterator yielding those items of
    the iterable for which func(item) is false.
    """
    return lambda data: itertools.filterfalse(func, data)


def find(func: Predicate) -> OptionalReducer:
    """
    Returns a callable that returns the first item that satisfies the given
    predicate or None
    """
    return lambda data: next((e for e in data if func(e)), None)


def find_last(func: Predicate) -> OptionalReducer:
    """
    Returns a callable that returns the last item that satisfies the given
    predicate or None
    """

    def _func(data):
        it = iter(data)
        q = deque(maxlen=1)
        q.append(next((e for e in it if func(e)), None))
        for e in it:
            if func(e):
                q.append(e)
        return q.popleft()

    return _func


def first(n: int = 1) -> Iter:
    """
    Returns a callable that returns the first n items from an iterable.
    n is the min of the size of the iterable or the given value.

    :raises ValueError: if the given value is negative
    """
    if n < 0:
        raise ValueError("Cannot get a negative number of elements")
    return lambda data: itertools.islice(data, n)


def flatten(data: Iterable[Iterable[T]]) -> Iterable[T]:
    """
    Returns a callable that returns a single iterable containing all items
    from sub-iterables in sequence
    """
    return itertools.chain.from_iterable(data)


def flat_map(func: Callable[[T], Iterable[V]]) -> IterMap:
    """
    Returns a callable that returns a single iterable containing all the
    items from the result of func in sequence
    """
    return lambda data: itertools.chain.from_iterable(map(func, data))


def fold(initial: T, func: Callable[[T, T], T]) -> Reducer:
    """
    Returns a callable that reduces an iterable with the given initial value
    """
    return lambda data: functools.reduce(
        func, itertools.chain((initial,), data)
    )


def for_each(func: Callable[[T], None]) -> Consumer:
    """
    Returns a callable that greedily applies func to each item in a given
    iterable
    """

    def _func(data):
        for e in data:
            func(e)

    return _func


def group_by(
        func: Callable[[T], H]) -> Callable[[Iterable[T]], Mapping[H, list[T]]]:
    """
    Returns a callable that groups elements of an iterable by the keys
    returned from func
    """

    def _func(data: Iterable[T]) -> Mapping[K, list[T]]:
        result = defaultdict(list)
        for e in data:
            result[func(e)].append(e)
        return result

    return _func


def get(i: int) -> Reducer:
    """
    Returns a callable that retrieves the ith element of a given iterable.
    i must be non-negative

    :raises IndexError: if i is not 0 <= i < len(iterable)
    """
    if i < 0:
        raise IndexError("Cannot use negative indices on Iterable")

    def _func(data):
        try:
            return next(itertools.islice(data, i, i + 1))
        except StopIteration:
            raise IndexError(f"index {i} is out of range")

    return _func


def get_or_default(i: int, default: T) -> Reducer:
    """
    Returns a callable that retrieves the ith element of a given iterable or
    the default value if i is outside the range of 0 <= i < len(iterable).
    """

    def _func(data):
        if i < 0:
            return default
        try:
            return next(itertools.islice(data, i, i + 1))
        except StopIteration:
            return default

    return _func


def is_empty(data: Iterable) -> bool:
    """Returns True if the given iterable is empty and False otherwise"""
    return len(tuple(data)) == 0


def is_not_empty(data: Iterable) -> bool:
    """Returns True if the given iterable is not empty and False otherwise"""
    return len(tuple(data)) != 0


def index_of(value: T) -> IntReducer:
    """
    Returns a callable that returns the 0-based position of the first
    occurrence of the given value in an Iterable. Will raise an IndexError if
    the value is not contained in the iterable.
    """

    def _func(data):
        """:raises IndexError: If the value is not contained in the iterable"""
        try:
            return next(i for i, e in enumerate(data) if e == value)
        except StopIteration:
            raise IndexError("Value is not in the iterable")

    return _func


def index_of_last(value: T) -> Callable[[Iterable[T]], int]:
    """
    Returns a callable that returns the 0-based position of the last
    occurrence of the given value in an Iterable. Will raise an IndexError if
    the value is not contained in the iterable.
    """

    def _func(data):
        it = enumerate(data)
        q = deque(maxlen=1)
        for i, e in it:
            if e == value:
                q.append(i)
        if len(q) == 0:
            raise IndexError("Value is not in the iterable")
        return q.pop()

    return _func


def join_to_str(
        sep: str = "", prefix: str = "", suffix: str = "",
) -> StrReducer:
    """
    Returns a callable that constructs a string with the given separator,
    prefix, and suffix. Unlike str.join, items are mapped to strings before
    joining
    """
    return lambda data: "".join(
        (prefix, sep.join(str(e) for e in data), suffix)
    )


def last(n: int = 1) -> Iter:
    """
    Returns a callable that returns the last n items from an iterable.
    n is the min of the size of the iterable or the given value.

    :raises ValueError: if the given value is negative
    """
    if n < 0:
        raise ValueError("Cannot get a negative number of elements")

    def _func(data):
        it = iter(data)
        window = deque(itertools.islice(it, n), maxlen=n)
        for e in it:
            window.append(e)
        return window

    return _func


def map_(func: Map) -> IterMap:
    """
    Returns a callable that returns an iterator yielding those items of
    the iterable mapped with the function func(item)
    """
    return lambda data: map(func, data)


def max_by(func: Map) -> Reducer:
    """
    Returns a callable that returns the item with the max value using the key
    function
    """
    return lambda data: max(data, key=func)


def min_by(func: Map) -> Reducer:
    """
    Returns a callable that returns the item with the min value using the key
    function
    """
    return lambda data: min(data, key=func)


def none(func: Predicate) -> BoolReducer:
    """
    Returns a callable that returns True iff no item in an iterable can be
    found that satisfies the given predicate
    """
    return lambda data: not any(func(e) for e in data)


def partition(
        func: Predicate,
) -> Callable[[Iterable[T]], tuple[Iterable[T], Iterable[T]]]:
    """
    Returns a callable that splits an iterable into two iterables where the
    first iterable contains those items that satisfy the predicate function,
    and the second contains those items which do not
    """

    def _func(data):
        t1, t2 = itertools.tee(data, 2)
        return filter(func, t2), itertools.filterfalse(func, t1)

    return _func


def peek(func: Callable[[T], None]) -> Iter:
    """
    Returns a callable that lazily applies the given function to each item in
    an iterable and yields the unmodified item. This is intended as a utility
    function to inspect/debug pipe operations.
    """

    def _func(data):
        for e in data:
            func(e)
            yield e

    return _func


def reduce(func: Callable[[T, T], T]) -> Reducer:
    """Returns a callable that reduces an iterable with the given function"""
    return lambda data: functools.reduce(func, data)


# ToDo remove, removeall, removelast, etc.


def scan(func: Callable[[T, T], T], initial=None) -> Iter:
    """Returns a callable that yields accumulated values"""
    return lambda data: itertools.accumulate(data, func, initial=initial)


@overload
def slice_(stop: int) -> Iter:
    """Returns a callable returns items up to the index before the stop value"""


@overload
def slice_(start: int, stop: int) -> Iter:
    """
    Returns a callable returns items from the given start index to the
    index before the stop value
    """


@overload
def slice_(start: int, stop: int, step: int) -> Iter:
    """
    Returns a callable that returns items from the given start index to one
    before the given stop index with the given step size
    """


def slice_(*args):
    return lambda data: itertools.islice(data, *args)


def sorted_by(func: Map) -> Iter:
    """Returns a callable that sorts an iterable by the given key function"""
    return lambda data: sorted(data, key=func)


def sorted_desc(data: Iterable[T]) -> Iterable[T]:
    """Sorts an iterable in reverse order"""
    return sorted(data, reverse=True)


def sorted_desc_by(func: Map) -> Iter:
    """
    Returns a callable that sorts an iterable in reverse order by the given
    key function
    """
    return lambda data: sorted(data, key=func, reverse=True)


def starmap(func: Callable[[...], T]) -> Iter:
    return lambda data: itertools.starmap(func, data)


def take(n: int = 1) -> Iter:
    """
    Returns a callable that returns the first n items form a given iterable

    :raises ValueError: if n is negative
    """
    if n < 0:
        raise ValueError("Cannot take negative items")

    return lambda data: itertools.islice(data, n)


def take_last(n: int = 1) -> Iter:
    """
    Returns a callable that returns the last n items form a given iterable

    :raises ValueError: if n is negative
    """
    if n < 0:
        raise ValueError("Cannot take negative items")

    return lambda data: iter(deque(data, maxlen=n))


def take_last_while(func: Predicate) -> Iter:
    """
    Returns a callable that returns the last elements from an iterable that
    satisfy the given predicate
    """

    def _func(data):
        it = iter(data)
        queue = deque()
        for e in it:
            if func(e):
                queue.append(e)
            else:
                queue = deque()
        yield from queue

    return _func


def take_while(func: Predicate) -> Iter:
    """
    Returns a callable that returns the first elements from an iterable that
    satisfy the given predicate
    """
    return lambda data: itertools.takewhile(func, data)


def try_map(
        func: Map,
        err: Type[E] | tuple[Type[E], ...] = Exception,
        default: V = None,
        *,
        ignore_errors: bool = False
) -> IterMap:
    """
    Returns a callable that attempts to map each item in an iterable.

    :param func: The mapping function
    :param err: The error type(s) that will be excepted
    :param default: The value that will be used if the error type err is raised
    :param ignore_errors: If False, the default value will replace values that
        error, otherwise values that error are skipped
    """

    def _func(data):
        for e in data:
            try:
                yield func(e)
            except err:
                if not ignore_errors:
                    yield default

    return _func


def windowed(n: int) -> NestedIter:
    """
    Returns a callable that returns a sliding window of size n over an iterable.
    Raises a ValueError if the window size is bigger than the given iterable

    :raises ValueError: if n is non-positive
    """
    if n <= 0:
        raise ValueError("Cannot yield non-positive window sizes")

    def _func(data):
        it = iter(data)
        window = deque(itertools.islice(it, n), maxlen=n)
        if len(window) == n:
            yield tuple(window)
        elif len(window) < n:
            raise ValueError("Window is larger than iterable length")
        for x in it:
            window.append(x)
            yield tuple(window)

    return _func


def unzip(
        data: Iterable[Sequence[T, V]] | Mapping[T, V]
) -> tuple[Iterable[T], Iterable[V]]:
    """
    Returns a tuple of two iterables, the first cotnains the first element of
    the given data, the second iterable contains the second element form the
    given data
    """
    if isinstance(data, Mapping):
        return data.keys(), data.values()
    thing1, thing2 = itertools.tee(data, 2)
    return (e[0] for e in thing1), (e[1] for e in thing2)
