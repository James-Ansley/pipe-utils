"""
Contains several utility functions to support processing iterables
"""

import functools
import itertools
from collections import defaultdict, deque
from collections.abc import Callable, Container, Hashable, Iterable, Mapping, \
    Reversible, \
    Sequence
from typing import Any, overload

from deprecated.sphinx import deprecated

from .curry import curry

__all__ = [
    "all_",
    "any_",
    "as_tuple",
    "as_tuples",
    "as_tuple_of_tuples",
    "as_list",
    "as_lists",
    "as_list_of_lists",
    "associate",
    "associate_with",
    "chunked",
    "consume",
    "contains",
    "contains_all",
    "count",
    "distinct",
    "distinct_by",
    "drop",
    "drop_last",
    "drop_last_while",
    "drop_while",
    "extend",
    "extend_left",
    "filter_",
    "filter_false",
    "filter_indexed",
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
    "lstrip",
    "map_",
    "map_indexed",
    "max_by",
    "min_by",
    "none",
    "not_contains",
    "pad_with",
    "partition",
    "peek",
    "reduce",
    "remove",
    "remove_last",
    "replace",
    "rstrip",
    "scan",
    "slice_",
    "sorted_by",
    "sorted_desc",
    "sorted_desc_by",
    "split_by",
    "split_by_any",
    "split_when",
    "starmap",
    "starred",
    "strip",
    "strip_while",
    "sum_by",
    "take",
    "take_last",
    "take_last_while",
    "take_while",
    "to_each",
    "transpose",
    "try_map",
    "unzip",
    "windowed",
    "wrap",
]

nothing = object()


@curry
def all_[T](func: Callable[[T], bool], data: Iterable[T]) -> bool:
    """
    Returns a callable that returns True iff all items in an iterable satisfy
    the given predicate
    """
    return all(func(e) for e in data)


@curry
def any_[T](func: Callable[[T], bool], data: Iterable[T]) -> bool:
    """
    Returns a callable that returns True iff any item in an iterable satisfies
    the given predicate
    """
    return any(func(e) for e in data)


@curry
def as_tuple[T](data: Iterable[T]) -> tuple[T, ...]:
    """Converts the given iterable to a tuple"""
    return tuple(data)


@curry
def as_tuples[T](data: Iterable[Iterable[T]]) -> Iterable[tuple[T, ...]]:
    """Lazily converts the given iterable to an iterable of tuples"""
    return (tuple(e) for e in data)


@curry
def as_tuple_of_tuples[T](
      data: Iterable[Iterable[T]]
) -> tuple[tuple[T, ...], ...]:
    """Converts the given iterable to a tuple of tuples"""
    return tuple(tuple(e) for e in data)


@curry
def as_list[T](data: Iterable[T]) -> list[T]:
    """Converts the given iterable to a list"""
    return list(data)


@curry
def as_lists[T](data: Iterable[Iterable[T]]) -> Iterable[list[T, ...]]:
    """Lazily converts the given iterable to an iterable of lists"""
    return (list(e) for e in data)


@curry
def as_list_of_lists[T](data: Iterable[Iterable[T]]) -> list[list[T]]:
    """Converts the given iterable to a list of lists"""
    return list(list(e) for e in data)


@curry
def associate[T, K, V](
      func: Callable[[T], tuple[K, V]],
      data: Iterable[T],
) -> Mapping[K, V]:
    """
    Returns a callable that returns a mapping of key value pairs produced from
    func(t) -> (k, v)

    If more than one item maps to the key, the last item is selected.
    """
    return dict(func(e) for e in data)


@curry
def associate_with[T, V](
      func: Callable[[T], V],
      data: Iterable[T]
) -> Mapping[T, V]:
    """
    Returns a callable that returns a mapping of key value pairs produced from
    func(t) -> v

    Duplicate key items are ignored.
    """
    return {k: func(k) for k in data}


@curry
def chunked[T](
      n: int,
      data: Iterable[T],
      *,
      strict: bool = True,
      partial: bool = False,
) -> Iterable[Iterable[T]]:
    """
    Returns a callable that yields items split into chunks of size n. If
    partial is True, also yields trailing chunk even if it has fewer than n
    items. If strict is True (and partial is False), will raise a value error
    if there are fewer than n trailing items at the end of the chunk sequence.
    """
    if n <= 0:
        raise ValueError("Cannot yield non-positive chunk sizes")

    data = iter(data)
    while chunk := tuple(itertools.islice(data, n)):
        if len(chunk) == n:
            yield chunk
        elif partial:
            yield chunk
        elif strict:
            raise ValueError(
                "Chunked iterator has trailing items in strict mode"
            )


@curry
def consume(data: Iterable) -> None:
    """Greedily consumes the given Iterable"""
    deque(data, maxlen=0)


@curry
def contains[T](value: T, data: Iterable[T]) -> bool:
    """
    Returns a callable that returns True if the given iterable contains the
    value
    """
    if isinstance(data, Container):
        return value in data
    else:
        return any(e == value for e in data)


@curry
def contains_all[T](values: Iterable[T], data: Iterable[T]) -> bool:
    """
    Returns a callable that returns True if the given iterable contains all
    the given values
    """
    return set(values).issubset(data)


@curry
def count[T](value: T, data: Iterable[T]) -> int:
    """
    Returns a callable that returns the number of occurrences of value in a
    given iterable
    """
    return sum(e == value for e in data)


@curry
def distinct[H: Hashable](data: Iterable[H]) -> Iterable[H]:
    """
    Returns the distinct items from a given iterable. Items must be hashable.
    """
    return dict.fromkeys(data).keys()


@curry
def distinct_by[T, K](func: Callable[[T], K], data: Iterable[T]) -> Iterable[T]:
    """
    Returns a callable that returns items from a given iterable with distinct
    keys. Keys must be hashable.

    If duplicate keys exist, the first item associated with the key is used
    """
    seen = set()
    for e in data:
        if (key := func(e)) not in seen:
            seen.add(key)
            yield e


@curry
def drop[T](n: int, data: Iterable[T]) -> Iterable[T]:
    """
    Returns a callable that drops n items from a given iterable

    :raises ValueError: if n is negative
    """
    if n < 0:
        raise ValueError("Cannot drop negative items")
    elif n == 0:
        yield from data
    else:
        it = iter(data)
        next(itertools.islice(it, n, n), None)
        yield from it


@curry
def drop_last[T](n: int, data: Iterable[T]) -> Iterable[T]:
    """
    Returns a callable that drops the last n items from a given iterable

    :raises ValueError: if n is negative
    """
    if n < 0:
        raise ValueError("Cannot drop negative items")
    elif n == 0:
        yield from data
    else:
        it = iter(data)
        window = deque(itertools.islice(it, n), maxlen=n)
        for e in it:
            value = window.popleft()
            window.append(e)
            yield value


@curry
def drop_last_while[T](
      func: Callable[[T], bool], data: Iterable[T]
) -> Iterable[T]:
    """
    Returns a callable that drops the last items of an iterable that satisfy
    the predicate
    """
    it = iter(data)
    queue = deque()
    for e in it:
        if func(e):
            queue.append(e)
        else:
            yield from queue
            queue = deque()
            yield e


@curry
def drop_while[T](func: Callable[[T], bool], data: Iterable[T]) -> Iterable[T]:
    """
    Returns a callable that drops the items of an iterable while the
    predicate is True
    """
    return itertools.dropwhile(func, data)


@curry
def extend[T](other: Iterable[T], data: Iterable[T]) -> Iterable[T]:
    """Returns a callable that yields ≈ [\\*data, \\*other]"""
    return itertools.chain(data, other)


@curry
def extend_left[T](
      other: Iterable[T],
      data: Iterable[T],
      *,
      reverse: bool = False
) -> Iterable[T]:
    """
    Returns a callable that yields ≈ [\\*other, \\*data]. This does *not*
    reverse the ``other`` iterable as other similar functions do in Python by
    default. However, calling with reverse = True will yield the equivalent
    of [ \\*reversed(other), \\*data] even if ``other`` has no default
    reverse iterator.
    """
    if reverse and isinstance(other, Reversible):
        other = reversed(other)
    elif reverse:
        other = reversed(tuple(other))
    return itertools.chain(other, data)


@curry
def filter_[T](func: Callable[[T], bool], data: Iterable[T]) -> Iterable[T]:
    """
    Returns a callable that returns an iterator yielding those items of
    the iterable for which func(item) is true.
    """
    return filter(func, data)


@curry
def filter_false[T](
      func: Callable[[T], bool],
      data: Iterable[T]
) -> Iterable[T]:
    """
    Returns a callable that returns an iterator yielding those items of
    the iterable for which func(item) is false.
    """
    return itertools.filterfalse(func, data)


@curry
def filter_indexed[T](
      func: Callable[[int, T], bool],
      data: Iterable[T],
      *,
      start: int = 0,
) -> Iterable[T]:
    """
    Returns a callable that returns an iterator yielding those items of the
    iterable for which func(i, item) is true where i is the position of the
    current item offset by the given start value.
    """
    data = enumerate(data, start=start)
    for i, e in data:
        if func(i, e):
            yield e


@curry
def find[T](func: Callable[[T], bool], data: Iterable[T]) -> T | None:
    """
    Returns a callable that returns the first item that satisfies the given
    predicate or None
    """
    return next((e for e in data if func(e)), None)


@curry
def find_last[T](func: Callable[[T], bool], data: Iterable[T]) -> T | None:
    """
    Returns a callable that returns the last item that satisfies the given
    predicate or None
    """
    it = iter(data)
    q = deque(maxlen=1)
    q.append(next((e for e in it if func(e)), None))
    for e in it:
        if func(e):
            q.append(e)
    return q.popleft()


@curry
def first[T](data: Iterable[T], *, default: T = nothing) -> T:
    """Returns the next element in data"""
    if default is nothing:
        return next(iter(data))
    else:
        return next(iter(data), default)


@curry
def flatten[T](data: Iterable[Iterable[T]]) -> Iterable[T]:
    """
    Returns a callable that returns a single iterable containing all items
    from sub-iterables in sequence
    """
    return itertools.chain.from_iterable(data)


@curry
def flat_map[T, V](
      func: Callable[[T], Iterable[V]],
      data: Iterable[T],
) -> Iterable[V]:
    """
    Returns a callable that returns a single iterable containing all the
    items from the result of func in sequence
    """
    return itertools.chain.from_iterable(map(func, data))


@curry
def fold[T](
      initial: T,
      func: Callable[[T, T], T],
      data: Iterable[T],
) -> T:
    """
    Returns a callable that reduces an iterable with the given initial value
    """
    return functools.reduce(func, data, initial)


@curry
def for_each[T](func: Callable[[T], None], data: Iterable[T]) -> None:
    """
    Returns a callable that eagerly calls func for each item in a given
    iterable
    """
    for e in data:
        func(e)


@curry
def group_by[T, H](
      func: Callable[[T], H],
      data: Iterable[T],
) -> Mapping[H, list[T]]:
    """
    Returns a callable that groups elements of an iterable by the keys
    returned from func
    """
    result = defaultdict(list)
    for e in data:
        result[func(e)].append(e)
    return result


@curry
def get[T](i: int, data: Iterable[T], *, default: T = nothing) -> T:
    """
    Returns a callable that retrieves the ith element of a given iterable. i
    must be non-negative.

    :raises IndexError: if i is not in range(len(data))
    """
    if i < 0 and default is nothing:
        raise IndexError(f"Iterable indices cannot be negative")
    try:
        return next(itertools.islice(data, i, i + 1))
    except (StopIteration, ValueError):
        if default is nothing:
            raise IndexError(f"index {i} is out of range")
        else:
            return default


@deprecated(
    version="0.4.0",
    reason="Use the `default` keyword argument in the `get` function instead"
)
def get_or_default[T, V](i: int, default: V) -> Callable[[Iterable[T]], T | V]:
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


@curry
def is_empty(data: Iterable) -> bool:
    """Returns True if the given iterable is empty and False otherwise"""
    return next(iter(data), nothing) is nothing


@curry
def is_not_empty(data: Iterable) -> bool:
    """Returns True if the given iterable is not empty and False otherwise"""
    return next(iter(data), nothing) is not nothing


@curry
def index_of[T](value: T, data: Iterable[T]) -> int:
    """
    Returns a callable that returns the 0-based position of the first
    occurrence of the given value in an Iterable. Will raise an IndexError if
    the value is not contained in the iterable.

    :raises IndexError: If the value is not contained in the iterable
    """
    try:
        return next(i for i, e in enumerate(data) if e == value)
    except StopIteration:
        raise IndexError("Value is not in the iterable")


@curry
def index_of_last[T](value: T, data: Iterable[T]) -> int:
    """
    Returns a callable that returns the 0-based position of the last
    occurrence of the given value in an Iterable. Will raise an IndexError if
    the value is not contained in the iterable.
    """
    it = enumerate(data)
    q = deque(maxlen=1)
    for i, e in it:
        if e == value:
            q.append(i)
    if len(q) == 0:
        raise IndexError("Value is not in the iterable")
    return q.pop()


@curry
def join_to_str[T](
      data: Iterable[T],
      *,
      sep: str = "",
      prefix: str = "",
      suffix: str = "",
) -> str:
    """
    Returns a callable that constructs a string with the given separator,
    prefix, and suffix. Unlike str.join, items are mapped to strings before
    joining
    """
    return "".join((prefix, sep.join(str(e) for e in data), suffix))


@curry
def last[T](data: Iterable[T]) -> T:
    """
    Returns a callable that returns the last n items from an iterable.
    n is the min of the size of the iterable or the given value.

    :raises ValueError: if the given value is negative
    """
    it = iter(data)
    window = deque((next(it),), maxlen=1)
    for e in it:
        window.append(e)
    return window


@curry
def lstrip[T](value: T, data: Iterable[T]) -> Iterable[T]:
    """
    returns a callable that strips all leading values equal to the given value
    """
    return drop_while(lambda e: e == value, data)


@curry
def map_[T, V](
      func: Callable[[T], V],
      data: Iterable[T],
) -> Iterable[V]:
    """
    Returns a callable that returns an iterator yielding those items of
    the iterable mapped with the function func(item)
    """
    return map(func, data)


@curry
def map_indexed[T, V](
      func: Callable[[int, T], V],
      data: Iterable[T],
      *,
      start: int = 0
) -> Iterable[V]:
    """
    Returns a callable that returns an iterator yielding those items of the
    iterable mapped with the function func(i, item) where i in the position
    of the current item in the iterable offset with the given start value.
    """
    return itertools.starmap(func, enumerate(data, start=start))


@curry
def max_by[T, V](
      func: Callable[[T], V],
      data: Iterable[T],
) -> T:
    """
    Returns a callable that returns the item with the max value using the key
    function
    """
    return max(data, key=func)


@curry
def min_by[T, V](
      func: Callable[[T], V],
      data: Iterable[T],
) -> T:
    """
    Returns a callable that returns the item with the min value using the key
    function
    """
    return min(data, key=func)


@curry
def none[T](func: Callable[[T], bool], data: Iterable[T]) -> bool:
    """
    Returns a callable that returns True iff no item in an iterable can be
    found that satisfies the given predicate
    """
    return not any(func(e) for e in data)


@curry
def not_contains[T](
      value: T,
      data: Iterable[T]
) -> bool:
    """
    Returns a callable that returns True if the given iterable doe not contain
    the value
    """
    return all(e != value for e in data)


@curry
def pad_with[T, V](
      fill: V,
      length: int,
      data: Iterable[T],
) -> Iterable[T | V]:
    """
    Returns a callable that pads an iterable with the specified character to
    the given length. If the length is None, an infinite iterable is returned.
    Raises a ValueError if the length is negative.

    If the iterable is longer than length, the iterable is sliced. e.g.
    :code:`pad_with("*", 2)([1, 2, 3, 4]) ≈≈ [1, 2]`
    """
    if length is None:
        return itertools.chain(data, itertools.repeat(fill))
    else:
        return itertools.islice(
            itertools.chain(data, itertools.repeat(fill)), length
        )


@curry
def partition[T](
      func: Callable[[T], bool],
      data: Iterable[T],
) -> tuple[Iterable[T], Iterable[T]]:
    """
    Returns a callable that splits an iterable into two iterables where the
    first iterable contains those items that satisfy the predicate function,
    and the second contains those items which do not
    """
    t1, t2 = itertools.tee(data, 2)
    return filter(func, t2), itertools.filterfalse(func, t1)


@curry
def peek[T](
      func: Callable[[T], None],
      data: Iterable[T],
) -> Iterable[T]:
    """
    Returns a callable that lazily applies the given function to each item in
    an iterable and yields the unmodified item. This is intended as a utility
    function to inspect/debug pipe operations.
    """
    for e in data:
        func(e)
        yield e


@curry
def reduce[T](
      func: Callable[[T, T], T],
      data: Iterable[T],
) -> T:
    """Returns a callable that reduces an iterable with the given function"""
    return functools.reduce(func, data)


@curry
def remove[T](value: T, data: Iterable[T]) -> Iterable[T]:
    """
    Returns a callable that returns all the values from a given iterable
    except the first occurrence of the given value
    """
    it = iter(data)
    yield from take_while(lambda e: e != value)(it)
    yield from it


@curry
def remove_last[T](value: T, data: Iterable[T]) -> Iterable[T]:
    """
    Returns a callable that returns all the values from a given iterable
    except the last occurrence of the given value
    """
    it = iter(data)
    queue = deque()
    for e in it:
        if e == value:
            yield from queue
            queue = deque((e,))
        elif queue:
            queue.append(e)
        else:
            yield e
    if queue:
        queue.popleft()
    yield from queue


@curry
def replace[T, V](old: T, new: V, data: Iterable[T]) -> Iterable[T | V]:
    """Returns a callable that replaces all occurrences of *old* with *new*"""
    for e in data:
        if e != old:
            yield e
        else:
            yield new


@curry
def rstrip[T](value: T, data: Iterable[T]) -> Iterable[T]:
    """
    returns a callable that strips all trailing values in an iterable which are
    equal to the given value
    """
    return drop_last_while(lambda e: e == value, data)


@curry
def scan[T, V](
      func: Callable[[V, T], V],
      data: Iterable[T],
      initial: V = None,
) -> Iterable[V]:
    """Returns a callable that yields accumulated values"""
    return itertools.accumulate(data, func, initial=initial)


@overload
def slice_[T](stop: int) -> Callable[[Iterable[T]], Iterable[T]]:
    """Returns a callable returns items up to the index before the stop value"""


@overload
def slice_[T](start: int, stop: int) -> Callable[[Iterable[T]], Iterable[T]]:
    """
    Returns a callable returns items from the given start index to the
    index before the stop value
    """


@overload
def slice_[T](
      start: int, stop: int, step: int) -> Callable[[Iterable[T]], Iterable[T]]:
    """
    Returns a callable that returns items from the given start index to one
    before the given stop index with the given step size
    """


def slice_(*args):
    """Slices iterable with [start,] stop, [step=1] args"""
    return lambda data: itertools.islice(data, *args)


@curry
def sorted_by[T, V](func: Callable[[T], V], data: Iterable[T]) -> Iterable[T]:
    """Returns a callable that sorts an iterable by the given key function"""
    return sorted(data, key=func)


@curry
def sorted_desc[T](data: Iterable[T]) -> Iterable[T]:
    """Sorts an iterable in reverse order"""
    return sorted(data, reverse=True)


@curry
def sorted_desc_by[T, V](
      func: Callable[[T], V],
      data: Iterable[T]
) -> Iterable[T]:
    """
    Returns a callable that sorts an iterable in reverse order by the given
    key function
    """
    return sorted(data, key=func, reverse=True)


@curry
def split_by[T](sep: T, data: Iterable[T]) -> Iterable[Iterable[T]]:
    """
    Returns a callable that splits an iterable by one or more separator values.

    e.g. ignoring types: :code:`split_by(-1, 0)([1, 2, 0, -1, 3, 4, -1])`
    is equivalent to :code:`[[1, 2], [], [3, 4], []]`
    """
    next_ = deque()
    for e in data:
        if e != sep:
            next_.append(e)
        else:
            yield next_
            next_ = deque()
    yield next_


@curry
def split_by_any[T](
      separators: Container[T],
      data: Iterable[T]
) -> Iterable[Iterable[T]]:
    """Splits the given iterable by any occurrence of a value in separators"""
    next_ = deque()
    for e in data:
        if e not in separators:
            next_.append(e)
        else:
            yield next_
            next_ = deque()
    yield next_


@curry
def split_when[T](
      func: Callable[[T], bool],
      data: Iterable[T],
) -> Iterable[Iterable[T]]:
    """Splits the given iterable when the predicate for an item is truthy"""
    next_ = deque()
    for e in data:
        if not func(e):
            next_.append(e)
        else:
            yield next_
            next_ = deque()
    yield next_


@curry
def starmap[T, V](
      func: Callable[[...], V],
      data: Iterable[T],
) -> Iterable[V]:
    """Returns a callable that returns the mapped starred values"""
    return itertools.starmap(func, data)


@curry
def starred[T, V](
      func: Callable[[...], V], **kwargs,
) -> Callable[[Iterable[T]], Iterable[V]]:
    """
    Returns a callable that takes in data and calls func with the data starred.
    Kwargs are passed to the function.
    """
    return lambda data: func(*data, **kwargs)


@curry
def strip[T](value: T, data: Iterable[T]) -> Iterable[T]:
    """
    returns a callable that strips all leading and trailing values equal to
    the given value
    """
    return strip_while(lambda e: e == value, data)


@curry
def strip_while[T](func: Callable[[T], bool], data: Iterable[T]) -> Iterable[T]:
    """
    returns a callable that strips all leading and trailing values that
    satisfy the given predicate.

    Use :func:`drop_while` and :func:`drop_last_while` for the equivalent
    left and right counterparts
    """
    return drop_last_while(func)(drop_while(func)(data))


@curry
def sum_by[T, V](func: Callable[[T], V], data: Iterable[T], start: V = 0) -> V:
    """Returns a callable that sums an iterable by the given function"""
    return sum((func(e) for e in data), start=start)


@curry
def take[T](n: int, data: Iterable[T]) -> Iterable[T]:
    """
    Returns a callable that returns the first n items form a given iterable

    :raises ValueError: if n is negative
    """
    if n < 0:
        raise ValueError("Cannot take negative items")
    return itertools.islice(data, n)


@curry
def take_last[T](n: int, data: Iterable[T]) -> Iterable[T]:
    """
    Returns a callable that returns the last n items form a given iterable

    :raises ValueError: if n is negative
    """
    if n < 0:
        raise ValueError("Cannot take negative items")
    return iter(deque(data, maxlen=n))


@curry
def take_last_while[T](
      func: Callable[[T], bool],
      data: Iterable[T],
) -> Iterable[T]:
    """
    Returns a callable that returns the last elements from an iterable that
    satisfy the given predicate
    """
    it = iter(data)
    queue = deque()
    for e in it:
        if func(e):
            queue.append(e)
        else:
            queue = deque()
    yield from queue


@curry
def take_while[T](func: Callable[[T], bool], data: Iterable[T]) -> Iterable[T]:
    """
    Returns a callable that returns the first elements from an iterable that
    satisfy the given predicate
    """
    return itertools.takewhile(func, data)


@curry
def to_each[T](func: Callable[[T], Any], data: Iterable[T]) -> Iterable[T]:
    """
    Returns a callable that eagerly applies the given function to each item
    an iterable and returns the iterable.

    Is only intended a convenience function to allow for mutations over
    iterator items.
    """
    thing1, thing2 = itertools.tee(data, 2)
    for thing in thing1:
        func(thing)
    return thing2


@curry
def transpose[T](data: Iterable[Iterable[T]]) -> Iterable[Iterable[T]]:
    """Returns the data transposed. e.g. [[1, 2], [3, 4]] -> [[1, 3], [2, 4]]"""
    return zip(*data)


@curry
def try_map[T, V, E: type[Exception] | tuple[type[Exception], ...]](
      func: Callable[[T], V],
      data: Iterable[T],
      *,
      catch: E = Exception,
      default: V = nothing,
) -> Iterable[V]:
    """
    Returns a callable that attempts to map each item in an iterable.

    :param func: The mapping function
    :param catch: The error type(s) that will be excepted
    :param default: The value that will be used if the error type err is raised
        – if not provided the error is simply ignored and no value is yielded
    """
    for e in data:
        try:
            yield func(e)
        except catch:
            if default is not nothing:
                yield default


@curry
def unzip[T, V](
      data: Iterable[Sequence[T, V]] | Mapping[T, V]
) -> tuple[Iterable[T], Iterable[V]]:
    """
    Returns a tuple of two iterables, the first contains the first element of
    the given data, the second iterable contains the second element form the
    given data
    """
    if isinstance(data, Mapping):
        return data.keys(), data.values()
    thing1, thing2 = itertools.tee(data, 2)
    return (e[0] for e in thing1), (e[1] for e in thing2)


@curry
def windowed[T](
      n: int,
      data: Iterable[T],
      *,
      strict: bool = True,
      partial: bool = False,
) -> Iterable[Iterable[T]]:
    """
    Returns a callable that returns a sliding window of size n over an
    iterable. If strict is True, Raises a ValueError if the window size is
    bigger than the given iterable, otherwise an empty iterable is returned.
    If partial is True, the trailing partial windows at the end are yielded –
    supersedes the behaviour of strict.

    :raises ValueError: if n is non-positive
    """
    if n <= 0 and strict:
        raise ValueError("Cannot yield non-positive window sizes")
    elif n <= 0:
        return tuple()
    else:
        it = iter(data)
        window = deque(itertools.islice(it, n), maxlen=n)
        if len(window) == n:
            yield tuple(window)

        elif len(window) < n:
            if strict:
                raise ValueError("Window is larger than iterable length")
            elif not partial:
                return tuple()
        for x in it:
            window.append(x)
            yield tuple(window)
        if partial:
            if len(window) == n:
                window.popleft()
            while window:
                yield tuple(window)
                window.popleft()


@curry
def wrap[T](
      other: Iterable[T],
      data: Iterable[T],
      *,
      reverse_left: bool = False,
) -> Iterable[T]:
    """
    Returns a callable that yields ≈ [\\*other, \\*data, \\*other]
    if ``reverse_left`` is True, yields the equivalent of
    [\\*reversed(other), \\*data, \\*other]
    """
    other1, other2 = itertools.tee(other, 2)
    if reverse_left:
        other1 = reversed(tuple(other1))
    return itertools.chain(other1, data, other2)
