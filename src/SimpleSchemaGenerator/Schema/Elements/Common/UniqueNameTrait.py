# ----------------------------------------------------------------------
# |
# |  UniqueNameTrait.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-12 20:01:54
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the UniqueNameTrait object."""

from dataclasses import dataclass, field
from typing import Union


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class UniqueNameTrait:
    """Trait for Elements that are given an unique name during parsing."""

    # ----------------------------------------------------------------------
    _unique_name: Union[
        None,  # Before NormalizeUniqueName is called
        str,  # After NormalizeUniqueName is called
    ] = field(init=False, default=None)

    # ----------------------------------------------------------------------
    @property
    def is_unique_name_normalized(self) -> bool:
        return self._unique_name is not None

    @property
    def unique_name(self) -> str:
        # Valid after NormalizeUniqueName is called
        assert self._unique_name is not None
        return self._unique_name

    # ----------------------------------------------------------------------
    def NormalizeUniqueName(self, unique_name: str) -> None:
        assert self._unique_name is None, self._unique_name
        object.__setattr__(self, "_unique_name", unique_name)
