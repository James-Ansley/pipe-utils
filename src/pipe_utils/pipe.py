from collections.abc import Callable, Iterable
from typing import Generic, Type, TypeVar

__all__ = ["Args", "Pipe"]

T = TypeVar("T")
R = TypeVar("R")
V = TypeVar("V")
E = TypeVar("E", bound=BaseException)
Handler = Callable[[E], R]
ExceptionType = Type[E] | tuple[Type[E], ...]
_Args = "Callable[[T], R] | Iterable[Callable[[T], R], ...] | Args"


class Args:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs


class Pipe(Generic[T, R]):
    def __init__(self, data: T):
        self._data: T = data
        self._err: Exception | None = None

    @classmethod
    def _from_err(cls, err):
        pipe = Pipe(None)
        pipe._err = err
        return pipe

    def then(self, func: Callable[[T, ...], R], *args, **kwargs) -> "Pipe[R]":
        if self._err is not None:
            return self
        try:
            return Pipe(func(self._data, *args, **kwargs))
        except Exception as e:
            return Pipe._from_err(e)

    def __or__(self, other: _Args) -> "Pipe[R]":
        if isinstance(other, Args):
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
        if isinstance(self._err, exception):
            return Pipe(handler(self._err))
        return self

    def get(self):
        if self._err is not None:
            raise self._err
        return self._data

    def get_or_else(self, default=None):
        if self._err is not None:
            return default
        return self._data

    def get_or_raise(self, exception: E | Type[E]):
        if self._err is not None:
            raise exception from self._err
        return self._data
