"""
Be careful with this one.

Contains all the utility functions.

Deprecated since 0.2.0
"""

import warnings

warnings.warn(DeprecationWarning(
    "utils module is deprecated – use the root `pipe_utils` module instead"
))

# noinspection PyUnresolvedReferences
from .pipe import *
# noinspection PyUnresolvedReferences
from .iterables import *
# noinspection PyUnresolvedReferences
from .mappings import *
# noinspection PyUnresolvedReferences
from .values import *
