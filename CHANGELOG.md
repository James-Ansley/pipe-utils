# Changelog

All notable changes to this project will be documented in this file.

## [0.4.0]

### Additions

- Curry wrapper. Functions can now be decorated with an `@curry` decorator.
  e.g.:
  ```python
  from pipe_utils import curry
  
  @curry
  def foo(x, y, z=3):
      return [x, y, z]
  
  result = foo(z=1)(3)(2)  # or: `foo(z=1) >> 3 >> 2`, or `foo(3, 2, 1)`
  print(result)  # [3, 2, 1]
  ```
- `P` added as a short alias for `Pipe`
- Pipes can now be created with the `>>` operator: `P >> data | ... `
- `obj` object to allow for method calls in pipe operations without using
  lambdas
- `returns`, and `instance_of` functions in the `values` module
- `case_match` and `case_when` functions in the `mappings` module
- `split_by_any` and `split_when` functions to split by containers and
  predicates respectively
- `melt` and `unmelt` in the `mappings` module to transform dicts to iterables
  and back
- `as_tuple`, `as_tuples`, `as_tuple_of_tuples`, `as_list`, `as_lists`,
  `as_list_of_lists` functions to easily convert data types

### Changes

- All functions are now curried and can be called with brackets or the right
  shift operator (e.g. `foo(1)(2)` or `foo >> 1 >> 2`).
  Functions will still work as before.
- `get_or_default` is now deprecated, use `get(n, default=...)` instead
- **breaking change** `first` and `last` now return single unwraped elements —
  to retrieve an iterable, use `take` and `take_last`
- **breaking change** `chunked`, `drop`, `drop_last`, `windowed`, no longer
  eagerly check for value errors
- **breaking change** `join_to_str` separator args are now keyword only
- **breaking change** `pad_with` `length` argument now no longer has a default
  None value
- **breaking change** `split_by` now takes a single `sep` parameter –
  use `split_by_any` as a replacement for multiple split values
- **breaking change** `try_map`, `catch` parameter is now keyword only

## [0.3.0]

### Additions

- `raises` function in `values`. Similar to `raise_` but returns a callable.
- Several functions in the `iterables` module:
    - `strip`, `lstrip`, `rstrip` and `strip_while`
    - `replace` function
    - `extend` and `extend_left` as replacements to `concat` and `concat_after`
    - `map_indexed` and `filter_indexed` functions
    - `wrap` function

### Changes

- **Deprecated modules and functions have been removed:** `utils` module and
  several functions in `values`
- `concat` and `concat_after` are now **deprecated** use `extend`
  and `extend_left` instead
- `try_map` now ignores errors by default and will only include default values
  if the (now named) default parameter is given. `err` parameter is also changed
  to `catch`
- `raise_` and `Raise` functions now take `nothing` singleton for the `from_`
  parameter allowing for exception chain disabling with the `raise E from None`
  idiom.
- `Pipe.get_or_raise` now takes a named `chained` parameter that determines
  whether errors should be chained with the caught Pipe exceptions.
- `chunked` now takes `partial` and `strict` arguments.
- Typehints have been updated for `Or`/`or_` and `And`/`and_` to indicate
  non-boolean return types.

## [0.2.2]

### Additions

- `pad_with` function has been added to `iterables` module.
- A `Catch` class has been added as an equivalent to `Pipe.catch` intended to be
  used with chained `__or__` calls
- `raise_` function in `values` module that raises an exception. Aliased
  as `Raise` in `override` module.

### Changes

- `it_is` and `it_is_not` have been **deprecated**, use `is_` and `is_not`
  instead for consistency with other naming conventions.
- `windowed` now has `strict` and `partial` parameters
- `Pipe` `get_or_default` and `get_or_raise` methods now take a named `catch`
  parameter that limits the scope of errors that are caught.
- `override` module now aliases `values` functions `and_`, `or_`, `not_`
  and `is_` to `And`, `Or`, `Not`, and `Is` to avoid underscore naming
  convention. Including `is_not` to `IsNot` for consistency with other binary
  operations.

## [0.2.1]

### Additions

- `sum_by` function was added to `iterables` module

### Changes

- multiple `it` objects can now be used in a single expression. e.g. `it ** it`

## [0.2.0]

### Additions

- An `override` module has been added that exposes `Pipe`, `Then`, `it` and all
  utility functions but aliases `filer_`, `map_`, `all_`, `any_`, and `slice_`
  to not include the trailing underscore – overriding the builtin names
- An `it` object has been added to the `pipe` module. This allows for simple
  comparisons to be constructed:
  ```python
  from pipe_utils.override import *
  
  class Foo:
      def __init__(self, bar):
          self.bar = bar

  res = (
      Pipe(Foo(x) for x in range(10))
      | map(it.bar)
      | filter(it % 2 == 0)
      | list
  ).get()
  
  print(res)
  ```
- Added `not_contains` utility to `iterables` module

### Changes

- `utils` module is now **deprecated**
- All utilities are now imported into the root `pipe_utils` module by default
- Several functions in the `values` module are **deprecated** as these are now
  replaced by the `it` object behaviour (e.g. `gt`, `add_by`, etc.).

### BugFixes

- `sorted_dict_by` no longer has a default key of `None`

## [0.1.0]

### Additions

- `to_each` in the `iterables` module
- `clamp`, `lclamp`, and `rclamp` in the `values` module
- `map_keys`, `map_values`, `filter_keys`, `filter_values`, `get_value`,
  `get_value_or_default` functions in the `mappings` module
- `utils` module that imports `Pipe`, `Then` and all utility functions

[0.3.0]: https://github.com/James-Ansley/pipe-utils/compare/v0.2.2...v0.3.0

[0.2.2]: https://github.com/James-Ansley/pipe-utils/compare/v0.2.1...v0.2.2

[0.2.1]: https://github.com/James-Ansley/pipe-utils/compare/v0.2.0...v0.2.1

[0.2.0]: https://github.com/James-Ansley/pipe-utils/compare/v0.1.0...v0.2.0

[0.1.0]: https://github.com/James-Ansley/pipe-utils/compare/v0.0.1...v0.1.0
