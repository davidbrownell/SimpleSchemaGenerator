# ----------------------------------------------------------------------
# |
# |  DurationTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-14 15:16:45
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the DurationTypeDefinition object."""

from dataclasses import dataclass
from datetime import timedelta
from typing import ClassVar, Type as PythonType

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class DurationTypeDefinition(TypeDefinition):
    """A Duration type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Duration"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (timedelta,)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: timedelta,
    ) -> timedelta:
        # No conversion necessary
        return value
