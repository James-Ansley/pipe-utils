:code:`it` Objects
==================

An :const:`pipe_utils.pipe.it` constant is provided that allows expressions to be built up into callable objects.
For example::

    it % 2 == 0

is equivalent to::

    lambda it_: it_ % 2 == 0

It objects work with attribute selection (:code:`it.foo`), and several operators
(e.g. :code:`it + 5`, :code:`it > 10`, :code:`~(it >> 2)`).

.. warning::
    Boolean operators (:code:`not, or, and, is, is not, in, not in`) do **NOT** work with the :code:`it` object. Instead use their corresponding helper functions in :mod:`.values` and :mod:`.iterables`

    `it` objects can also only be used to construct callables directly through operators. You cannot pass them into functions etc.
