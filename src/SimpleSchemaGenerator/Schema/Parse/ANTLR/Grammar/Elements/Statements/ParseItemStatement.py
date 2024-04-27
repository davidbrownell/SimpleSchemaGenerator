# ----------------------------------------------------------------------
# |
# |  ParseItemStatement.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-13 11:18:20
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the ParseItemStatement object."""

from dataclasses import dataclass

from dbrownell_Common.Types import override

from ..Common.ParseIdentifier import ParseIdentifier
from ..Types.ParseType import ParseType

from ......Elements.Statements.Statement import Element, Statement


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ParseItemStatement(Statement):
    """Defins a single item; instances are only valid during the parsing process and are converted to other items in subsequent steps."""

    # ----------------------------------------------------------------------
    name: ParseIdentifier
    type: ParseType

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from super(ParseItemStatement, self)._GenerateAcceptDetails()

        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "name", self.name
        )
        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "type", self.type
        )
