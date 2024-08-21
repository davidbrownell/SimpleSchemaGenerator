# ----------------------------------------------------------------------
# |
# |  IntegerTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-16 09:19:24
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the IntegerTypeDefinition object."""

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Optional, Type as PythonType

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition
from ..... import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class IntegerTypeDefinition(TypeDefinition):
    """An Integer type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Integer"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (int,)

    # ----------------------------------------------------------------------
    # |
    # |  Public Types
    # |
    # ----------------------------------------------------------------------
    class Bits(str, Enum):
        Value8 = "8 bits"
        Value16 = "16 bits"
        Value32 = "32 bits"
        Value64 = "64 bits"
        Value128 = "128 bits"

    # ----------------------------------------------------------------------
    # |
    # |  Public Data
    # |
    # ----------------------------------------------------------------------
    min: Optional[int] = field(default=None)
    max: Optional[int] = field(default=None)
    bits: Optional[Bits] = field(default=None)

    # ----------------------------------------------------------------------
    # |
    # |  Public Methods
    # |
    # ----------------------------------------------------------------------
    def __post_init__(self):
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValueError(
                Errors.integer_typedef_min_max_invalid.format(min=self.min, max=self.max)
            )

    # ----------------------------------------------------------------------
    # |
    # |  Private Methods
    # |
    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        constraints: list[str] = []

        if self.min is not None:
            constraints.append(f">= {self.min}")
        if self.max is not None:
            constraints.append(f"<= {self.max}")

        result = super(IntegerTypeDefinition, self)._display_type

        if constraints:
            result += " {{{}}}".format(", ".join(constraints))

        return result

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: int,
    ) -> int:
        if self.min is not None and value < self.min:
            raise Exception(
                Errors.integer_typedef_too_small.format(constraint=self.min, value=value)
            )

        if self.max is not None and value > self.max:
            raise Exception(
                Errors.integer_typedef_too_large.format(constraint=self.max, value=value)
            )

        return value
