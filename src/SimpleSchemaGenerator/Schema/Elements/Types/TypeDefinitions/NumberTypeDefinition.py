# ----------------------------------------------------------------------
# |
# |  NumberTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-16 10:24:53
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the NumberTypeDefinition object."""

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Optional, Type as PythonType

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition
from ..... import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class NumberTypeDefinition(TypeDefinition):
    """A Number type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Number"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (float, int)

    # ----------------------------------------------------------------------
    # |
    # |  Public Types
    # |
    # ----------------------------------------------------------------------
    class Bits(str, Enum):
        Value16 = "IEEE 754 half precision"
        Value32 = "IEEE 754 single precision"
        Value64 = "IEEE 754 double precision"
        Value128 = "IEEE 754 quadruple precision"
        Value256 = "IEEE 754 octuple precision"

    # ----------------------------------------------------------------------
    # |
    # |  Public Data
    # |
    # ----------------------------------------------------------------------
    min: Optional[float] = field(default=None)
    max: Optional[float] = field(default=None)
    bits: Optional[Bits] = field(default=None)

    # ----------------------------------------------------------------------
    # |
    # |  Public Methods
    # |
    # ----------------------------------------------------------------------
    def __post_init__(self):
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValueError(
                Errors.number_typedef_min_max_invalid.format(min=self.min, max=self.max)
            )

    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        constraints: list[str] = []

        if self.min is not None:
            constraints.append(f">= {self.min}")
        if self.max is not None:
            constraints.append(f"<= {self.max}")

        result = super(NumberTypeDefinition, self)._display_type

        if constraints:
            result += " {{{}}}".format(", ".join(constraints))

        return result

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: float,
    ) -> float:
        if self.min is not None and value < self.min:
            raise Exception(
                Errors.number_typedef_too_small.format(constraint=self.min, value=value)
            )

        if self.max is not None and value > self.max:
            raise Exception(
                Errors.number_typedef_too_large.format(constraint=self.max, value=value)
            )

        return value
