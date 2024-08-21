# ----------------------------------------------------------------------
# |
# |  TimeTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-16 10:44:31
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the TimeTypeDefinition object."""

from dataclasses import dataclass
from datetime import time
from typing import ClassVar, Type as PythonType

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class TimeTypeDefinition(TypeDefinition):
    """A Time type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Time"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (time,)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: time,
    ) -> time:
        # No conversion necessary
        return value
