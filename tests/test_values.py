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


def test_is_none():
    assert is_none(None)
    assert not is_none([])


def test_is_not_none():
    assert not is_not_none(None)
    assert is_not_none([])


def test_add_by():
    assert add_by(1)(1) == 2
    assert add_by(1)(-1) == 0
    assert add_by(-1)(1) == 0
    assert add_by(Fraction(1, 2))(Fraction(1, 2)) == Fraction(1, 1)


def test_sub_by():
    assert sub_by(1)(1) == 0
    assert sub_by(1)(-1) == -2
    assert sub_by(-1)(1) == 2
    assert sub_by(Fraction(1, 2))(Fraction(1, 2)) == Fraction(0, 1)


def test_mul_by():
    assert mul_by(1)(1) == 1
    assert mul_by(1)(-1) == -1
    assert mul_by(-1)(1) == -1
    assert mul_by(Fraction(1, 2))(Fraction(1, 2)) == Fraction(1, 4)

    assert mul_by(2)("a") == "aa"


def test_div_by():
    assert div_by(1)(1) == 1.0
    assert div_by(1)(-1) == -1.0
    assert div_by(-1)(1) == -1.0
    assert div_by(2)(10) == 5.0
    assert div_by(Fraction(1, 2))(Fraction(1, 2)) == Fraction(1, 1)


def test_fdiv_by():
    assert fdiv_by(1)(1) == 1
    assert fdiv_by(1)(-1) == -1
    assert fdiv_by(-1)(1) == -1
    assert fdiv_by(2)(10) == 5
    assert fdiv_by(Fraction(1, 2))(Fraction(1, 2)) == Fraction(1, 1)
    assert fdiv_by(Fraction(2, 1))(Fraction(1, 1)) == Fraction(0, 1)


def test_mod_by():
    assert mod_by(2)(0) == 0
    assert mod_by(2)(2) == 0
    assert mod_by(2)(1) == 1
    assert mod_by(2)(3) == 1
    assert mod_by(5)(6) == 1


def test_to_power():
    assert to_power(2)(2) == 4
    assert to_power(0)(2) == 1
    assert to_power(1)(0) == 0
    assert to_power(1)(1) == 1
    assert to_power(0.5)(4) == 2.0


def test_eq():
    assert eq(5)(5)
    assert not eq(5)(4)
    assert eq([1, 2])([1, 2])
    assert not eq([1, 2])([1, 2, 3])


def test_ne():
    assert ne(5)(4)
    assert ne([1, 2])([1, 2, 3])
    assert not ne(5)(5)
    assert not ne([1, 2])([1, 2])


def test_lt():
    assert lt(6)(5)
    assert not lt(3)(4)
    assert not lt(3)(3)
    assert lt("b")("a")
    assert not lt("a")("b")


def test_gt():
    assert gt(5)(6)
    assert not gt(5)(5)
    assert not gt(5)(4)
    assert gt("a")("b")
    assert not gt("b")("a")


def test_le():
    assert le(6)(5)
    assert not le(3)(4)
    assert le(3)(3)
    assert le("b")("a")
    assert not le("a")("b")
    assert le("a")("a")


def test_ge():
    assert ge(5)(6)
    assert ge(5)(5)
    assert not ge(5)(4)
    assert ge("a")("b")
    assert not ge("b")("a")
    assert ge("a")("a")


def test_it_is():
    a, b = object(), object()
    assert it_is(a)(a)
    assert it_is(None)(None)
    assert not it_is(a)(b)
    assert not it_is(None)(b)
    assert not it_is(a)(None)
    assert not it_is([1, 2])([1, 2])


def test_it_is_not():
    a, b = object(), object()
    assert not it_is_not(a)(a)
    assert not it_is_not(None)(None)
    assert it_is_not(a)(b)
    assert it_is_not(None)(b)
    assert it_is_not(a)(None)
    assert it_is_not([1, 2])([1, 2])


def test_bit_and():
    assert bit_and(0b0101)(0b1010) == 0b0000
    assert bit_and(0b1010)(0b1010) == 0b1010
    assert bit_and(0b00)(0b11) == 0b00
    assert bit_and(0b11)(0b11) == 0b11


def test_bit_or():
    assert bit_or(0b0101)(0b1010) == 0b1111
    assert bit_or(0b1010)(0b1010) == 0b1010
    assert bit_or(0b00)(0b11) == 0b11
    assert bit_or(0b11)(0b11) == 0b11


def test_bit_xor():
    assert bit_xor(0b0101)(0b1010) == 0b1111
    assert bit_xor(0b1010)(0b1010) == 0b0000
    assert bit_xor(0b00)(0b11) == 0b11
    assert bit_xor(0b11)(0b11) == 0b00


def test_rshift():
    assert rshift(1)(2) == 1
    assert rshift(1)(4) == 2
    assert rshift(2)(8) == 2


def test_lshift():
    assert lshift(1)(2) == 4
    assert lshift(1)(4) == 8
    assert lshift(2)(8) == 32
