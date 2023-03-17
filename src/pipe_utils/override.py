"""
Imports everything but aliases `filer_`,
`map_`, `all_`, `any_`, and `slice_` to not include the trailing underscore –
overriding their corresponding builtin names.
"""

# noinspection PyUnresolvedReferences
from .pipe import *
# noinspection PyUnresolvedReferences
from .iterables import *
# noinspection PyUnresolvedReferences
from .mappings import *
# noinspection PyUnresolvedReferences
from .values import *

# noinspection PyUnresolvedReferences
from .iterables import (
    filter_ as filter,
    map_ as map,
    all_ as all,
    any_ as any,
    slice_ as slice,
)
