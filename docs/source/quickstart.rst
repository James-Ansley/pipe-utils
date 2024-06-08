Quick Start
===========

Pipe-Utils defines a :code:`Pipe` class that allows function calls to be chained together with the pipe operator (:code:`|`).
Pipe-Utils also defines several utility functions in the :mod:`pipe_utils.iterables`, :mod:`pipe_utils.mappings`, and :mod:`pipe_utils.values` modules.


Install
-------

To install pipe-utils use the following command::

    pip install pipe-utils


Usage
-----

Data first needs to be wrapped in a :class:`pipe_utils.Pipe`::

    from pipe_utils import Pipe

    data = "I think pipes are cool"
    pipe = Pipe(data)

Operations can then be chained, before the result of the operation is retrieved
with :code:`.get()`, :code:`.get_or_default(...)`, or :code:`.get_or_raise(...)`
or, with the :code:`unwrap` singleton::

    from pipe_utils import Pipe

    data = "I think pipes are cool"

    result = (
            Pipe(data)
            | str.lower
            | str.split
            | sorted
            | unwrap
    )

    print(result)

Which would print::

    ['are', 'cool', 'i', 'pipes', 'think']


Utilities
---------

Pipe-Utils defines several utility functions in the :mod:`.iterables`, :mod:`.mappings`, and :mod:`.values` modules.

These modules contain several helper-functions.
Many of which take an intermediary value and return a closure / callable that will compute a result from some data and the intermediary values.
These modules are all re-exported in the base :mod:`pipe_utils` module.
For example::

    from pipe_utils import *

    data = "I think pipes are cool"

    result = (
            Pipe(data)
            | str.lower
            | str.split
            | group_by(len)
            | sorted_dict()
            | unwrap
    )

    print(result)

Which prints::

    {1: ['i'], 3: ['are'], 4: ['cool'], 5: ['think', 'pipes']}

Here, the :func:`~pipe_utils.iterables.group_by`, and :func:`~pipe_utils.mappings.sorted_dict` functions are both utility functions provided by pipe-utils.
:func:`~pipe_utils.iterables.group_by` takes a key function that is used to group values by, and :func:`~pipe_utils.mappings.sorted_dict` can be used directly as a callable.


If you're feeling dangerous, you could import all from the :mod:`.override`
module, which exports all the utility functions and pipe classes,
but renames :func:`~pipe_utils.iterables.filter_`,
:func:`~pipe_utils.iterables.map_`, :func:`~pipe_utils.iterables.all_`,
:func:`~pipe_utils.iterables.any_`, and :func:`~pipe_utils.iterables.slice_`
to not be followed by a trailing underscore, thus overriding their builtin
counterparts::

    from pipe_utils.override import *

    data = [[1, -3, 4], [1, 2, 3], [2, 3, 4], [5, -1, 4]]

    result = (
            Pipe(data)
            | filter(all(it >= 0))
            | map(sum_by(it * it))
            | unwrap(as_list)
    )

    print(result)  # [14, 29]
