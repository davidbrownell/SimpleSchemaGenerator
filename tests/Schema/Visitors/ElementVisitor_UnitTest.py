# ----------------------------------------------------------------------
# |
# |  ElementVisitor_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 09:06:42
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
# """Unit tests for ElementVisitor.py"""

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator
from unittest.mock import Mock

from dbrownell_Common.Types import override

from SimpleSchemaGenerator.Schema.Elements.Common.TerminalElement import Element, TerminalElement
from SimpleSchemaGenerator.Schema.Visitors.ElementVisitor import ElementVisitorHelper, VisitResult


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Element1(Element):
    value: str


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Element2(Element):
    value: Element

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem("value", self.value)


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Element3(Element):
    values: list[Element]

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem("values", self.values)


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Elements(Element):
    elements: list[Element]

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GetAcceptChildren(self) -> Element._GetAcceptChildrenResultType:
        return Element._GetAcceptChildrenResult("elements", self.elements)


# ----------------------------------------------------------------------
def test_ElementVisitorHelper():
    e = Elements(Mock(), [Element1(Mock(), "value1"), Element2(Mock(), TerminalElement[int](Mock(), 2))])

    e.Accept(ElementVisitorHelper())


# ----------------------------------------------------------------------
def test_CustomVisitor():
    e = Elements(
        Mock(),
        [
            Element1(Mock(), "value1"),
            Element2(Mock(), TerminalElement[int](Mock(), 2)),
            Element3(
                Mock(),
                [
                    TerminalElement[str](Mock(), "values_1"),
                    TerminalElement[str](Mock(), "values_2"),
                ],
            ),
        ],
    )

    # ----------------------------------------------------------------------
    class Visitor(ElementVisitorHelper):
        # ----------------------------------------------------------------------
        def __init__(self):
            self.value = 0

        # ----------------------------------------------------------------------
        @override
        @contextmanager
        def OnElements(self, element: Elements) -> Iterator[VisitResult]:
            assert element is e
            self.value += 1
            yield VisitResult.Continue

        # ----------------------------------------------------------------------
        @override
        @contextmanager
        def OnElement1(self, element: Element1) -> Iterator[VisitResult]:
            assert element is e.elements[0]
            self.value += 10
            yield VisitResult.Continue

        # ----------------------------------------------------------------------
        @override
        @contextmanager
        def OnElement2(self, element: Element2) -> Iterator[VisitResult]:
            assert element is e.elements[1]
            self.value += 20
            yield VisitResult.Continue

        # ----------------------------------------------------------------------
        @override
        def OnElement2__value(
            self,
            element: TerminalElement[int],
            include_disabled: bool,
        ) -> VisitResult:
            assert element is e.elements[1].value
            self.value += 100
            return VisitResult.Continue

    # ----------------------------------------------------------------------

    visitor = Visitor()

    e.Accept(visitor)

    assert visitor.value == 131


# ----------------------------------------------------------------------
def test_ListTermination():
    # ----------------------------------------------------------------------
    class Visitor(ElementVisitorHelper):
        # ----------------------------------------------------------------------
        @override
        @contextmanager
        def OnElement1(self, element: Element1) -> Iterator[VisitResult]:
            yield VisitResult.Terminate

    # ----------------------------------------------------------------------

    e = Element3(Mock(), [Element1(Mock(), "value1")])

    assert e.Accept(Visitor()) == VisitResult.Terminate


# ----------------------------------------------------------------------
def test_ItemTermination():
    # ----------------------------------------------------------------------
    class Visitor(ElementVisitorHelper):
        # ----------------------------------------------------------------------
        @override
        @contextmanager
        def OnElement1(self, element: Element1) -> Iterator[VisitResult]:
            yield VisitResult.Terminate

    # ----------------------------------------------------------------------

    e = Element2(Mock(), Element1(Mock(), "value1"))

    assert e.Accept(Visitor()) == VisitResult.Terminate
