Curried Functions
=================

Functions can be curried with the `curry` decorator::

    @curry
    def foo(x, y, z):
        x + y + z

Alternatively, existing functions can simply be passed to the curry function::

    def bar(x, y, z):
        x + y + z


    curry_bar = curry(bar)

Most functions in the pipe utils package are curried.::

    from pipe_utils.override import *

    data = [[1, -3, 4], [1, 2, 3], [2, 3, 4], [5, -1, 4]]

    result = (
          Pipe(data)
          | filter(all(it >= 0))
          | map(sum_by(it * it))
          | as_list
    ).get()

    print(result)  # [14, 29]


Here, ``filer`` and ``map``, ``all``, and ``sum_by`` are curried—they are
called with only some of their parameters which returns a callable of the
partially completed functon.

To avoid many nested brackets, curried functions have an alternative syntax to
call functions using the ``>>`` right shift operator.::

    from pipe_utils.override import *

    data = [[1, -3, 4], [1, 2, 3], [2, 3, 4], [5, -1, 4]]

    result = (
          P >> data
          | filter >> all(it >= 0)
          | map >> sum_by(it * it)
          | unwrap >> as_list
    )

    print(result)  # [14, 29]

The syntax ``curried_func >> arg`` is equivalent to ``curried_func(arg)``.

Keyword Arguments
-----------------

Arguments can generally be referred to by their keywords in any order with one exception.

Given the following curried function::

    @curry
    def foo(x, y, z):
        return x + y + z

This function could be called in numerous ways::

    print(foo("a", "b", "c"))
    print(foo("a")("b")("c"))
    print(foo >> "a" >> "b" >> "c")
    print(foo("a") >> "b" >> "c")
    print(foo(x="a") >> "b" >> "c")
    print(foo(x="a")("b") >> "c")
    print(foo("a", y="b") >> "c")
    print(foo(y="b")("a")("c"))
    print(foo(y="b", z="c")("a"))
    print(foo(y="b", z="c")(x="a"))
    print(foo(y="b")("a")(z="c"))

All of the above function calls print ``"abc"``.

The ony exception is default arguments. Default arguments can only be overriden
in the first call to the curried function::

    @curry
    def foo(x, y, z="X"):
        return x + y + z

    # Works:
    print(foo(z="c")("a", "b"))
    print(foo("a", z="c")("b"))

    # Uses Default
    print(foo("a")("b"))

    # Does NOT work:
    print(foo("a", "b")(z="c"))

The last case does not work because after the call to ``foo("a", "b")``, the
function is evaluated using the default parameter.
