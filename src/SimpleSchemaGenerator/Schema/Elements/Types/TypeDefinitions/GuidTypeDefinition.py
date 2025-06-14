# ----------------------------------------------------------------------
# |
# |  GuidTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-16 09:13:30
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the GuidTypeDefinition object."""

from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from dbrownell_Common.Types import override

from .TypeDefinition import TypeDefinition


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class GuidTypeDefinition(TypeDefinition):
    """A Guid type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Guid"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (UUID,)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: UUID,
    ) -> UUID:
        # No conversion necessary
        return value
