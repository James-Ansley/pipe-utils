from fractions import Fraction
from io import StringIO
from operator import add

from pytest import raises

from pipe_utils import Pipe
from pipe_utils.iterables import *


def is_even(e):
    return e % 2 == 0


def test_all():
    assert (Pipe(range(0, 11, 2)) | all_(is_even)).get() is True
    assert (Pipe([]) | all_(is_even)).get() is True
    assert (Pipe(range(1, 11, 2)) | all_(is_even)).get() is False


def test_any():
    assert (Pipe([-1, 0, 1]) | any_(lambda x: x == 0)).get() is True
    assert (Pipe([-1, 0, 1]) | any_(lambda x: x == 2)).get() is False
    assert (Pipe([]) | any_(lambda x: x == 2)).get() is False


def test_associate():
    assert (Pipe([]) | associate(lambda e: (e, e))).get() == {}

    pipe = (Pipe(["A", "Ab"])
            | associate(lambda s: (s.lower(), s.upper())))
    assert dict(pipe.get()) == {"a": "A", "ab": "AB"}

    pipe = (Pipe(["ab", "cd"])
            | associate(lambda s: (len(s), s)))
    assert dict(pipe.get()) == {2: "cd"}


def test_associate_with():
    assert (Pipe([]) | associate_with(len)).get() == {}

    pipe = (Pipe(["a", "ab", "abc"]) | associate_with(len))
    assert dict(pipe.get()) == {"a": 1, "ab": 2, "abc": 3}

    pipe = (Pipe(["a", "ab", "a"]) | associate_with(len))
    assert dict(pipe.get()) == {"a": 1, "ab": 2}


def test_chunked():
    assert (Pipe([]) | chunked(3) | list).get() == []
    pipe = (
            Pipe(range(9))
            | chunked(3)
            | map_(list)
            | list
    )
    assert pipe.get() == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    with raises(ValueError):
        Pipe([]) | chunked(0)
    with raises(ValueError):
        Pipe([]) | chunked(-1)


def test_concat():
    assert (Pipe([]) | concat([]) | list).get() == []
    assert (Pipe(["a"]) | concat([]) | list).get() == ["a"]
    assert (Pipe([]) | concat(["b"]) | list).get() == ["b"]
    assert (Pipe(["a"]) | concat(["b"]) | list).get() == ["a", "b"]
    pipe = (Pipe(["a", "b", "c"])
            | concat(["d", "e", "f"])
            | list)
    assert pipe.get() == list("abcdef")


def test_concat_after():
    assert (Pipe([]) | concat_after([]) | list).get() == []
    assert (Pipe(["a"]) | concat_after([]) | list).get() == ["a"]
    assert (Pipe([]) | concat_after(["b"]) | list).get() == ["b"]
    assert (Pipe(["a"]) | concat_after(["b"]) | list).get() == ["b", "a"]
    pipe = (Pipe(["a", "b", "c"])
            | concat_after(["d", "e", "f"])
            | list)
    assert pipe.get() == list("defabc")


def test_contains():
    assert (Pipe([]) | contains(0)).get() is False
    assert (Pipe([-1, 1]) | contains(0)).get() is False
    assert (Pipe([-1, 0, 1]) | contains(0)).get() is True
    assert (Pipe([-1]) | concat([0]) | contains(0)).get() is True


def test_contains_all():
    assert (Pipe([]) | contains_all([0])).get() is False
    assert (Pipe([-1, 1]) | contains_all([0, 1])).get() is False
    assert (Pipe([-1, 0, 1]) | contains_all([0, -1])).get() is True
    assert (Pipe([-1]) | concat([0]) | contains_all([-1, 0])).get() is True


def test_count():
    assert (Pipe([]) | count(0)).get() == 0
    assert (Pipe([-1, 1]) | count(0)).get() == 0
    assert (Pipe([-1, 0, 1]) | count(0)).get() == 1
    assert (Pipe([-1, 0, 1, 0, 0]) | count(0)).get() == 3


def test_distinct():
    assert (Pipe([]) | distinct | list).get() == []
    assert (Pipe([1, 2, 3]) | distinct | list).get() == [1, 2, 3]
    assert (Pipe([1, 2, 1, 3, 2]) | distinct | list).get() == [1, 2, 3]
    assert (Pipe([1, 1, 1, 1]) | distinct | list).get() == [1]


def test_distinct_by():
    assert (Pipe([]) | distinct_by(len) | list).get() == []
    pipe = (Pipe(["a", "b", "ab"]) | distinct_by(len) | list)
    assert pipe.get() == ["a", "ab"]
    pipe = (Pipe(["a", "ab", "b", "c", "bc"]) | distinct_by(len) | list)
    assert pipe.get() == ["a", "ab"]


def test_drop():
    assert (Pipe([]) | drop(5) | list).get() == []
    assert (Pipe([]) | drop(0) | list).get() == []
    assert (Pipe([1]) | drop(0) | list).get() == [1]
    assert (Pipe([1]) | drop(1) | list).get() == []
    assert (Pipe([1]) | drop(2) | list).get() == []
    assert (Pipe([1, 2, 3]) | drop(0) | list).get() == [1, 2, 3]
    assert (Pipe([1, 2, 3]) | drop(1) | list).get() == [2, 3]
    assert (Pipe([1, 2, 3]) | drop(2) | list).get() == [3]
    assert (Pipe([1, 2, 3]) | drop(3) | list).get() == []
    assert (Pipe([1, 2, 3]) | drop(4) | list).get() == []

    with raises(ValueError):
        Pipe([]) | drop(-1)


def test_drop_last():
    assert (Pipe([]) | drop_last(5) | list).get() == []
    assert (Pipe([]) | drop_last(0) | list).get() == []
    assert (Pipe([1]) | drop_last(0) | list).get() == [1]
    assert (Pipe([1]) | drop_last(1) | list).get() == []
    assert (Pipe([1]) | drop_last(2) | list).get() == []
    assert (Pipe([1, 2, 3]) | drop_last(0) | list).get() == [1, 2, 3]
    assert (Pipe([1, 2, 3]) | drop_last(1) | list).get() == [1, 2]
    assert (Pipe([1, 2, 3]) | drop_last(2) | list).get() == [1]
    assert (Pipe([1, 2, 3]) | drop_last(3) | list).get() == []
    assert (Pipe([1, 2, 3]) | drop_last(4) | list).get() == []

    with raises(ValueError):
        Pipe([]) | drop_last(-1)


def test_drop_last_while():
    assert (Pipe([]) | drop_last_while(is_even) | list).get() == []
    assert (Pipe([0, 1, 2]) | drop_last_while(is_even) | list).get() == [0, 1]
    pipe = (Pipe([1, 2, 3]) | drop_last_while(is_even) | list)
    assert pipe.get() == [1, 2, 3]
    assert (Pipe([0, 0, 0]) | drop_last_while(is_even) | list).get() == []
    pipe = (Pipe([1, 2, 3, 4, 6, 8]) | drop_last_while(is_even) | list)
    assert pipe.get() == [1, 2, 3]


def test_drop_while():
    assert (Pipe([]) | drop_while(is_even) | list).get() == []
    assert (Pipe([0, 1, 2]) | drop_while(is_even) | list).get() == [1, 2]
    assert (Pipe([1, 2, 3]) | drop_while(is_even) | list).get() == [1, 2, 3]
    assert (Pipe([0, 0, 0]) | drop_while(is_even) | list).get() == []


def test_filter():
    assert (Pipe([]) | filter_(is_even) | list).get() == []
    pipe = Pipe(range(11)) | filter_(is_even) | list
    assert pipe.get() == [0, 2, 4, 6, 8, 10]


def test_filter_false():
    assert (Pipe([]) | filter_false(is_even) | list).get() == []
    assert (Pipe([-1, 0, 1]) | filter_false(is_even) | list).get() == [-1, 1]
    pipe = (Pipe(range(11)) | filter_false(is_even) | list)
    assert pipe.get() == [1, 3, 5, 7, 9]


def test_find():
    assert (Pipe([]) | find(is_even)).get() is None
    assert (Pipe([1, 2, 3, 4]) | find(is_even)).get() == 2
    assert (Pipe([1, 3, 5, 7]) | find(is_even)).get() is None


def test_find_last():
    assert (Pipe([]) | find_last(is_even)).get() is None
    assert (Pipe([1, 2, 3, 4, 5]) | find_last(is_even)).get() == 4
    assert (Pipe([1, 3, 5, 7]) | find_last(is_even)).get() is None


def test_first():
    assert (Pipe([]) | first() | list).get() == []
    assert (Pipe([]) | first(5) | list).get() == []
    assert (Pipe([1, 2, 3]) | first() | list).get() == [1]
    assert (Pipe([1, 2, 3]) | first(2) | list).get() == [1, 2]
    assert (Pipe([1, 2, 3]) | first(3) | list).get() == [1, 2, 3]
    assert (Pipe([1, 2, 3]) | first(4) | list).get() == [1, 2, 3]

    with raises(ValueError):
        Pipe([]) | first(-1)


def test_flatten():
    assert (Pipe([]) | flatten | list).get() == []
    assert (Pipe([[1]]) | flatten | list).get() == [1]
    assert (Pipe([[1], [2]]) | flatten | list).get() == [1, 2]
    assert (Pipe([[1, 2], [3]]) | flatten | list).get() == [1, 2, 3]
    assert (Pipe([[[1, 2]], [[3]]]) | flatten | list).get() == [[1, 2], [3]]


def test_flat_map():
    assert (Pipe([]) | flat_map(list) | list).get() == []
    assert (Pipe(["a"]) | flat_map(list) | list).get() == ["a"]
    assert (Pipe(["ab", "cd"]) | flat_map(list) | list).get() == list("abcd")


def test_fold():
    assert (Pipe([]) | fold(1, add)).get() == 1
    assert (Pipe([1]) | fold(1, add)).get() == 2
    assert (Pipe([1, 2, 3]) | fold(1, add)).get() == 7


# noinspection PyShadowingNames,PyDefaultArgument
def test_for_each():
    res = []
    Pipe([]) | for_each(lambda e, res=res: res.append(e))
    assert res == []
    res = []
    Pipe([1, 2, 3]) | for_each(lambda e, res=res: res.append(e))
    assert res == [1, 2, 3]


def test_group_by():
    assert (Pipe([]) | group_by(len) | dict).get() == {}
    assert (Pipe(["a"]) | group_by(len) | dict).get() == {1: ["a"]}
    pipe = (Pipe(["a", "b", "ab"]) | group_by(len) | dict)
    assert pipe.get() == {1: ["a", "b"], 2: ["ab"]}


def test_get():
    assert (Pipe(["a"]) | get(0)).get() == "a"
    assert (Pipe("abc") | get(1)).get() == "b"

    with raises(IndexError):
        (Pipe("abc") | get(3)).get()
    with raises(IndexError):
        (Pipe("abc") | get(-1)).get()


def test_get_or_default():
    assert (Pipe(["a"]) | get_or_default(0, "")).get() == "a"
    assert (Pipe("abc") | get_or_default(1, "")).get() == "b"
    assert (Pipe("abc") | get_or_default(3, "")).get() == ""
    assert (Pipe("abc") | get_or_default(-1, "")).get() == ""


def test_is_empty():
    assert (Pipe([]) | is_empty).get() is True
    assert (Pipe([1]) | is_empty).get() is False
    assert (Pipe([1, 2]) | is_empty).get() is False


def test_is_not_empty():
    assert (Pipe([]) | is_not_empty).get() is False
    assert (Pipe([1]) | is_not_empty).get() is True
    assert (Pipe([1, 2]) | is_not_empty).get() is True


def test_index_of():
    assert (Pipe(["a"]) | index_of("a")).get() == 0
    assert (Pipe(["a", "b"]) | index_of("b")).get() == 1
    assert (Pipe(["a", "b", "a"]) | index_of("a")).get() == 0
    with raises(IndexError):
        (Pipe(["a", "b", "a"]) | index_of("c")).get()


def test_index_of_last():
    assert (Pipe(["a"]) | index_of_last("a")).get() == 0
    assert (Pipe(["a", "b"]) | index_of_last("b")).get() == 1
    assert (Pipe(["a", "b", "a", "c"]) | index_of_last("a")).get() == 2
    with raises(IndexError):
        (Pipe(["a", "b", "a"]) | index_of_last("c")).get()


def test_join_to_str():
    joiner = join_to_str(sep="-", prefix="~", suffix="`")
    assert (Pipe([]) | join_to_str()).get() == ""
    assert (Pipe([]) | join_to_str(sep="-")).get() == ""
    assert (Pipe([]) | joiner).get() == "~`"
    assert (Pipe([]) | join_to_str(prefix="~", suffix="`")).get() == "~`"
    assert (Pipe([]) | join_to_str(prefix="~")).get() == "~"
    assert (Pipe([]) | join_to_str(suffix="`")).get() == "`"
    assert (Pipe([1]) | join_to_str()).get() == "1"
    assert (Pipe([1, 2]) | join_to_str()).get() == "12"
    assert (Pipe([1, 2]) | join_to_str(sep="-")).get() == "1-2"
    assert (Pipe([1, 2]) | join_to_str(sep="-", prefix="~")).get() == "~1-2"
    assert (Pipe([1, 2]) | join_to_str(sep="-", suffix="`")).get() == "1-2`"
    assert (Pipe([1, 2]) | joiner).get() == "~1-2`"
    assert (Pipe([1, 2, 3, 4]) | joiner).get() == "~1-2-3-4`"


def test_last():
    assert (Pipe([]) | last() | list).get() == []
    assert (Pipe([]) | last(5) | list).get() == []
    assert (Pipe([1, 2, 3]) | last() | list).get() == [3]
    assert (Pipe([1, 2, 3]) | last(2) | list).get() == [2, 3]
    assert (Pipe([1, 2, 3]) | last(3) | list).get() == [1, 2, 3]
    assert (Pipe([1, 2, 3]) | last(4) | list).get() == [1, 2, 3]

    with raises(ValueError):
        Pipe([]) | last(-1)


def test_map():
    pipe = Pipe(range(11)) | filter_(is_even) | map_(lambda e: e * 2) | list
    assert pipe.get() == [0, 4, 8, 12, 16, 20]
    pipe = Pipe([[3, 2, 1], [6, 5, 4]]) | map_(sorted) | list
    assert pipe.get() == [[1, 2, 3], [4, 5, 6]]


def test_max_by():
    assert (Pipe(["a"]) | max_by(len)).get() == "a"
    assert (Pipe(["a", "b"]) | max_by(len)).get() == "a"
    assert (Pipe(["a", "b", "ab"]) | max_by(len)).get() == "ab"
    assert (Pipe(["a", "b", "ab", "cd"]) | max_by(len)).get() == "ab"


def test_min_by():
    assert (Pipe(["a"]) | min_by(len)).get() == "a"
    assert (Pipe(["a", "b"]) | min_by(len)).get() == "a"
    assert (Pipe(["a", "b", "ab"]) | min_by(len)).get() == "a"
    assert (Pipe(["ab", "cd", "b"]) | min_by(len)).get() == "b"


def test_none():
    assert (Pipe([-1, 0, 1]) | none(lambda x: x == 2)).get() is True
    assert (Pipe([]) | none(lambda x: x == 2)).get() is True
    assert (Pipe([-1, 0, 1]) | none(lambda x: x == 0)).get() is False


def test_partition():
    assert (Pipe([]) | partition(is_even) | map_(list) | list).get() == [[], []]
    pipe = (Pipe([1, 2, 3, 4]) | partition(is_even) | map_(list) | list)
    assert pipe.get() == [[2, 4], [1, 3]]
    pipe = (Pipe([2, 4, 6, 8]) | partition(is_even) | map_(list) | list)
    assert pipe.get() == [[2, 4, 6, 8], []]
    pipe = (Pipe([1, 3, 5, 7]) | partition(is_even) | map_(list) | list)
    assert pipe.get() == [[], [1, 3, 5, 7]]


# noinspection PyShadowingNames,PyDefaultArgument
def test_peek():
    res = []
    pipe = (Pipe([1, 2, 3]) | peek(lambda e, res=res: res.append(e)) | list)
    assert res == [1, 2, 3] and pipe.get() == [1, 2, 3]

    # is lazy
    res = []
    pipe = (Pipe([0, 0, 1, 2])
            | peek(lambda e, res=res: res.append(e))
            | first(2)
            | list)
    assert res == [0, 0] and pipe.get() == [0, 0]


def test_reduce():
    pipe = Pipe(range(11)) | reduce(add)
    assert pipe.get() == sum(range(11))
    pipe = Pipe([1]) | reduce(add)
    assert pipe.get() == 1


def test_remove():
    assert (Pipe([1, 2, 3, 2]) | remove(2) | list).get() == [1, 3, 2]
    assert (Pipe([1, 2, 3, 2]) | remove(4) | list).get() == [1, 2, 3, 2]
    assert (Pipe([]) | remove(4) | list).get() == []
    assert (Pipe([1]) | remove(1) | list).get() == []


def test_remove_last():
    assert (Pipe([1, 2, 3, 2]) | remove_last(2) | list).get() == [1, 2, 3]
    assert (Pipe([1, 2, 3, 2]) | remove_last(3) | list).get() == [1, 2, 2]
    assert (Pipe([1, 2, 3, 2]) | remove_last(1) | list).get() == [2, 3, 2]
    assert (Pipe([1, 2, 3, 2]) | remove_last(4) | list).get() == [1, 2, 3, 2]
    assert (Pipe([]) | remove_last(4) | list).get() == []
    assert (Pipe([1]) | remove_last(1) | list).get() == []


def test_scan():
    assert (Pipe([]) | scan(add) | list).get() == []
    assert (Pipe([1]) | scan(add) | list).get() == [1]
    assert (Pipe([1, 2, 3]) | scan(add) | list).get() == [1, 3, 6]


def test_slice():
    assert (Pipe([]) | slice_(10) | list).get() == []
    assert (Pipe([]) | slice_(0, 10, 2) | list).get() == []
    assert (Pipe([1, 2, 3, 4]) | slice_(2) | list).get() == [1, 2]
    assert (Pipe([1, 2, 3, 4]) | slice_(1, 3) | list).get() == [2, 3]
    assert (Pipe([1, 2, 3, 4]) | slice_(0, 4, 2) | list).get() == [1, 3]


def test_sorted_by():
    assert (Pipe([]) | sorted_by(len)).get() == []
    assert (Pipe(["ab", "a", "b", "cd"])
            | sorted_by(len)).get() == ["a", "b", "ab", "cd"]


def test_sorted_desc():
    assert (Pipe([]) | sorted_by(len)).get() == []
    assert (Pipe(["ab", "a", "b", "cd"])
            | sorted_desc).get() == ["cd", "b", "ab", "a"]


def test_sorted_desc_by():
    assert (Pipe([]) | sorted_desc_by(len)).get() == []
    assert (Pipe(["ab", "a", "b", "cd"])
            | sorted_desc_by(len)).get() == ["ab", "cd", "a", "b"]


def test_starmap():
    assert (Pipe([]) | starmap(pow) | list).get() == []
    pipe = (Pipe([(2, 5), (3, 2), (10, 3)]) | starmap(pow) | list)
    assert pipe.get() == [32, 9, 1000]


def test_starred():
    assert (Pipe([1, 2]) | starred(add)).get() == 3
    stream = StringIO()
    (Pipe([1, 2]) | starred(print, file=stream, sep="~", end="")).get()
    assert stream.getvalue() == "1~2"


def test_take():
    assert (Pipe([]) | take() | list).get() == []
    assert (Pipe([]) | take(0) | list).get() == []
    assert (Pipe([]) | take(10) | list).get() == []
    assert (Pipe([1, 2, 3]) | take(0) | list).get() == []
    assert (Pipe([1, 2, 3]) | take() | list).get() == [1]
    assert (Pipe([1, 2, 3]) | take(2) | list).get() == [1, 2]
    assert (Pipe([1, 2, 3]) | take(3) | list).get() == [1, 2, 3]
    assert (Pipe([1, 2, 3]) | take(10) | list).get() == [1, 2, 3]

    with raises(ValueError):
        Pipe([]) | take(-1)


def test_take_last():
    assert (Pipe([]) | take_last() | list).get() == []
    assert (Pipe([]) | take_last(0) | list).get() == []
    assert (Pipe([]) | take_last(10) | list).get() == []
    assert (Pipe([1, 2, 3]) | take_last(0) | list).get() == []
    assert (Pipe([1, 2, 3]) | take_last() | list).get() == [3]
    assert (Pipe([1, 2, 3]) | take_last(2) | list).get() == [2, 3]
    assert (Pipe([1, 2, 3]) | take_last(3) | list).get() == [1, 2, 3]
    assert (Pipe([1, 2, 3]) | take_last(10) | list).get() == [1, 2, 3]

    with raises(ValueError):
        Pipe([]) | take_last(-1)


def test_take_last_while():
    assert (Pipe([]) | take_last_while(is_even) | list).get() == []
    assert (Pipe([1]) | take_last_while(is_even) | list).get() == []
    assert (Pipe([0, 1]) | take_last_while(is_even) | list).get() == []
    pipe = (Pipe([2, 4, 6]) | take_last_while(is_even) | list)
    assert pipe.get() == [2, 4, 6]
    pipe = (Pipe([2, 1, 4, 6]) | take_last_while(is_even) | list)
    assert pipe.get() == [4, 6]


def test_take_while():
    assert (Pipe([]) | take_while(is_even) | list).get() == []
    assert (Pipe([1]) | take_while(is_even) | list).get() == []
    assert (Pipe([1, 2]) | take_while(is_even) | list).get() == []
    assert (Pipe([2, 4, 6]) | take_while(is_even) | list).get() == [2, 4, 6]
    assert (Pipe([2, 1, 4, 6]) | take_while(is_even) | list).get() == [2]


def test_transpose():
    assert (Pipe(range(6)) | chunked(2) | transpose | map_(tuple) | tuple
            ).get() == ((0, 2, 4), (1, 3, 5))

    assert Pipe([]).then(transpose).then(list).get() == []
    assert (Pipe([[1]]) | transpose | map_(list) | list).get() == [[1]]
    assert (Pipe([[1, 2]]) | transpose | map_(list) | list).get() == [[1], [2]]
    assert (Pipe([[1], [2]]) | transpose | map_(list) | list).get() == [[1, 2]]


def test_try_map():
    pipe = (Pipe([])
            | try_map(lambda x: 1 / x, ZeroDivisionError, 0)
            | list)
    assert pipe.get() == []
    pipe = (Pipe(range(1, 3))
            | map_(Fraction)
            | try_map(lambda x: 1 / x, ZeroDivisionError, Fraction(0))
            | list)
    assert pipe.get() == [Fraction(1, 1), Fraction(1, 2)]
    pipe = (Pipe(range(-1, 2))
            | map_(Fraction)
            | try_map(lambda x: 1 / x, ZeroDivisionError, Fraction(0))
            | list)
    assert pipe.get() == [Fraction(-1, 1), Fraction(0, 1), Fraction(1, 1)]
    pipe = (Pipe(range(-1, 2))
            | map_(Fraction)
            | try_map(lambda x: 1 / x, default=ZeroDivisionError,
                      ignore_errors=True)
            | list)
    assert pipe.get() == [Fraction(-1, 1), Fraction(1, 1)]

    with raises(ZeroDivisionError):
        (Pipe(range(-1, 2))
         | map_(Fraction)
         | try_map(lambda x: 1 / x, IndexError, Fraction(0))
         | list).get()


def test_windowed():
    assert (Pipe([1]) | windowed(1) | map_(list) | list).get() == [[1]]
    pipe = (Pipe([1, 2, 3]) | windowed(2) | map_(list) | list)
    assert pipe.get() == [[1, 2], [2, 3]]

    with raises(ValueError):
        (Pipe([]) | windowed(1) | list).get()

    with raises(ValueError):
        (Pipe([1]) | windowed(2) | list).get()

    with raises(ValueError):
        (Pipe([1]) | windowed(-1) | list).get()

    with raises(ValueError):
        (Pipe([1]) | windowed(0) | list).get()


def test_unzip():
    assert (Pipe([]) | unzip | map_(list) | list).get() == [[], []]
    pipe = (Pipe(["a", "ab", "abc"])
            | associate_with(len)
            | unzip
            | map_(list)
            | list)
    assert pipe.get() == [["a", "ab", "abc"], [1, 2, 3]]

    pipe = (Pipe([(1, 2), (3, 4), (5, 6)])
            | unzip
            | map_(list)
            | list)
    assert pipe.get() == [[1, 3, 5], [2, 4, 6]]
