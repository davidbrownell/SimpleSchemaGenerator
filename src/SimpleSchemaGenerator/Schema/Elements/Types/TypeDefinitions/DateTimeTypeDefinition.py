# ----------------------------------------------------------------------
# |
# |  DateTimeTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-14 14:57:10
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the DateTimeTypeDefinition object."""

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, Type as PythonType

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class DateTimeTypeDefinition(TypeDefinition):
    """A DateTime type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "DateTime"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (datetime,)

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: datetime,
    ) -> datetime:
        # No conversion necessary
        return value
