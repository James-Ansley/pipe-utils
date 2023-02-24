from collections.abc import ItemsView, KeysView, ValuesView

from pytest import raises

from pipe_utils.mappings import *
from pipe_utils.utils import fdiv_by, mul_by
from pipe_utils.values import gt, is_even


def test_filter_keys():
    assert filter_keys(is_even)({}) == {}
    data = {1: "a", 2: "b", 3: "c", 4: "d"}
    assert filter_keys(is_even)(data) == {2: "b", 4: "d"}
    assert filter_keys(gt(0))(data) == data


def test_filter_values():
    assert filter_values(is_even)({}) == {}
    data = {"a": 1, "b": 2, "c": 3, "d": 4}
    assert filter_values(is_even)(data) == {"b": 2, "d": 4}
    assert filter_values(gt(0))(data) == data


def test_get_value():
    assert get_value(1)({1: "a"}) == "a"

    with raises(KeyError):
        assert get_value(2)({1: "a"})
    with raises(KeyError):
        assert get_value(2)({})


def test_get_value_or_default():
    assert get_value_or_default(1, None)({1: "a"}) == "a"
    assert get_value_or_default(2, None)({1: "a"}) is None
    assert get_value_or_default(2, 0)({}) == 0
    assert get_value_or_default(-1, 0)({}) == 0


def test_item_view():
    items = item_view({})
    assert isinstance(items, ItemsView) and list(items) == []
    items = item_view({1: "a", 2: "b"})
    assert list(items) == [(1, "a"), (2, "b")]


def test_key_view():
    keys = key_view({})
    assert isinstance(keys, KeysView) and list(keys) == []
    keys = key_view({1: "a", 2: "b"})
    assert list(keys) == [1, 2]


def test_map_keys():
    data = {1: "a", 2: "b", 3: "c"}
    assert dict(map_keys(mul_by(2))(data)) == {2: "a", 4: "b", 6: "c"}
    data = {2: "a", 3: "d", 4: "b", 5: "e", 6: "c", 7: "f"}
    assert dict(map_keys(fdiv_by(2))(data)) == {1: "d", 2: "e", 3: "f"}


def test_map_values():
    data = {1: "a", 2: "b", 3: "c"}
    assert dict(map_values(mul_by(2))(data)) == {1: "aa", 2: "bb", 3: "cc"}
    data = {"a": 2, "d": 3, "b": 4, "e": 5}
    expect = {"a": 1, "d": 1, "b": 2, "e": 2}
    assert dict(map_values(fdiv_by(2))(data)) == expect


def test_sorted_by_key():
    assert sorted_by_key({}) == {}
    result = tuple(sorted_by_key({2: "a", 1: "b"}).items())
    assert result == tuple({1: "b", 2: "a"}.items())


def test_sorted_by_key_by():
    result = tuple(sorted_by_key_by(len)({"abc": 0, "bc": 1, "c": 2}).items())
    assert result == tuple({"c": 2, "bc": 1, "abc": 0}.items())


def test_sorted_by_value():
    assert sorted_by_value({}) == {}
    result = tuple(sorted_by_value({"a": 2, "b": 1}).items())
    assert result == tuple({"b": 1, "a": 2}.items())


def test_sorted_by_value_by():
    result = tuple(
        sorted_by_value_by(len)({0: "abc", 1: "bc", 2: "c"}).items()
    )
    assert result == tuple({2: "c", 1: "bc", 0: "abc"}.items())


def test_sorted_dict():
    assert sorted_dict({}) == {}
    result = tuple(sorted_dict({2: "a", 1: "b"}).items())
    assert result == tuple({1: "b", 2: "a"}.items())


def test_sorted_dict_by():
    result = tuple(sorted_dict_by(sum)({0: 5, 1: 3, 2: 1}).items())
    assert result == tuple({2: 1, 1: 3, 0: 5}.items())


def test_value_view():
    values = value_view({})
    assert isinstance(values, ValuesView) and list(values) == []
    values = value_view({1: "a", 2: "b"})
    assert list(values) == ["a", "b"]
