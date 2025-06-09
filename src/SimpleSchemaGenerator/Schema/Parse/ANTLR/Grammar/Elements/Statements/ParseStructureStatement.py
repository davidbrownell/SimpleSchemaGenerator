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
from typing import cast

from dbrownell_Common.Types import override

from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Common.ParseIdentifier import ParseIdentifier
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Types.ParseIdentifierType import (
    ParseIdentifierType,
)

from SimpleSchemaGenerator.Schema.Elements.Common.Cardinality import Cardinality
from SimpleSchemaGenerator.Schema.Elements.Common.Metadata import Metadata
from SimpleSchemaGenerator.Schema.Elements.Statements.Statement import Element, Statement


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ParseStructureStatement(Statement):
    """A structure-like statement that is used during the parse process"""

    # ----------------------------------------------------------------------
    name: ParseIdentifier
    bases: list[ParseIdentifierType] | None
    cardinality: Cardinality
    unresolved_metadata: Metadata | None
    children: list[Statement]  # Can be empty

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from super()._GenerateAcceptDetails()

        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "name", self.name
        )

        if self.bases:
            yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
                "bases", cast(list[Element], self.bases)
            )

        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "cardinality", self.cardinality
        )

        if self.unresolved_metadata:
            yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
                "unresolved_metadata", self.unresolved_metadata
            )

    # ----------------------------------------------------------------------
    @override
    def _GetAcceptChildren(self) -> Element._GetAcceptChildrenResultType:
        return Element._GetAcceptChildrenResult(  # noqa: SLF001
            "children", cast(list[Element], self.children)
        )
