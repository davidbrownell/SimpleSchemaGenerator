# ----------------------------------------------------------------------
# |
# |  BooleanTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-13 16:22:46
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the BooleanTypeDefinition object."""

from dataclasses import dataclass
from typing import Any, ClassVar, Type as PythonType

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class BooleanTypeDefinition(TypeDefinition):
    """A boolean."""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Boolean"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (bool,)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: Any,
    ) -> Any:
        return value
