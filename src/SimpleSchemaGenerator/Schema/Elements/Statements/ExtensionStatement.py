# ----------------------------------------------------------------------
# |
# |  ExtensionStatement.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-20 16:57:29
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the ExtensionStatement object."""

from dataclasses import dataclass, field, InitVar
from typing import cast

from dbrownell_Common.Types import override

from .Statement import Element, Statement
from SimpleSchemaGenerator.Schema.Elements.Common.TerminalElement import TerminalElement
from SimpleSchemaGenerator.Schema.Elements.Expressions.Expression import Expression

from SimpleSchemaGenerator import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ExtensionStatementKeywordArg(Element):
    """Keyword argument associated with an extension statement."""

    # ----------------------------------------------------------------------
    name: TerminalElement[str]
    expression: Expression

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem("name", self.name)  # noqa: SLF001
        yield Element._GenerateAcceptDetailsItem("expression", self.expression)  # noqa: SLF001


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ExtensionStatement(Statement):
    """An extension statement that is processed by plugins."""

    # ----------------------------------------------------------------------
    name: TerminalElement[str]
    positional_args: list[Expression]

    keyword_args_param: InitVar[list[ExtensionStatementKeywordArg]]
    keyword_args: dict[str, ExtensionStatementKeywordArg] = field(init=False)

    # ----------------------------------------------------------------------
    def __post_init__(
        self,
        keyword_args_param: list[ExtensionStatementKeywordArg],
    ) -> None:
        keyword_args: dict[str, ExtensionStatementKeywordArg] = {}

        for keyword_arg in keyword_args_param:
            key = keyword_arg.name.value

            prev_value = keyword_args.get(key)
            if prev_value is not None:
                raise Errors.SimpleSchemaGeneratorError(
                    Errors.ExtensionStatementDuplicateKeywordArgError.Create(
                        keyword_arg.name.region,
                        key,
                        prev_value.name.region,
                    ),
                )

            keyword_args[key] = keyword_arg

        object.__setattr__(self, "keyword_args", keyword_args)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "name", self.name
        )
        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "positional_args", cast(list[Element], self.positional_args)
        )
        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "keyword_args", cast(list[Element], list(self.keyword_args.values()))
        )
