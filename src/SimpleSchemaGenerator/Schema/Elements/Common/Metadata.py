# ----------------------------------------------------------------------
# |
# |  Metadata.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 09:11:14
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Metadata and MetadataItem elements"""

from dataclasses import dataclass, field, InitVar

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .Element import Element
from .TerminalElement import TerminalElement
from ..Expressions.Expression import Expression
from .... import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class MetadataItem(Element):
    """Individual metadata item within a collection of metadata items"""

    # ----------------------------------------------------------------------
    name: TerminalElement[str]
    expression: Expression

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem("name", self.name)
        yield Element._GenerateAcceptDetailsItem("expression", self.expression)


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Metadata(Element):
    """Collection of metadata items"""

    # ----------------------------------------------------------------------
    items_param: InitVar[list[MetadataItem]]  # Can be an empty list
    items: dict[str, MetadataItem] = field(init=False)

    # ----------------------------------------------------------------------
    def __post_init__(
        self,
        items_param: list[MetadataItem],
    ) -> None:
        items: dict[str, MetadataItem] = {}

        for item in items_param:
            key = item.name.value

            prev_value = items.get(key, None)
            if prev_value is not None:
                raise Errors.SimpleSchemaGeneratorException(
                    Errors.MetadataItemDuplicated.Create(
                        item.name.region,
                        key,
                        prev_value.name.region,
                    ),
                )

            items[key] = item

        # Commit
        object.__setattr__(self, "items", items)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GetAcceptChildren(self) -> Element._GetAcceptChildrenResultType:
        return Element._GetAcceptChildrenResult("items", list(self.items.values()))
