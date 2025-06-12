# ----------------------------------------------------------------------
# |
# |  StructureStatement.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-20 18:05:24
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the StructureStatement object."""

from dataclasses import dataclass
from typing import cast, TYPE_CHECKING
from weakref import ReferenceType as WeakReferenceType

from dbrownell_Common.Types import override

from .Statement import Statement
from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element
from SimpleSchemaGenerator.Schema.Elements.Common.TerminalElement import TerminalElement
from SimpleSchemaGenerator.Schema.Elements.Common.UniqueNameTrait import UniqueNameTrait

if TYPE_CHECKING:
    from SimpleSchemaGenerator.Schema.Elements.Types.ReferenceType import ReferenceType  # pragma: no cover


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class StructureStatement(UniqueNameTrait, Statement):
    """The definition of a structure."""

    # ----------------------------------------------------------------------
    name: TerminalElement[str]
    base_types: list["ReferenceType"]  # Can be empty
    children: list[Statement]  # Can be empty

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "name",
            self.name,
        )

        if self.base_types:
            yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
                "base_types",
                cast(
                    list[WeakReferenceType[Element]],
                    self.base_types,  # TODO: [ref(base_type) for base_type in self.base_types],
                ),
            )

    # ----------------------------------------------------------------------
    @override
    def _GetAcceptChildren(self) -> Element._GetAcceptChildrenResultType:
        return Element._GetAcceptChildrenResult(  # noqa: SLF001
            "children", cast(list[Element], self.children)
        )
