# ----------------------------------------------------------------------
# |
# |  Cardinality.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 08:12:25
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Cardinality object"""

from dataclasses import dataclass, field, InitVar
from functools import cached_property
from typing import Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .Element import Element
from ..Expressions.IntegerExpression import IntegerExpression
from .... import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Cardinality(Element):
    """Specifies the minimum and maximum number of times an element can appear within a collection."""

    min_param: InitVar[Optional[IntegerExpression]]
    max_param: InitVar[Optional[IntegerExpression]]

    min: IntegerExpression = field(init=False)
    max: Optional[IntegerExpression] = field(init=False)

    # ----------------------------------------------------------------------
    def __post_init__(
        self,
        min_param: Optional[IntegerExpression],
        max_param: Optional[IntegerExpression],
    ) -> None:
        if min_param is None and max_param is None:
            min_param = IntegerExpression(self.region, 1)
            max_param = IntegerExpression(self.region, 1)
        elif min_param is None:
            min_param = IntegerExpression(self.region, 0)
        elif max_param is None:
            # Nothing to do here, as this indicates an unbounded number of items
            pass

        assert min_param is not None

        if max_param is not None and max_param.value < min_param.value:
            raise Errors.CardinalityInvalidRange.CreateAsException(
                max_param.region,
                min_param.value,
                max_param.value,
            )

        # Commit
        object.__setattr__(self, "min", min_param)
        object.__setattr__(self, "max", max_param)

    # ----------------------------------------------------------------------
    def __str__(self) -> str:
        return self._string

    # ----------------------------------------------------------------------
    @cached_property
    def is_single(self) -> bool:
        return self.min.value == 1 and self.max is not None and self.max.value == 1

    @cached_property
    def is_optional(self) -> bool:
        return self.min.value == 0 and self.max is not None and self.max.value == 1

    @cached_property
    def is_container(self) -> bool:
        return self.max is None or self.max.value > 1

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @cached_property
    def _string(self) -> str:
        # pylint: disable=too-many-return-statements
        if self.is_single:
            return ""

        if self.is_optional:
            return "?"

        if self.max is None:
            if self.min.value == 0:
                return "*"

            if self.min.value == 1:
                return "+"

            return f"[{self.min.value}+]"

        if self.min.value == self.max.value:
            return f"[{self.min.value}]"

        return f"[{self.min.value}..{self.max.value}]"

    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem("min", self.min)

        if self.max is not None:
            yield Element._GenerateAcceptDetailsItem("max", self.max)
