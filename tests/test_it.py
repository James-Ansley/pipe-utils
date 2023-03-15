from collections import Counter
from fractions import Fraction

from pipe_utils.override import *


def test_it_lt():
    assert (it < 5)(0)
    assert not (it < 5)(5)
    assert not (it < 5)(10)


def test_it_le():
    assert (it <= 5)(0)
    assert (it <= 5)(5)
    assert not (it <= 5)(6)


def test_it_eq():
    assert (it == 5)(5)
    assert not (it == 5)(0)
    assert not (it == 5)(10)


def test_it_ne():
    assert not (it != 5)(5)
    assert (it != 5)(0)
    assert (it != 5)(10)


def test_it_gt():
    assert not (it > 5)(0)
    assert not (it > 5)(5)
    assert (it > 5)(10)


def test_it_ge():
    assert not (it >= 5)(0)
    assert (it >= 5)(5)
    assert (it >= 5)(6)


def test_it_abs():
    assert abs(it)(-5) == 5
    assert abs(it)(-10) == 10
    assert abs(it)(10) == 10
    assert abs(it)(0) == 0


def test_it_pos():
    c = Counter({1: 3, 2: 0, 3: -5})
    assert (+it)(c) == Counter([1, 1, 1])


def test_it_neg():
    assert (-it)(5) == -5
    assert (-it)(-5) == 5


def test_it_add():
    assert (it + 5)(0) == 5
    assert (it + 5)(1) == 6


def test_it_floordiv():
    assert (it // 2)(4) == 2.0
    assert (it // 2)(5) == 2.0


def test_it_matmul():
    class X:
        def __init__(self, data):
            self.data = data

        def __matmul__(self, other):
            return self.data + other

    assert (it @ 2)((X(0))) == 2
    assert (it @ 2)((X(1))) == 3
    assert (it @ -1)((X(1))) == 0


def test_it_mod():
    assert (it % 2)(0) == 0
    assert (it % 2)(2) == 0
    assert (it % 2)(1) == 1
    assert (it % 2)(3) == 1
    assert (it % 5)(6) == 1


def test_it_mul():
    assert (it * 1)(1) == 1
    assert (it * 1)(-1) == -1
    assert (it * -1)(1) == -1
    assert (it * Fraction(1, 2))(Fraction(1, 2)) == Fraction(1, 4)
    assert (it * 2)("a") == "aa"


def test_it_pow():
    assert (it ** 2)(2) == 4
    assert (it ** 0)(2) == 1
    assert (it ** 1)(0) == 0
    assert (it ** 1)(1) == 1
    assert (it ** 0.5)(4) == 2.0


def test_it_sub():
    assert (it - 1)(1) == 0
    assert (it - 1)(-1) == -2
    assert (it - -1)(1) == 2
    assert (it - Fraction(1, 2))(Fraction(1, 2)) == Fraction(0, 1)


def test_it_div():
    assert (it / 1)(1) == 1.0
    assert (it / 1)(-1) == -1.0
    assert (it / -1)(1) == -1.0
    assert (it / 2)(10) == 5.0
    assert (it / Fraction(1, 2))(Fraction(1, 2)) == Fraction(1, 1)


def test_it_or():
    assert (it | 0b0101)(0b1010) == 0b1111
    assert (it | 0b1010)(0b1010) == 0b1010
    assert (it | 0b00)(0b11) == 0b11
    assert (it | 0b11)(0b11) == 0b11


def test_it_and():
    assert (it & 0b0101)(0b1010) == 0b0000
    assert (it & 0b1010)(0b1010) == 0b1010
    assert (it & 0b00)(0b11) == 0b00
    assert (it & 0b11)(0b11) == 0b11


def test_it_invert():
    assert (~it)(1) == -2
    assert (~it)(10) == -11


def test_it_lshift():
    assert (it << 1)(2) == 4
    assert (it << 1)(4) == 8
    assert (it << 2)(8) == 32


def test_it_rshift():
    assert (it >> 1)(2) == 1
    assert (it >> 1)(4) == 2
    assert (it >> 2)(8) == 2


def test_it_xor():
    assert (it ^ 0b0101)(0b1010) == 0b1111
    assert (it ^ 0b1010)(0b1010) == 0b0000
    assert (it ^ 0b00)(0b11) == 0b11
    assert (it ^ 0b11)(0b11) == 0b00


def test_it_getitem():
    assert (it[1])([1, 2, 3]) == 2
    assert (it[1])({1: "a", 2: "b"}) == "a"


def test_it_radd():
    assert (5 + it)(0) == 5
    assert (5 + it)(1) == 6


def test_it_rfloordiv():
    assert (4 // it)(2) == 2.0
    assert (5 // it)(2) == 2.0


def test_it_rmatmul():
    class X:
        def __init__(self, data):
            self.data = data

        def __rmatmul__(self, other):
            return self.data + other

    assert (2 @ it)((X(0))) == 2
    assert (2 @ it)((X(1))) == 3
    assert (-1 @ it)((X(1))) == 0


def test_it_rmod():
    assert (0 % it)(2) == 0
    assert (2 % it)(2) == 0
    assert (1 % it)(2) == 1
    assert (3 % it)(2) == 1
    assert (6 % it)(5) == 1


def test_it_rmul():
    assert (1 * it)(1) == 1
    assert (-1 * it)(1) == -1
    assert (1 * it)(-1) == -1
    assert (Fraction(1, 2) * it)(Fraction(1, 2)) == Fraction(1, 4)
    assert ("a" * it)(2) == "aa"


def test_it_rpow():
    assert (2 ** it)(2) == 4
    assert (2 ** it)(0) == 1
    assert (0 ** it)(1) == 0
    assert (1 ** it)(1) == 1
    assert (4 ** it)(0.5) == 2.0


def test_it_rsub():
    assert (1 - it)(1) == 0
    assert (-1 - it)(1) == -2
    assert (1 - it)(-1) == 2
    assert (Fraction(1, 2) - it)(Fraction(1, 2)) == Fraction(0, 1)


def test_it_rdiv():
    assert (1 / it)(1) == 1.0
    assert (-1 / it)(1) == -1.0
    assert (1 / it)(-1) == -1.0
    assert (10 / it)(2) == 5.0
    assert (Fraction(1, 2) / it)(Fraction(1, 2)) == Fraction(1, 1)


def test_it_ror():
    assert (0b0101 | it)(0b1010) == 0b1111
    assert (0b1010 | it)(0b1010) == 0b1010
    assert (0b00 | it)(0b11) == 0b11
    assert (0b11 | it)(0b11) == 0b11


def test_it_rand():
    assert (0b0101 & it)(0b1010) == 0b0000
    assert (0b1010 & it)(0b1010) == 0b1010
    assert (0b00 & it)(0b11) == 0b00
    assert (0b11 & it)(0b11) == 0b11


def test_it_rlshift():
    assert (2 << it)(1) == 4
    assert (4 << it)(1) == 8
    assert (8 << it)(2) == 32


def test_it_rrshift():
    assert (2 >> it)(1) == 1
    assert (4 >> it)(1) == 2
    assert (8 >> it)(2) == 2


def test_it_rxor():
    assert (0b0101 ^ it)(0b1010) == 0b1111
    assert (0b1010 ^ it)(0b1010) == 0b0000
    assert (0b00 ^ it)(0b11) == 0b11
    assert (0b11 ^ it)(0b11) == 0b00


def test_it_divmod():
    assert divmod(it, 5)(7) == (1, 2)


def test_it_rdivmod():
    assert divmod(7, it)(5) == (1, 2)
