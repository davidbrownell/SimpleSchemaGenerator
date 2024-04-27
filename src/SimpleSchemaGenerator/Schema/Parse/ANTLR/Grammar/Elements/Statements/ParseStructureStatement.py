# ----------------------------------------------------------------------
# |
# |  ParseStructureStatement.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-13 11:30:42
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
# """Contains the ParseStructureStatement object."""

from dataclasses import dataclass
from typing import cast, Optional

from dbrownell_Common.Types import override

from ..Common.ParseIdentifier import ParseIdentifier
from ..Types.ParseIdentifierType import ParseIdentifierType

from ......Elements.Common.Cardinality import Cardinality
from ......Elements.Common.Metadata import Metadata
from ......Elements.Statements.Statement import Element, Statement


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ParseStructureStatement(Statement):
    """A structure-like statement that is used during the parse process"""

    # ----------------------------------------------------------------------
    name: ParseIdentifier
    bases: Optional[list[ParseIdentifierType]]
    cardinality: Cardinality
    unresolved_metadata: Optional[Metadata]
    children: list[Statement]  # Can be empty

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from super(ParseStructureStatement, self)._GenerateAcceptDetails()

        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "name", self.name
        )

        if self.bases:
            yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
                "bases", cast(list[Element], self.bases)
            )

        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "cardinality", self.cardinality
        )

        if self.unresolved_metadata:
            yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
                "unresolved_metadata", self.unresolved_metadata
            )

    # ----------------------------------------------------------------------
    @override
    def _GetAcceptChildren(self) -> Element._GetAcceptChildrenResultType:
        return Element._GetAcceptChildrenResult(  # pylint: disable=protected-access
            "children", cast(list[Element], self.children)
        )
