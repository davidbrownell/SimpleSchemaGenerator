# ----------------------------------------------------------------------
# |
# |  ItemStatement.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-20 17:57:45
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the ItemStatement object."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from dbrownell_Common.Types import override

from .Statement import Statement
from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element
from SimpleSchemaGenerator.Schema.Elements.Common.TerminalElement import TerminalElement
from SimpleSchemaGenerator.Schema.Elements.Common.Visibility import VisibilityTrait

if TYPE_CHECKING:
    from SimpleSchemaGenerator.Schema.Elements.Types.ReferenceType import ReferenceType  # pragma: no cover


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ItemStatement(VisibilityTrait, Statement):
    """Defines a single attribute"""

    # ----------------------------------------------------------------------
    name: TerminalElement[str]
    type: "ReferenceType"

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from VisibilityTrait._GenerateAcceptDetails(self)  # noqa: SLF001

        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "name",
            self.name,
        )

        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "type",
            self.type,  # TODO: cast(WeakReferenceType[Element], ref(self.type)),
        )
