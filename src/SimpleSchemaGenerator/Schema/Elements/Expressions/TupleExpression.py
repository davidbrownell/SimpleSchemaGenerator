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

from dbrownell_Common.Types import override

from .Expression import Expression
from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element
from SimpleSchemaGenerator import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class TupleExpression(Expression):
    """Tuple value"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Tuple"

    value: tuple[Expression, ...]

    # ----------------------------------------------------------------------
    def __post_init__(self) -> None:
        if not self.value:
            raise Errors.SimpleSchemaGeneratorError(Errors.TupleExpressionEmpty.Create(self.region))

        super().__post_init__()

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "value", list(self.value)
        )
