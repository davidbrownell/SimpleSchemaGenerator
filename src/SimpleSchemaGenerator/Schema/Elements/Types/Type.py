# ----------------------------------------------------------------------
# |
# |  Type.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-12 20:12:04
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Type object."""

from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar

from dbrownell_Common.Types import extension

from ..Common.Element import Element
from ..Common.UniqueNameTrait import UniqueNameTrait


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Type(UniqueNameTrait, Element):
    """Abstract base class for IntrinsicType and ComplexType"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = ""

    # ----------------------------------------------------------------------
    def __post_init__(self):
        if self.NAME == "":
            raise Exception(f"NAME must be defined for '{self.__class__.__name__}'.")

    # ----------------------------------------------------------------------
    @cached_property
    def display_type(self) -> str:
        return self._display_type

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @property
    @extension
    def _display_type(self) -> str:
        return self.__class__.NAME
