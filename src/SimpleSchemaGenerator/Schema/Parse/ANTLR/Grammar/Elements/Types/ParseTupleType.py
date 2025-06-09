# ----------------------------------------------------------------------
# |
# |  ParseTupleType.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-20 17:41:56
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the ParseTupleType object."""

from dataclasses import dataclass
from typing import cast

from dbrownell_Common.Types import override

from .ParseType import ParseType
from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element
from SimpleSchemaGenerator import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ParseTupleType(ParseType):
    """A list of types used during the parsing process; subsequent steps will replace this value."""

    # ----------------------------------------------------------------------
    types: list[ParseType]

    # ----------------------------------------------------------------------
    def __post_init__(self) -> None:
        if not self.types:
            raise Errors.SimpleSchemaGeneratorError(Errors.ParseTupleTypeMissingTypes.Create(self.region))

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from super()._GenerateAcceptDetails()

        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "types",
            cast(list[Element], self.types),
        )

    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        return "({}, ){}".format(
            ", ".join(child_type.display_type for child_type in self.types),
            self.cardinality,
        )
