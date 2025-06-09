# ----------------------------------------------------------------------
# |
# |  ParseIncludeStatement.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-20 18:21:52
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the ParseIncludeStatement, ParseIncludeStatementItem, and ParseIncludeStatementType objects."""

from dataclasses import dataclass
from enum import auto, Enum
from pathlib import Path
from typing import cast

from dbrownell_Common.Types import override

from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Common.ParseIdentifier import ParseIdentifier

from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element
from SimpleSchemaGenerator.Schema.Elements.Common.TerminalElement import TerminalElement
from SimpleSchemaGenerator.Schema.Elements.Statements.Statement import Statement
from SimpleSchemaGenerator import Errors


# ----------------------------------------------------------------------
class ParseIncludeStatementType(Enum):
    """Specifies the type of include statement encountered during parsing"""

    # from <directory> import <filename_stem>
    Module = auto()

    # from <filename> import <name_or_names>
    Package = auto()

    # from <filename> import *
    Star = auto()


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ParseIncludeStatementItem(Element):
    """Named import item"""

    # ----------------------------------------------------------------------
    element_name: ParseIdentifier
    reference_name: ParseIdentifier

    # ----------------------------------------------------------------------
    def __post_init__(self) -> None:
        if not self.element_name.is_type:
            raise Errors.SimpleSchemaGeneratorError(
                Errors.ParseIncludeStatementItemNotType.Create(
                    self.element_name.region, self.element_name.value
                )
            )

        if not self.reference_name.is_type:
            raise Errors.SimpleSchemaGeneratorError(
                Errors.ParseIncludeStatementItemReferenceNotType.Create(
                    self.reference_name.region,
                    self.reference_name.value,
                )
            )

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from super()._GenerateAcceptDetails()

        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "element_name",
            self.element_name,
        )

        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "reference_name",
            self.reference_name,
        )


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ParseIncludeStatement(Statement):
    """Statement that includes content from another file."""

    # ----------------------------------------------------------------------
    include_type: ParseIncludeStatementType

    filename: TerminalElement[Path]
    items: list[ParseIncludeStatementItem]  # Can be empty

    # ----------------------------------------------------------------------
    def __post_init__(self) -> None:
        if not self.filename.value.is_file():
            raise Errors.SimpleSchemaGeneratorError(
                Errors.ParseIncludeStatementInvalidFile.Create(self.filename.region, self.filename.value)
            )

        if self.include_type in [
            ParseIncludeStatementType.Module,
            ParseIncludeStatementType.Star,
        ]:
            if self.items:
                raise Errors.SimpleSchemaGeneratorError(
                    Errors.ParseIncludeStatementInvalidItems.Create(self.region)
                )
        elif self.include_type == ParseIncludeStatementType.Package:
            if not self.items:
                raise Errors.SimpleSchemaGeneratorError(
                    Errors.ParseIncludeStatementMissingItems.Create(self.region)
                )
        else:
            raise AssertionError(self.include_type)  # pragma: no cover

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from super()._GenerateAcceptDetails()

        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "filename",
            self.filename,
        )

        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "items",
            cast(list[Element], self.items),
        )
