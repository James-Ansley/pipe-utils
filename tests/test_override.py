from pytest import raises

from pipe_utils.override import *


def test_override_all():
    assert (Pipe(range(0, 11, 2)) | all(is_even)).get() is True
    assert (Pipe([]) | all(is_even)).get() is True
    assert (Pipe(range(1, 11, 2)) | all(is_even)).get() is False


def test_override_any():
    assert (Pipe([-1, 0, 1]) | any(lambda x: x == 0)).get() is True
    assert (Pipe([-1, 0, 1]) | any(lambda x: x == 2)).get() is False
    assert (Pipe([]) | any(lambda x: x == 2)).get() is False


def test_override_filter():
    assert (Pipe([]) | filter(is_even) | list).get() == []
    pipe = Pipe(range(11)) | filter(is_even) | list
    assert pipe.get() == [0, 2, 4, 6, 8, 10]


def test_map():
    pipe = Pipe(range(11)) | filter(is_even) | map(lambda e: e * 2) | list
    assert pipe.get() == [0, 4, 8, 12, 16, 20]
    pipe = Pipe([[3, 2, 1], [6, 5, 4]]) | map(sorted) | list
    assert pipe.get() == [[1, 2, 3], [4, 5, 6]]


def test_override_slice():
    assert (Pipe([]) | slice(10) | list).get() == []
    assert (Pipe([]) | slice(0, 10, 2) | list).get() == []
    assert (Pipe([1, 2, 3, 4]) | slice(2) | list).get() == [1, 2]
    assert (Pipe([1, 2, 3, 4]) | slice(1, 3) | list).get() == [2, 3]
    assert (Pipe([1, 2, 3, 4]) | slice(0, 4, 2) | list).get() == [1, 3]


def test_not():
    assert Not(is_even)(5)
    assert not Not(is_even)(4)


def test_or():
    assert Or(is_even, it > 4)(2)
    assert Or(is_even, it > 4)(5)
    assert not Or(is_even, it > 4)(1)


def test_and():
    assert And(it % 2 == 0, it > 4)(10)
    assert not And(it % 2 == 0, it > 4)(2)
    assert not And(it % 2 == 0, it > 4)(5)
    assert not And(it % 2 == 0, it > 4)(1)


def test_is():
    a, b = object(), object()
    assert Is(a)(a)
    assert Is(None)(None)
    assert not Is(a)(b)
    assert not Is(None)(b)
    assert not Is(a)(None)
    assert not Is([1, 2])([1, 2])


def test_is_not():
    a, b = object(), object()
    assert not IsNot(a)(a)
    assert not IsNot(None)(None)
    assert IsNot(a)(b)
    assert IsNot(None)(b)
    assert IsNot(a)(None)
    assert IsNot([1, 2])([1, 2])


def test_raise():
    with raises(ZeroDivisionError):
        Raise(ZeroDivisionError())
    with raises(ZeroDivisionError):
        Raise(ZeroDivisionError)
    with raises(ValueError) as e:
        Raise(ValueError("Uh oh!"), from_=TypeError("Oops!"))
    assert str(e.value) == "Uh oh!"
    assert isinstance(e.value.__cause__, TypeError)
    assert str(e.value.__cause__) == "Oops!"
