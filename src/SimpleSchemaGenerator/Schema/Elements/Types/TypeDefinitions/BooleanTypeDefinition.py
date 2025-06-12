# ----------------------------------------------------------------------
# |
# |  BooleanTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-14 13:54:31
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the BooleanTypeDefinition object."""

from dataclasses import dataclass
from typing import ClassVar

from dbrownell_Common.Types import override

from .TypeDefinition import TypeDefinition


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class BooleanTypeDefinition(TypeDefinition):
    """A Boolean type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Boolean"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (bool,)

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: bool,  # noqa: FBT001
    ) -> bool:
        # No conversion necessary
        return value
