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
from typing import ClassVar, Type as PythonType

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class BooleanTypeDefinition(TypeDefinition):
    """A Boolean type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Boolean"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (bool,)

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: bool,
    ) -> bool:
        # No conversion necessary
        return value
