# ----------------------------------------------------------------------
# |
# |  ParseVariantType.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-20 17:46:44
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the ParseVariantType object."""

from dataclasses import dataclass
from typing import cast

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .ParseType import ParseType
from ......Elements.Common.Element import Element
from ....... import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ParseVariantType(ParseType):
    """A list of types used during the parsing process; subsequent steps will replace this value."""

    # ----------------------------------------------------------------------
    types: list[ParseType]

    # ----------------------------------------------------------------------
    def __post_init__(self):
        if len(self.types) < 2:
            raise Errors.SimpleSchemaGeneratorException(
                Errors.ParseVariantTypeMissingTypes.Create(self.region)
            )

        for the_type in self.types:
            if isinstance(the_type, ParseVariantType):
                raise Errors.SimpleSchemaGeneratorException(
                    Errors.ParseVariantTypeNestedType.Create(the_type.region)
                )

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from super(ParseVariantType, self)._GenerateAcceptDetails()

        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "types",
            cast(list[Element], self.types),
        )

    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        return "({}){}".format(
            " | ".join(child_type.display_type for child_type in self.types),
            self.cardinality,
        )
