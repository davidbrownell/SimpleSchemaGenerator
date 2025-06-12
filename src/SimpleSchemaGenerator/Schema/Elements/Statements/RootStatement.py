# ----------------------------------------------------------------------
# |
# |  RootStatement.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-14 17:00:44
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the RootStatement object."""

from dataclasses import dataclass
from typing import cast

from dbrownell_Common.Types import override

from .Statement import Element, Statement
from SimpleSchemaGenerator import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class RootStatement(Statement):
    """Collection of statements associated with a translation unit"""

    # ----------------------------------------------------------------------
    statements: list[Statement]  # Can be empty

    # ----------------------------------------------------------------------
    def __post_init__(self) -> None:
        for statement in self.statements:
            if isinstance(statement, RootStatement):
                raise Errors.SimpleSchemaGeneratorError(
                    Errors.RootStatementInvalidNested.Create(statement.region)
                )

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GetAcceptChildren(self) -> Element._GetAcceptChildrenResultType:
        return Element._GetAcceptChildrenResult(  # noqa: SLF001
            "statements", cast(list[Element], self.statements)
        )
