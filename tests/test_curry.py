import pytest

from pipe_utils import curry


def foo(x, y, z):
    return x + y + z


def default_foo(x, y, z="X"):
    return x + y + z


def bar(a, b, *args):
    return a + b + sum(args)


def baz(a, b, **kwargs):
    return a + b + sum(kwargs.values())


def test_functions_can_curry():
    curry_foo = curry(foo)
    assert curry_foo(1)(2)(3) == 6
    assert curry_foo("a")("b")("c") == "abc"
    assert curry_foo(z="a")("b")("c") == "bca"
    assert curry_foo(y="a", z="b")("c") == "cab"
    assert curry_foo(y="a", z="b", x="c") == "cab"
    assert curry_foo(x="a")(y="b")("c") == "abc"
    assert curry_foo(y="a")(x="b")("c") == "bac"
    assert curry_foo(y="a")("b")(z="c") == "bac"


def test_kwargs_can_only_be_defined_once():
    curry_foo = curry(default_foo)
    assert curry_foo("a")("b") == "abX"
    assert curry_foo(z="c")("a")("b") == "abc"
    with pytest.raises(TypeError):
        curry_foo(z="c")(x="a")(x="b")("d")
    with pytest.raises(TypeError):
        curry_foo("a")("b")("c")


def test_var_args_cant_curry():
    with pytest.raises(TypeError):
        curry(bar)


def test_var_kwargs_can_curry():
    curry_baz = curry(baz)
    assert curry_baz(i=1, j=1)(1, 1) == 4
    assert curry_baz(1, 1, i=1, j=1) == 4
    assert curry_baz(a=1, i=1, j=1)(1) == 4
