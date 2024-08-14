# ----------------------------------------------------------------------
# |
# |  TupleExpression.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 15:10:28
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the TupleExpression object."""

from dataclasses import dataclass
from typing import ClassVar

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .Expression import Expression
from ..Common.Element import Element
from .... import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class TupleExpression(Expression):
    """Tuple value"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Tuple"

    value: tuple[Expression, ...]

    # ----------------------------------------------------------------------
    def __post_init__(self):
        if not self.value:
            raise Errors.SimpleSchemaGeneratorException(
                Errors.TupleExpressionEmpty.Create(self.region)
            )

        super(TupleExpression, self).__post_init__()

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "value", list(self.value)
        )
