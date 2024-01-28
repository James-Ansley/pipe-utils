from functools import update_wrapper
from inspect import Parameter, signature

__all__ = ["curry", "Curried"]

# VAR_PARAMS = (Parameter.VAR_KEYWORD, Parameter.VAR_POSITIONAL)
VAR_PARAMS = (Parameter.VAR_POSITIONAL,)


# noinspection PyPep8Naming
class curry:
    def __init__(self, func):
        self.func = func

        params = signature(func).parameters.values()
        if any(param.kind in VAR_PARAMS for param in params):
            raise TypeError("Cannot curry_ext.py function with varargs")

        update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        return Curried.from_call(self.func, *args, **kwargs)

    def __rshift__(self, arg):
        return self(arg)


class Curried:
    """Curry docs!"""

    def __init__(self, func, arguments=None):
        self.func = func
        self.signature = signature(func)
        if arguments is None:
            self.arguments = self.signature.bind_partial()
        else:
            self.arguments = arguments

        self.__module__ = func.__module__
        update_wrapper(self, func)

    @classmethod
    def from_call(cls, func, *args, **kwargs):
        curried = cls(func)(*args, **kwargs)
        if isinstance(curried, Curried):
            return curried._apply_defaults()
        else:
            return curried

    def _apply_defaults(self):
        self.arguments.apply_defaults()
        if len(self.arguments.arguments) == len(self.signature.parameters):
            return self.func(*self.arguments.args, **self.arguments.kwargs)
        else:
            return self

    def __call__(self, *args, **kwargs):
        args = self.signature.bind_partial(
            *self.arguments.args,
            *args,
            **self.arguments.kwargs,
            **kwargs,
        )
        if len(args.arguments) == len(self.signature.parameters):
            return self.func(*args.args, **args.kwargs)
        else:
            return type(self)(self.func, args)

    def __rshift__(self, arg):
        return self(arg)
