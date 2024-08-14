# ----------------------------------------------------------------------
# |
# |  DateTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-13 16:25:21
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
from typing import Any, ClassVar, Type as PythonType

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class DateTypeDefinition(TypeDefinition):
    """A date."""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Date"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (date,)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: Any,
    ) -> Any:
        return value
