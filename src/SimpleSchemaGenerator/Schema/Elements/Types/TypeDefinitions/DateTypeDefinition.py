# ----------------------------------------------------------------------
# |
# |  DateTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-14 15:03:06
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the DateTypeDefinition object."""

from dataclasses import dataclass
from datetime import date
from typing import ClassVar

from dbrownell_Common.Types import override

from .TypeDefinition import TypeDefinition


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class DateTypeDefinition(TypeDefinition):
    """A Date type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Date"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (date,)

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: date,
    ) -> date:
        # No conversion necessary
        return value
