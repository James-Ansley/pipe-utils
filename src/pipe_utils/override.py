"""
Imports everything but aliases:
`filer_`, `map_`, `all_`, `any_`, and `slice_` to not include the trailing
underscore – overriding their corresponding builtin names.

And, `not_`, `or_`, `and_`, `is_`, `is_not`, `raise_` to
`Not`, `Or`, `And`, `Is`, `IsNot`, `Raise` to remove the trailing underscore.
CamelCase to avoid clash with keywords.
"""

# noinspection PyUnresolvedReferences
from .pipe import *
# noinspection PyUnresolvedReferences
from .iterables import *
# noinspection PyUnresolvedReferences
from .mappings import *
# noinspection PyUnresolvedReferences
from .values import *

# noinspection PyUnresolvedReferences,PyShadowingBuiltins
from .iterables import (
    filter_ as filter,
    map_ as map,
    all_ as all,
    any_ as any,
    slice_ as slice,
)

# noinspection PyUnresolvedReferences,PyPep8Naming
from .values import (
    not_ as Not,
    or_ as Or,
    and_ as And,
    is_ as Is,
    is_not as IsNot,
    raise_ as Raise,
)
