:code:`it` Objects
==================

An :const:`pipe_utils.pipe.it` constant is provided that allows expressions to be built up into callable objects.
For example::

    it % 2 == 0

is equivalent to::

    lambda it_: it_ % 2 == 0

It objects work with attribute selection (:code:`it.foo`), and several operators
(e.g. :code:`it + 5`, :code:`it > 10`, :code:`~(it >> 2)`).

.. note::
    :code:`it` objects cannot be used with:
        - boolean operators :code:`not, or, and, is, is not`
        - contains operators :code:`in, not in`

    For these, use their equivalent functions in the `values` module.

    :code:`it` objects cannot be used multiple times in one expression. e.g. :code:`it * it` will not work
