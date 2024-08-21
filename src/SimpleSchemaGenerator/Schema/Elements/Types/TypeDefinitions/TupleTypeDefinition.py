# ----------------------------------------------------------------------
# |
# |  TupleTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-19 10:21:17
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the TupleTypeDefinition object."""

import itertools

from dataclasses import dataclass, MISSING
from typing import Any, cast, ClassVar, Type as PythonType

from dbrownell_Common.InflectEx import inflect  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition
from ..Type import Type
from ...Common.Element import Element
from ..... import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class TupleTypeDefinition(TypeDefinition):
    """A list of types"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Tuple"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (tuple,)

    types: list[Type]

    # ----------------------------------------------------------------------
    def __post_init__(self, *args, **kwargs):
        if not self.types:
            raise Errors.SimpleSchemaGeneratorException(
                Errors.TupleTypedefNoTypes.Create(self.region)
            )

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        display_values: list[str] = []

        for child_type in self.types:
            child_display = child_type.display_type

            if "{" in child_display and not (
                child_display.startswith("<") and child_display.endswith(">")
            ):
                child_display = f"<{child_display}>"

            display_values.append(child_display)

        return "({}, )".format(", ".join(display_values))

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: tuple,
    ) -> tuple:
        tuple_items: list[Any] = []

        for child_type, child_expression_or_value in itertools.zip_longest(
            self.types,
            value,
            fillvalue=MISSING,
        ):
            if child_type is MISSING or child_expression_or_value is MISSING:
                raise Exception(
                    Errors.tuple_type_item_mismatch.format(
                        value=inflect.no("tuple item", len(self.types)),
                        value_verb=inflect.plural_verb("was", len(self.types)),
                        found=inflect.no("tuple item", len(value)),
                        found_verb=inflect.plural_verb("was", len(value)),
                    ),
                )

            tuple_items.append(child_type.ToPythonInstance(child_expression_or_value))

        return tuple(tuple_items)

    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from super(TupleTypeDefinition, self)._GenerateAcceptDetails()

        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "types",
            cast(list[Element], self.types),
        )
