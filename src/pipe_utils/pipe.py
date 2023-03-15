from collections.abc import Callable, Iterable
from operator import attrgetter
from typing import Generic, Type, TypeVar

__all__ = ["Then", "Pipe", "it"]

T = TypeVar("T")
R = TypeVar("R")
V = TypeVar("V")
E = TypeVar("E", bound=BaseException)
Handler = Callable[[E], R]
ExceptionType = Type[E] | tuple[Type[E], ...]
_Args = "Callable[[T], R] | Iterable[Callable[[T], R], ...] | Then"


class Then:
    """
    Container class used to store a func along with additional args and kwargs.
    Is intended to be used with `Pipe.__or__` (`|`).

    Is evaluated as func(data, *args, **kwargs) where the data is the value
    currently stored in the pipe
    """

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs


class Pipe(Generic[T, R]):
    """
    Pipe class that supports chained operations on the given data. If an
    error occurs during the chaining process, the pipe goes into error
    state. The error must either be caught by calling `.catch` or ignored
    when yielding data with `get_or_default` or `get_or_raise`
    """

    def __init__(self, data: T):
        self._data: T = data
        self._err: Exception | None = None

    @classmethod
    def _from_err(cls, err):
        pipe = Pipe(None)
        pipe._err = err
        return pipe

    def then(
            self,
            func: Callable[[T], R],
            *args,
            **kwargs,
    ) -> "Pipe[R]":
        """
        Returns a new pipe containing the result of calling
        func(data, *args, **kwargs)
        """
        if self._err is not None:
            return self
        try:
            return Pipe(func(self._data, *args, **kwargs))
        except Exception as e:
            return Pipe._from_err(e)

    def __or__(self, other: _Args) -> "Pipe[R]":
        if isinstance(other, Then):
            return self.then(other.func, *other.args, **other.kwargs)
        if isinstance(other, Callable):
            return self.then(other)
        elif isinstance(other, Iterable):
            return self.then(*other)
        raise ValueError(f"cannot perform pipe with type {type(other)}")

    def catch(
            self,
            exception: ExceptionType,
            handler: Handler,
    ) -> "Pipe[T | R]":
        """
        Catches the given exception if it has been raised and returns a new
        Pipe containing the result of the handler
        """
        if isinstance(self._err, exception):
            return Pipe(handler(self._err))
        return self

    def get(self):
        """
        Returns the result of the pipe or raises the first error encountered
        when chaining functions
        """
        if self._err is not None:
            raise self._err
        return self._data

    def get_or_default(self, default=None):
        """
        Returns the result of the pipe or the default value if the pipe is in
        error state
        """
        if self._err is not None:
            return default
        return self._data

    def get_or_raise(self, exception: E | Type[E]):
        """
        Returns the result of the pipe or raises the given exception if the
        pipe is in error state
        """
        if self._err is not None:
            raise exception from self._err
        return self._data


class It:
    def __init__(self, call=None):
        if call is None:
            call = lambda e, *args, **kwargs: e
        self._callable = call

    def __call__(self, value, *args, **kwargs):
        return self._callable(value, *args, **kwargs)

    def __lt__(self, other):
        return It(lambda e: self._callable(e) < other)

    def __le__(self, other):
        return It(lambda e: self._callable(e) <= other)

    def __eq__(self, other):
        return It(lambda e: self._callable(e) == other)

    def __ne__(self, other):
        return It(lambda e: self._callable(e) != other)

    def __ge__(self, other):
        return It(lambda e: self._callable(e) >= other)

    def __gt__(self, other):
        return It(lambda e: self._callable(e) > other)

    def __abs__(self, ):
        return It(lambda e: self._callable(e).__abs__())

    def __pos__(self, ):
        return It(lambda e: +self._callable(e))

    def __neg__(self):
        return It(lambda e: -self._callable(e))

    def __add__(self, other):
        return It(lambda e: self._callable(e) + other)

    def __floordiv__(self, other):
        return It(lambda e: self._callable(e) // other)

    def __matmul__(self, other):
        return It(lambda e: self._callable(e) @ other)

    def __mod__(self, other):
        return It(lambda e: self._callable(e) % other)

    def __mul__(self, other):
        return It(lambda e: self._callable(e) * other)

    def __pow__(self, other, modulo=None):
        return It(lambda e: pow(self._callable(e), other, modulo))

    def __sub__(self, other):
        return It(lambda e: self._callable(e) - other)

    def __truediv__(self, other):
        return It(lambda e: self._callable(e) / other)

    def __or__(self, other):
        return It(lambda e: self._callable(e) | other)

    def __and__(self, other):
        return It(lambda e: self._callable(e) & other)

    def __invert__(self):
        return It(lambda e: ~self._callable(e))

    def __lshift__(self, other):
        return It(lambda e: self._callable(e) << other)

    def __rshift__(self, other):
        return It(lambda e: self._callable(e) >> other)

    def __xor__(self, other):
        return It(lambda e: self._callable(e) ^ other)

    def __getitem__(self, item):
        return It(lambda e: self._callable(e)[item])

    def __radd__(self, other):
        return It(lambda e: other + self._callable(e))

    def __rsub__(self, other):
        return It(lambda e: other - self._callable(e))

    def __rmul__(self, other):
        return It(lambda e: other * self._callable(e))

    def __rmatmul__(self, other):
        return It(lambda e: other @ self._callable(e))

    def __rtruediv__(self, other):
        return It(lambda e: other / self._callable(e))

    def __rfloordiv__(self, other):
        return It(lambda e: other // self._callable(e))

    def __rmod__(self, other):
        return It(lambda e: other % self._callable(e))

    def __divmod__(self, other):
        return It(lambda e: self._callable(e).__divmod__(other))

    def __rdivmod__(self, other):
        return It(lambda e: divmod(other, e))

    def __rpow__(self, other, modulo=None):
        return It(lambda e: pow(other, self._callable(e), modulo))

    def __rlshift__(self, other):
        return It(lambda e: other << self._callable(e))

    def __rrshift__(self, other):
        return It(lambda e: other >> self._callable(e))

    def __rand__(self, other):
        return It(lambda e: other & self._callable(e))

    def __rxor__(self, other):
        return It(lambda e: other ^ self._callable(e))

    def __ror__(self, other):
        return It(lambda e: other | self._callable(e))

    def __getattr__(self, item):
        return It(lambda e: attrgetter(item)(self._callable(e)))


#: A utility object that allows for comparisons and simple operations on objects
#:
#: Using :code:`it` in simple expressions results in a callable that takes a
#: single parameter that will evaluate the expression by replacing :code:`it`.
#: For example, callables can be constructed thus::
#:
#:     it % 2 == 0
#:
#: This is equivalent to::
#:
#:     lambda value: value % 2 == 0
#:
#: :code:`it` objects can be used for attribute selection (:code:`it.foo`),
#: simple operators (e.g. :code:`it + 5`, :code:`~(it << 2)`). **EXCEPT**,
#: boolean operators (:code:`not, or, and, is, is not`) and the contains
#: operators ( :code:`in, not in`) do **NOT** work with the :code:`it` object.
#:
#: Note: only one :code:`it` object can be used per expression. :code:`it * it`
#: will not work.
it = It()
