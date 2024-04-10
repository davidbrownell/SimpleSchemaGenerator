# ----------------------------------------------------------------------
# |
# |  TestHelperVisitor_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 11:58:01
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for TestHelperVisitor.py"""

from dataclasses import dataclass
from unittest.mock import Mock

from dbrownell_Common.Types import override

from SimpleSchemaGenerator.Schema.Common.Element import Element
from SimpleSchemaGenerator.Schema.Common.TerminalElement import TerminalElement
from SimpleSchemaGenerator.Schema.Visitors.TestHelperVisitor import TestHelperVisitor


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class MyElement(Element):
    """Element used for testing"""

    # ----------------------------------------------------------------------
    name: TerminalElement[str]
    value: TerminalElement[int]
    values: list[Element]

    unusual_child_name: list[Element]

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem("name", self.name)
        yield Element._GenerateAcceptDetailsItem("value", self.value)
        yield Element._GenerateAcceptDetailsItem("values", self.values)

    # ----------------------------------------------------------------------
    @override
    def _GetAcceptChildren(self) -> Element._GetAcceptChildrenResultType:
        return Element._GetAcceptChildrenResult("unusual_child_name", self.unusual_child_name)


# ----------------------------------------------------------------------
def test_TestHelperVisitor():
    name = TerminalElement[str](Mock(), "name")
    value = TerminalElement[int](Mock(), 42)

    values1 = TerminalElement[int](Mock(), 1)
    values2 = TerminalElement[int](Mock(), 2)

    child1 = TerminalElement[str](Mock(), "child1")
    child2 = TerminalElement[str](Mock(), "child2")
    child3 = TerminalElement[str](Mock(), "child3")

    e = MyElement(Mock(), name, value, [values1, values2], [child1, child2, child3])

    visitor = TestHelperVisitor()

    e.Accept(visitor)

    assert visitor.queue == [
        e,
        ("name", name),
        name,
        ("value", value),
        value,
        ("values", [values1, values2]),
        values1,
        values2,
        "Push 'unusual_child_name'",
        child1,
        child2,
        child3,
        "Pop 'unusual_child_name'",
    ]
