# ----------------------------------------------------------------------
# |
# |  ListExpression.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 15:04:48
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the ListExpression object."""

from dataclasses import dataclass
from typing import cast, ClassVar

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .Expression import Expression
from ..Common.Element import Element


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ListExpression(Expression):
    """A list of expressions"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "List"

    value: list[Expression]

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "value", cast(list[Element], self.value)
        )
