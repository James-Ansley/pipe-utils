# Changelog

All notable changes to this project will be documented in this file.

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

[0.2.2]: https://github.com/James-Ansley/pipe-utils/compare/v0.2.1...v0.2.2

[0.2.1]: https://github.com/James-Ansley/pipe-utils/compare/v0.2.0...v0.2.1

[0.2.0]: https://github.com/James-Ansley/pipe-utils/compare/v0.1.0...v0.2.0

[0.1.0]: https://github.com/James-Ansley/pipe-utils/compare/v0.0.1...v0.1.0
