import pytest

from pipe_utils import it
from pipe_utils.values import *


def test_not():
    assert not_(is_even)(5)
    assert not not_(is_even)(4)


def test_or():
    assert or_(is_even, it > 4)(2)
    assert or_(is_even, it > 4)(5)
    assert not or_(is_even, it > 4)(1)


def test_and():
    assert and_(it % 2 == 0, it > 4)(10)
    assert not and_(it % 2 == 0, it > 4)(2)
    assert not and_(it % 2 == 0, it > 4)(5)
    assert not and_(it % 2 == 0, it > 4)(1)


def test_is_even():
    assert is_even(-2)
    assert not is_even(-1)
    assert is_even(0)
    assert not is_even(1)
    assert is_even(2)
    assert not is_even(3)


def test_is_odd():
    assert not is_odd(-2)
    assert is_odd(-1)
    assert not is_odd(0)
    assert is_odd(1)
    assert not is_odd(2)
    assert is_odd(3)


def test_is_congruent():
    assert is_congruent(3, 12)(15)
    assert is_congruent(12, 12)(24)
    assert is_congruent(1, 12)(13)
    assert not is_congruent(1, 12)(14)

    assert is_congruent(-4, 5)(1)
    assert is_congruent(-1, 5)(4)


def test_clamp():
    assert clamp(0, 10)(5) == 5
    assert clamp(0, 10)(20) == 10
    assert clamp(0, 10)(-20) == 0
    assert clamp(0, 10)(0) == 0
    assert clamp(0, 10)(10) == 10


def test_lclamp():
    assert lclamp(0)(5) == 5
    assert lclamp(20)(10) == 20
    assert lclamp(0)(-20) == 0
    assert lclamp(0)(0) == 0
    assert lclamp(10)(10) == 10


def test_rclamp():
    assert rclamp(10)(5) == 5
    assert rclamp(10)(20) == 10
    assert rclamp(0)(20) == 0
    assert rclamp(0)(0) == 0
    assert rclamp(10)(10) == 10


def test_is_none():
    assert is_none(None)
    assert not is_none([])


def test_is_not_none():
    assert not is_not_none(None)
    assert is_not_none([])


def test_raise():
    with pytest.raises(ZeroDivisionError):
        raise_(ZeroDivisionError())
    with pytest.raises(ZeroDivisionError) as e:
        raise_(ZeroDivisionError)
    assert e.value.__cause__ is None
    with pytest.raises(ValueError) as e:
        raise_(ValueError("Uh oh!"), from_=TypeError("Oops!"))
    assert str(e.value) == "Uh oh!"
    assert isinstance(e.value.__cause__, TypeError)
    assert str(e.value.__cause__) == "Oops!"

    with pytest.raises(ValueError) as e:
        try:
            1 / 0
        except ZeroDivisionError:
            raise_(ValueError("Oops!"), from_=None)
    assert e.value.__suppress_context__ is True
    assert e.value.__cause__ is None
    assert str(e.value) == "Oops!"


def test_raises():
    with pytest.raises(ZeroDivisionError):
        raises(ZeroDivisionError())()
    with pytest.raises(ZeroDivisionError) as e:
        raises(ZeroDivisionError)("Hello", key="Some Args")
    assert e.value.__cause__ is None
    with pytest.raises(ValueError) as e:
        raises(ValueError("Uh oh!"), from_=TypeError("Oops!"))(...)
    assert str(e.value) == "Uh oh!"
    assert isinstance(e.value.__cause__, TypeError)
    assert str(e.value.__cause__) == "Oops!"

    with pytest.raises(ValueError) as e:
        try:
            1 / 0
        except ZeroDivisionError:
            raises(ValueError("Oops!"), from_=None)(raises)
    assert e.value.__suppress_context__ is True
    assert e.value.__cause__ is None
    assert str(e.value) == "Oops!"


def test_is():
    a, b = object(), object()
    assert is_(a)(a)
    assert is_(None)(None)
    assert not is_(a)(b)
    assert not is_(None)(b)
    assert not is_(a)(None)
    assert not is_([1, 2])([1, 2])


def test_is_not():
    a, b = object(), object()
    assert not is_not(a)(a)
    assert not is_not(None)(None)
    assert is_not(a)(b)
    assert is_not(None)(b)
    assert is_not(a)(None)
    assert is_not([1, 2])([1, 2])
