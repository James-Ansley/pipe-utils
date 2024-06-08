Pipe Objects
============

Pipes are immutable objects that hold data and can apply a function call to the pipe's data.
Each function call returns a new pipe object with the transformed data.

Note: while pipes are immutable, pipe data has interior mutability - chained function calls can mutate the interior data.
This is especially relevant for piped operations on iterators which can be consumed.

There are several ways pipes allow chained operations with the pipe operator: :code:`|`.
The result of a chain of piped calls can be retrieved via :meth:`~pipe_utils.Pipe.get`, :meth:`~pipe_utils.Pipe.get_or_default`, :meth:`~pipe_utils.Pipe.get_or_raise`, or the :func:`~pipe_utils.pipe.unwrap` function.

To start, Pipes need to be instantiated with data::

    from pipe_utils import Pipe

    data = [1, 2, 3]
    pipe = Pipe(data)


The Pipe Operator
-----------------

The basic usage for functions that take no additional args and kwargs::

    from pipe_utils import Pipe

    data = (
        Pipe("I think pipes are COOL")
        | str.lower
        | str.split
        | list
    ).get()

    print(data)  # ['i', 'think', 'pipes', 'are', 'cool']

Getting Data From a Pipe
------------------------

There are four ways to get the data from a pipe: :meth:`~pipe_utils.Pipe.get`, :meth:`~pipe_utils.Pipe.get_or_default`, :meth:`pipe_utils.Pipe.get_or_raise`, or the :func:`~pipe_utils.pipe.unwrap` function..

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

:func:`~pipe_utils.pipe.unwrap` will unwrap the data in the pipe and can optionally be given a function to apply to the resulting data. This is equivalent to usign `get`::

    from pipe_utils import Pipe

    data = (
        Pipe("I think pipes are COOL")
        | str.lower
        | str.split
        | unwrap >> as_list
    ).get()

    print(data)  # ['i', 'think', 'pipes', 'are', 'cool']
