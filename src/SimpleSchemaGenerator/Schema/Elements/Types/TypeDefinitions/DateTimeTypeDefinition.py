# ----------------------------------------------------------------------
# |
# |  DateTimeTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-13 16:24:28
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
from typing import Any, ClassVar, Type as PythonType

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class DateTimeTypeDefinition(TypeDefinition):
    """A date and time."""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "DateTime"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (datetime,)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: Any,
    ) -> Any:
        return value
