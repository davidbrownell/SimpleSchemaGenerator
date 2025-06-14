# ----------------------------------------------------------------------
# |
# |  ParseIdentifierType.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-13 12:06:23
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the ParseIdentifierType object."""

from dataclasses import dataclass
from typing import cast

from dbrownell_Common.Types import override

from .ParseType import ParseType
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Common.ParseIdentifier import ParseIdentifier
from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element
from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ParseIdentifierType(ParseType):
    """Temporary identifier generated during parsing and replaced in subsequent steps."""

    # ----------------------------------------------------------------------
    identifiers: list[ParseIdentifier]
    is_global_reference: Region | None

    # ----------------------------------------------------------------------
    def __post_init__(self) -> None:
        if not self.identifiers:
            raise Errors.SimpleSchemaGeneratorError(Errors.ParseIdentifierTypeEmpty.Create(self.region))

        for identifier in self.identifiers:
            if not identifier.is_type:
                raise Errors.SimpleSchemaGeneratorError(
                    Errors.ParseIdentifierTypeNotType.Create(identifier.region, identifier.value)
                )

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from super()._GenerateAcceptDetails()

        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "identifiers", cast(list[Element], self.identifiers)
        )

    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        return "{global_value}{identifiers}{cardinality}".format(
            global_value="::" if self.is_global_reference else "",
            identifiers=".".join(identifier.value for identifier in self.identifiers),
            cardinality=self.cardinality,
        )
