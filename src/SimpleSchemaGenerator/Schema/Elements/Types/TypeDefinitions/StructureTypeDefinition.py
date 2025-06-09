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
from typing import ClassVar, NoReturn

from dbrownell_Common.Types import override

from .TypeDefinition import TypeDefinition
from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element
from SimpleSchemaGenerator.Schema.Elements.Statements.StructureStatement import StructureStatement


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class StructureTypeDefinition(TypeDefinition):
    """A Structure type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Structure"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (object,)

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
        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "structure", self.structure
        )

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(self, *args, **kwargs) -> NoReturn:  # noqa: ARG002
        raise Exception(  # noqa: TRY003
            "This method should never be called for StructureTypeDefinition instances."  # noqa: EM101
        )  # pragma: no cover
