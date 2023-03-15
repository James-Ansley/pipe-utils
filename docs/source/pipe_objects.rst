Pipe Objects
============

Pipes are immutable objects that hold data and can apply a function call to the pipe's data.
Each function call returns a new pipe object with the transformed data.

Note: while pipes are immutable, pipe data has interior mutability - chained function calls can mutate the interior data.
This is especially relevant for piped operations on iterators which can be consumed.

There are several ways pipes can be used.
Namely, the :meth:`~pipe_utils.Pipe.then` and :meth:`~pipe_utils.Pipe.catch` methods, or the pipe/bitwise-or operator :code:`|`.
These methods and operators allow for functions to be chained together.
The result of a chain of piped calls can be retrieved via :meth:`~pipe_utils.Pipe.get`, :meth:`~pipe_utils.Pipe.get_or_default`, or :meth:`~pipe_utils.Pipe.get_or_raise`.

To start, Pipes need to be instantiated with data::

    from pipe_utils import Pipe

    data = [1, 2, 3]
    pipe = Pipe(data)


:code:`.then` and :code:`.catch`
--------------------------------

:meth:`~pipe_utils.Pipe.then` takes a function, :code:`func`, along with :code:`*args` and :code:`**kwargs`.
The then call is processed as :code:`func(data, *args, **kwargs)` where :code:`data` is the data contained in the pipe.
A new pipe is returned with the result of the function call.

If an error is raised by any chained function call, the pipe goes into an error state and all subsequent piped calls are ignored unless the error is caught with :meth:`~pipe_utils.Pipe.catch`.

:meth:`~pipe_utils.Pipe.catch` takes an exception type, and an exception handler.
If the pipe is in error state with an exception, :code:`e` matching the type of the exception, the handler is called: :code:`handler(e)`.
The result of the handler is then returned as a new Pipe, now no longer in error state.

If the pipe is in an error state with an error type not caught by the exception type passed into :meth:`~pipe_utils.Pipe.catch`, the pipe remains in error state.


Example
^^^^^^^
::

    from pipe_utils import *

    data = (
        Pipe(range(-10, 11))
        .then(map_(1 / it))
        .then(sum)  # consumes map, ZeroDivisionError is raised for 1 / 0
        .catch(ZeroDivisionError, lambda _: float("NaN"))  # default value of NaN
        .then(it + 1)
    ).get()

    print(data)  # NaN


The Pipe Operator
-----------------

The pipe operator is mostly equivalent to :meth:`~pipe_utils.Pipe.then`, however, it handles args and kwargs differently.
The pipe operator cannot directly be used with the :meth:`~pipe_utils.Pipe.catch` method.

The basic usage for functions that take no additional args and kwargs is the same as :meth:`~pipe_utils.Pipe.then`::

    from pipe_utils import Pipe

    data = (
        Pipe("I think pipes are COOL")
        | str.lower
        | str.split
        | list
    ).get()

    print(data)  # ['i', 'think', 'pipes', 'are', 'cool']

However, if args and kwargs are needed, a tuple of the form :code:`(func, *args)` can be provided.
For example::

    from pipe_utils import Pipe
    from operator import add, mul

    data = (
        Pipe(1)
        | (add, 5)  # calls add(data, 5)
        | (mul, 2)  # calls mul(data, 2)
    ).get()

    print(data)  # 12

In this example, it might be cleaner to use the :func:`~pipe_utils.pipe.it` object for slightly cleaner code.

If kwargs are needed, a :class:`~pipe_utils.pipes.Then` object can be constructed with any additional args or kwargs.::

    from pipe_utils import Pipe
    from pipe_utils.pipe import Then

    data = (
            Pipe(["a", "ab", "abc", "abcd"])
            | Then(sorted, reverse=True, key=len)
    ).get()

    print(data)  # ['abcd', 'abc', 'ab', 'a']

In this example, it might be cleaner to use the :func:`~pipe_utils.iterables.sorted_desc_by` function.


Getting Data From a Pipe
------------------------

There are three ways to get the data from a pipe: :meth:`~pipe_utils.Pipe.get`, :meth:`~pipe_utils.Pipe.get_or_default`, or :meth:`~pipe_utils.Pipe.get_or_raise`.

:meth:`~pipe_utils.Pipe.get` will attempt to return the result from the pipe object or raise any errors if the pipe is in error state::

    from pipe_utils import Pipe
    from pipe_utils.values import div_by, add_by

    data = (
        Pipe(1)
        | it / 0
        | it + 1
    ).get()  # Raises ZeroDivisionError


:meth:`~pipe_utils.Pipe.get_or_default` will attempt to return the data in the pipe, or if the pipe is in an error state, will return the default value.::

    data = (
        Pipe(1)
        | it / 0
        | it + 1
    ).get_or_default(float("NaN"))  # nan


:meth:`~pipe_utils.Pipe.get_or_raise` will return the data in the pipe if it is not in an error state, or it will raise a given error from the error in the pipe.::

    data = (
        Pipe(1)
        | it / 0
        | it + 1
    ).get_or_raise(ValueError("Oops!"))  # Raises ValueError from the ZeroDivisionError
