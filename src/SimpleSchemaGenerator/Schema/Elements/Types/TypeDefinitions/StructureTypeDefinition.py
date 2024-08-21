# ----------------------------------------------------------------------
# |
# |  StructureTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-19 09:37:34
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the StructureTypeDefinition object."""

from dataclasses import dataclass
from typing import ClassVar, Type as PythonType

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition
from ...Common.Element import Element
from ...Statements.StructureStatement import StructureStatement


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class StructureTypeDefinition(TypeDefinition):
    """A Structure type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Structure"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (object,)

    structure: StructureStatement

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        return self.structure.name.value

    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "structure", self.structure
        )

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(self, *args, **kwargs):
        raise Exception(  # pragma: no cover
            "This method should never be called for StructureTypeDefinition instances."
        )
