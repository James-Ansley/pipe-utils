from collections.abc import Callable, Iterable
from typing import Generic, Type, TypeVar

__all__ = ["Then", "Pipe"]

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
