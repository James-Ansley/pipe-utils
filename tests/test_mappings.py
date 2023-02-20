from collections.abc import ItemsView, KeysView, ValuesView

from pipe_utils.mappings import *


def test_item_view():
    items = item_view({})
    assert isinstance(items, ItemsView) and list(items) == []
    items = item_view({1: "a", 2: "b"})
    assert list(items) == [(1, "a"), (2, "b")]


def test_value_view():
    values = value_view({})
    assert isinstance(values, ValuesView) and list(values) == []
    values = value_view({1: "a", 2: "b"})
    assert list(values) == ["a", "b"]


def test_key_view():
    keys = key_view({})
    assert isinstance(keys, KeysView) and list(keys) == []
    keys = key_view({1: "a", 2: "b"})
    assert list(keys) == [1, 2]


def test_sorted_dict():
    assert sorted_dict({}) == {}
    result = tuple(sorted_dict({2: "a", 1: "b"}).items())
    assert result == tuple({1: "b", 2: "a"}.items())


def test_sorted_dict_by():
    result = tuple(sorted_dict_by(sum)({0: 5, 1: 3, 2: 1}).items())
    assert result == tuple({2: 1, 1: 3, 0: 5}.items())


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
