from pipe_utils.override import *


def is_even(e):
    return e % 2 == 0


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
