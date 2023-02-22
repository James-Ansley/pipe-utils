import operator
from io import StringIO

from pytest import raises

from pipe_utils import Pipe
from pipe_utils.pipe import Then


def test_pipe_yields_data():
    assert Pipe(5).get() == 5
    assert Pipe([1, 2, 3]).get_or_default([2, 4, 8]) == [1, 2, 3]
    assert Pipe("Hello").get_or_raise(ValueError) == "Hello"


def test_pipe_then_yield():
    assert Pipe(5).then(str).get() == "5"
    assert Pipe("Hello").then(len).get_or_default(-1) == 5
    assert Pipe([3, 2, 1]).then(sorted).get_or_raise(ValueError) == [1, 2, 3]


def test_pipe_is_immutable():
    p1 = Pipe("Hello")
    p2 = p1.then(len)
    assert p1.get() == "Hello"
    assert p2.get() == 5


def test_pipe_or():
    assert (Pipe("Hello") | len).get() == 5
    assert (Pipe(5) | str).get() == "5"
    assert (Pipe([3, 2, 1]) | sorted).get() == [1, 2, 3]
    assert (
                   Pipe("Hello")
                   | list
                   | (lambda data: map(lambda c: c * 2, data))
                   | "".join
           ).get() == "HHeelllloo"
    assert (
                   Pipe(1)
                   | (operator.add, 5)
                   | (operator.mul, 2)
           ).get() == 12


def test_err_is_caught():
    pipe = (
            Pipe([-1, 0, 1])
            | (lambda data: map(lambda x: 1 / x, data))
            | list
    )
    assert pipe.get_or_default(-1) == -1

    with raises(ZeroDivisionError):
        pipe.get()
    with raises(TypeError) as e:
        pipe.get_or_raise(TypeError("Oops!!"))
    assert "Oops!!" in str(e.value)


def test_args():
    stream = StringIO()
    Pipe("Hello") | Then(print, end=", World", file=stream)
    assert stream.getvalue() == "Hello, World"

    stream = StringIO()
    Pipe("one") | Then(print, "two", end="-three", sep="-", file=stream)
    assert stream.getvalue() == "one-two-three"


def test_catch():
    assert (Pipe([-1, 0, 1])
            .then(lambda data: map(lambda x: 1 / x, data))
            .then(list)
            .catch(ZeroDivisionError, lambda _: [0])
            ).get() == [0]
    with raises(ZeroDivisionError):
        (
            Pipe([-1, 0, 1])
            .then(lambda data: map(lambda x: 1 / x, data))
            .then(list)
            .catch(TypeError, lambda _: [0])
        ).get()


def test_pipe_err_state_is_chained():
    assert (
        Pipe(1)
        | (operator.truediv, 0)
        | (operator.add, 1)
        | Then(print, end="")
    ).get_or_default("Oops!") == "Oops!"


def test_pipe_with_non_function():
    with raises(ValueError):
        Pipe([]) | 4
