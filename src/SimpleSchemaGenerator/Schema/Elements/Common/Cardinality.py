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
from typing import Any, Optional

from dbrownell_Common.InflectEx import inflect  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .Element import Element
from ..Expressions.Expression import Expression
from ..Expressions.IntegerExpression import IntegerExpression
from ....Common.Error import Error
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
            raise Errors.SimpleSchemaGeneratorException(
                Errors.CardinalityInvalidRange.Create(
                    max_param.region,
                    min_param.value,
                    max_param.value,
                ),
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
    def Validate(
        self,
        expression_or_value: Expression | Any,
    ) -> None:
        # ----------------------------------------------------------------------
        def Impl(
            value: Any,
        ) -> None:
            if value is None:
                if self.is_optional:
                    return

                raise Exception(Errors.cardinality_validate_none_not_expected)

            if self.is_container:
                if not isinstance(value, list):
                    raise Exception(Errors.cardinality_validate_list_required)

                num_items = len(value)

                if num_items < self.min.value:
                    raise Exception(
                        Errors.cardinality_validate_list_too_small.format(
                            value=inflect.no("item", self.min.value),
                            value_verb=inflect.plural_verb("was", self.min.value),
                            found=inflect.no("item", num_items),
                            found_verb=inflect.plural_verb("was", num_items),
                        ),
                    )

                if self.max is not None and num_items > self.max.value:
                    raise Exception(
                        Errors.cardinality_validate_list_too_large.format(
                            value=inflect.no("item", self.max.value),
                            value_verb=inflect.plural_verb("was", self.max.value),
                            found=inflect.no("item", num_items),
                            found_verb=inflect.plural_verb("was", num_items),
                        ),
                    )

                return

            elif self.is_optional:
                # We don't have enough context to validate the cardinality, but it will be validated
                # at a later time.
                return

            if isinstance(value, list):
                raise Exception(Errors.cardinality_validate_list_not_expected)

        # ----------------------------------------------------------------------

        if isinstance(expression_or_value, Expression):
            try:
                Impl(expression_or_value.value)
                return
            except Exception as ex:
                raise Errors.SimpleSchemaGeneratorException(
                    Error.Create(
                        ex,
                        expression_or_value.region,
                        include_callstack=False,
                    ),
                ) from ex

        Impl(expression_or_value)

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
