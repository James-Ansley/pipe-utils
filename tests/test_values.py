from fractions import Fraction

from pipe_utils.values import *


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


def test_is_non_negative():
    assert is_non_negative(2)
    assert is_non_negative(0)
    assert is_non_negative(-0)
    assert is_non_negative(0.0)
    assert is_non_negative(-0.0)
    assert not is_non_negative(-1)
    assert not is_non_negative(-10)

    assert is_non_negative(Fraction(1, 1))
    assert not is_non_negative(Fraction(-1, 1))


def test_is_non_positive():
    assert is_non_positive(-2)
    assert is_non_positive(-1)
    assert is_non_positive(0)
    assert is_non_positive(-0)
    assert is_non_positive(0.0)
    assert is_non_positive(-0.0)
    assert not is_non_positive(1)
    assert not is_non_positive(10)

    assert is_non_positive(Fraction(-1, 1))
    assert not is_non_positive(Fraction(1, 1))
