Quick Start
===========

Pipe-Utils defines a :code:`Pipe` class that allows function calls to be chained together with the pipe operator (:code:`|`).
Pipe-Utils also defines several utility functions in the :mod:`pipe_utils.iterables`, :mod:`pipe_utils.mappings`, and :mod:`pipe_utils.values` modules.


Install
-------

To install qChecker use the following command::

    pip install pipe-utils


Usage
-----

Data first needs to be wrapped in a :class:`pipe_utils.Pipe`::

    from pipe_utils import Pipe

    data = "I think pipes are cool"
    pipe = Pipe(data)

Operations can then be chained, before the result of the operation is retrieved with :code:`.get()`, :code:`.get_or_default(...)`, or :code:`.get_or_raise(...)`::

    from pipe_utils import Pipe

    data = "I think pipes are cool"

    result = (
            Pipe(data)
            | str.lower
            | str.split
            | sorted
    ).get()

    print(result)

Which would print::

    ['are', 'cool', 'i', 'pipes', 'think']


Utilities
---------

Pipe-Utils defines several utility functions in the :mod:`pipe_utils.iterables`, :mod:`pipe_utils.mappings`, and :mod:`pipe_utils.values` modules.

These modules contain several helper-functions.
Many of which take an intermediary value and return a closure / callable that will compute a result from some data and the intermediary values.
For example::

    from pipe_utils import Pipe
    from pipe_utils.iterables import *
    from pipe_utils.mappings import *

    data = "I think pipes are cool"

    result = (
            Pipe(data)
            | str.lower
            | str.split
            | group_by(len)
            | items
            | sorted
            | dict
    ).get()

    print(result)

Which prints::

    {1: ['i'], 3: ['are'], 4: ['cool'], 5: ['think', 'pipes']}

Here, the :func:`pipe_utils.iterables.group_by`, and :func:`pipe_utils.mappings.items` functions are both utility functions provided by pipe-utils.
:func:`pipe_utils.iterables.group_by` takes a key function that is used to group values by, and :func:`pipe_utils.mappings.items` can be used directly as a callable.
