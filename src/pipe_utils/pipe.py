"""Exports the Pipe, Then, and it objects/classes"""

from collections.abc import Callable, Iterable
from operator import attrgetter
from typing import Self, Type, TypeVar

from ._types import E, EType, ExceptionHandler

__all__ = ["Then", "Catch", "Pipe", "P", "it", "obj"]

T = TypeVar("T")
R = TypeVar("R")
V = TypeVar("V")
_Args = "Callable[[T], R] | Iterable[Callable[[T], R], ...] | Then"


class Then:
    """
    Container class used to store a func along with additional args and kwargs.
    Is intended to be used with :meth:`Pipe.__or__`
    (:code:`|`).

    Is evaluated as func(data, \\*args, \\*\\*kwargs) where the data is the value
    currently stored in the pipe
    """

    def __init__(self, func: Callable[[T, ...], V], *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs


class Catch:
    """
    Container class used to store exceptions and an exception handler.
    Is Intended to be used with :meth:`Pipe.__or__` (:code:`|`).

    Is equivalent to calling :meth:`Pipe.catch`
    """

    def __init__(self, exception: EType, handler: ExceptionHandler):
        self.exception = exception
        self.handler = handler


class PipeMeta(type):
    def __new__(mcs, name, bases, dct):
        return super().__new__(mcs, name, bases, dct)

    def __rshift__(cls, other) -> Self:
        return cls(other)


class Pipe[T](metaclass=PipeMeta):
    """
    Pipe class that supports chained operations on the given data. If an
    error occurs during the chaining process, the pipe goes into error
    state. The error must either be caught by calling ``.catch`` or ignored
    when yielding data with ``get_or_default`` or ``get_or_raise``
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
          func: Callable[[T, ...], R],
          *args,
          **kwargs,
    ) -> "Pipe[R]":
        """
        Returns a new pipe containing the result of calling
        func(data, \\*args, \\*\\*kwargs)
        """
        if self._err is not None:
            return self
        try:
            return Pipe(func(self._data, *args, **kwargs))
        except Exception as e:
            return Pipe._from_err(e)

    def __or__(self, other: _Args) -> "Pipe[R]":
        if isinstance(other, Callable):
            return self.then(other)
        elif isinstance(other, Iterable):
            return self.then(*other)
        elif isinstance(other, Then):
            return self.then(other.func, *other.args, **other.kwargs)
        elif isinstance(other, Catch):
            return self.catch(other.exception, other.handler)
        else:
            raise ValueError(f"cannot perform pipe with type {type(other)}")

    def catch(
          self,
          exception: EType,
          handler: ExceptionHandler,
    ) -> "Pipe[T | R]":
        """
        Catches the given exception if it has been raised and returns a new
        Pipe containing the result of the handler
        """
        if isinstance(self._err, exception):
            return Pipe(handler(self._err))
        else:
            return self

    def get(self):
        """
        Returns the result of the pipe or raises the first error encountered
        when chaining functions
        """
        if self._err is not None:
            raise self._err
        else:
            return self._data

    def get_or_default(
          self, default: V = None, *, catch: EType = Exception
    ) -> T | V:
        """
        Returns the result of the pipe or the default value if the pipe is in
        error state and the error is of type :code:`catch`. If the error is
        not of type :code:`catch`, the error is raised instead.
        """
        if self._err is None:
            return self._data
        elif isinstance(self._err, catch):
            return default
        else:
            raise self._err

    def get_or_raise(
          self,
          exception: E | Type[E],
          *,
          catch: EType = Exception,
          chained: bool = True,
    ) -> T:
        """
        Returns the result of the pipe or raises the given exception if the
        pipe is in error state and the error is of type :code:`catch`. If the
        error is not of type :code:`catch`, the error itself is raised
        instead.

        If ``chained`` is ``True``, the given exception will be
        raised from the exception currently in the ``Pipe`` object.
        Otherwise, the given exception is raised as is – but may still be
        chained if this is raised during the handling of another exception.
        """
        if self._err is None:
            return self._data
        elif isinstance(self._err, catch) and chained:
            raise exception from self._err
        elif isinstance(self._err, catch) and not chained:
            raise exception
        else:
            raise self._err


#: A short alias for Pipe
P = Pipe


class _It:
    def __init__(self, call=None):
        if call is None:
            call = lambda e, *args, **kwargs: e
        self._callable = call

    def __call__(self, value, *args, **kwargs):
        return self._callable(value, *args, **kwargs)

    def __lt__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  < (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __le__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  <= (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __eq__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  == (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __ne__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  != (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __ge__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  >= (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __gt__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  > (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __abs__(self, ):
        return _It(
            lambda e: (
                self._callable(e).__abs__()
            )
        )

    def __pos__(self, ):
        return _It(
            lambda e: (
                +self._callable(e)
            )
        )

    def __neg__(self):
        return _It(
            lambda e: (
                -self._callable(e)
            )
        )

    def __add__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  + (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __floordiv__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  // (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __matmul__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  @ (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __mod__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  % (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __mul__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  * (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __pow__(self, other, modulo=None):
        return _It(
            lambda e: (
                pow(
                    self._callable(e),
                    (other._callable(e) if isinstance(other, _It) else other),
                    (modulo._callable(e) if isinstance(modulo, _It) else modulo)
                )
            )
        )

    def __sub__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  - (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __truediv__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  / (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __or__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  | (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __and__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  & (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __invert__(self):
        return _It(
            lambda e: (
                ~self._callable(e)
            )
        )

    def __lshift__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  << (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __rshift__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  >> (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __xor__(self, other):
        return _It(
            lambda e: (
                  self._callable(e)
                  ^ (other._callable(e) if isinstance(other, _It) else other)
            )
        )

    def __getitem__(self, item):
        return _It(
            lambda e: (
                self._callable(e)[item]
            )
        )

    def __radd__(self, other):
        return _It(
            lambda e: (
                  (other._callable(e) if isinstance(other, _It) else other)
                  + self._callable(e)
            )
        )

    def __rsub__(self, other):
        return _It(
            lambda e: (
                  (other._callable(e) if isinstance(other, _It) else other)
                  - self._callable(e)
            )
        )

    def __rmul__(self, other):
        return _It(
            lambda e: (
                  (other._callable(e) if isinstance(other, _It) else other)
                  * self._callable(e)
            )
        )

    def __rmatmul__(self, other):
        return _It(
            lambda e: (
                  (other._callable(e) if isinstance(other, _It) else other)
                  @ self._callable(e)
            )
        )

    def __rtruediv__(self, other):
        return _It(
            lambda e: (
                  (other._callable(e) if isinstance(other, _It) else other)
                  / self._callable(e)
            )
        )

    def __rfloordiv__(self, other):
        return _It(
            lambda e: (
                  (other._callable(e) if isinstance(other, _It) else other)
                  // self._callable(e)
            )
        )

    def __rmod__(self, other):
        return _It(
            lambda e: (
                  (other._callable(e) if isinstance(other, _It) else other)
                  % self._callable(e)
            )
        )

    def __divmod__(self, other):
        return _It(
            lambda e: (
                divmod(
                    self._callable(e),
                    (other._callable(e) if isinstance(other, _It) else other),
                )
            )
        )

    def __rdivmod__(self, other):
        return _It(
            lambda e: (
                divmod(
                    (other._callable(e) if isinstance(other, _It) else other),
                    self._callable(e),
                )
            )
        )

    def __rpow__(self, other, modulo=None):
        return _It(
            lambda e: (
                pow(
                    (other._callable(e) if isinstance(other, _It) else other),
                    self._callable(e),
                    (modulo._callable(e) if isinstance(modulo,
                                                       _It) else modulo),
                )
            )
        )

    def __rlshift__(self, other):
        return _It(
            lambda e: (
                  (other._callable(e) if isinstance(other, _It) else other)
                  << self._callable(e)
            )
        )

    def __rrshift__(self, other):
        return _It(
            lambda e: (
                  (other._callable(e) if isinstance(other, _It) else other)
                  >> self._callable(e)
            )
        )

    def __rand__(self, other):
        return _It(
            lambda e: (
                  (other._callable(e) if isinstance(other, _It) else other)
                  & self._callable(e)
            )
        )

    def __rxor__(self, other):
        return _It(
            lambda e: (
                  (other._callable(e) if isinstance(other, _It) else other)
                  ^ self._callable(e)
            )
        )

    def __ror__(self, other):
        return _It(
            lambda e: (
                  (other._callable(e) if isinstance(other, _It) else other)
                  | self._callable(e)
            )
        )

    def __getattr__(self, item):
        return _It(
            lambda e: (
                attrgetter(item)(self._callable(e)))
        )


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
#: simple operators (e.g. :code:`it + 5`, :code:`~(it << 2)`).
#:
#: .. warning::
#:     Boolean operators (:code:`not, or, and, is, is not, in, not in`)
#:     do **NOT** work with the :code:`it` object. Instead use their
#:     corresponding helper functions in :mod:`.values` and
#:     :mod:`.iterables`
it = _It()


class _Obj[T, V]:
    def __getattr__(self, item):
        def method(*args, **kwargs):
            return _It(
                lambda e: (
                    getattr(e, item)(*args, **kwargs)
                )
            )

        return method


#: A utility object that allows for method calls
#:
#: Calling a method on :code:`obj` returns an :code:`it` object that will call
#: that method when it itself is called.
#: For example, callables can be constructed thus::
#:
#:     obj.split(",")
#:
#: This is roughly equivalent to::
#:
#:     lambda e: e.split(",")
#:
#: However, the resulting object will be an :code:`it` object which can be
#: used for attribute selection (:code:`it.foo`), and simple operators
#: (e.g. :code:`it + 5`, :code:`~(it << 2)`).
#:
#: For example::
#:
#:     obj.split(",")[0]
#:
#: .. warning::
#:     :code:`obj` objects can **NOT** be used for chained method calls
obj = _Obj()
