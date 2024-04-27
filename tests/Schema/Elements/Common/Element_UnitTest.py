# ----------------------------------------------------------------------
# |
# |  Element_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 09:05:38
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Element.py"""

from contextlib import contextmanager
from dataclasses import dataclass
from typing import cast, Iterator
from unittest.mock import Mock

import pytest

from dbrownell_Common.Types import override

from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element
from SimpleSchemaGenerator.Schema.Visitors.ElementVisitor import ElementVisitor, VisitResult


# ----------------------------------------------------------------------
def test_Basics():
    region_mock = Mock()

    e = Element(region_mock)

    assert e.region is region_mock

    # Disable
    assert e.is_disabled__ is False
    e.Disable()
    assert e.is_disabled__ is True


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Element1(Element):
    value: str


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Element2(Element):
    value1: Element
    value2: Element

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem("value1", self.value1)
        yield Element._GenerateAcceptDetailsItem("value2", self.value2)


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ChildElement(Element):
    value: str


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Element3(Element):
    children: list[ChildElement]

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GetAcceptChildren(self) -> Element._GetAcceptChildrenResultType:
        return Element._GetAcceptChildrenResult("children", cast(list[Element], self.children))


# ----------------------------------------------------------------------
class Visitor(ElementVisitor):
    # ----------------------------------------------------------------------
    def __init__(
        self,
        *,
        terminate_on_element: bool = False,
        skip_all_on_element: bool = False,
        terminate_on_element_details: bool = False,
        skip_details_on_element_details: bool = False,
        terminate_on_element_children: bool = False,
        skip_children_on_element_children: bool = False,
        terminate_on_element1: bool = False,
        terminate_on_element2: bool = False,
        skip_details_on_element2: bool = False,
        terminate_on_element2_details: bool = False,
        skip_details_on_element2_details: bool = False,
        terminate_on_element3: bool = False,
        skip_children_on_element3: bool = False,
        terminate_on_element3_child: bool = False,
        skip_children_on_element3_child: bool = False,
    ):
        self.queue: list[Element] = []

        self.terminate_on_element = terminate_on_element
        self.skip_all_on_element = skip_all_on_element

        self.terminate_on_element_details = terminate_on_element_details
        self.skip_details_on_element_details = skip_details_on_element_details

        self.terminate_on_element_children = terminate_on_element_children
        self.skip_children_on_element_children = skip_children_on_element_children

        self.terminate_on_element1 = terminate_on_element1

        self.terminate_on_element2 = terminate_on_element2
        self.skip_details_on_element2 = skip_details_on_element2
        self.terminate_on_element2_details = terminate_on_element2_details
        self.skip_details_on_element2_details = skip_details_on_element2_details

        self.terminate_on_element3 = terminate_on_element3
        self.skip_children_on_element3 = skip_children_on_element3
        self.terminate_on_element3_child = terminate_on_element3_child
        self.skip_children_on_element3_child = skip_children_on_element3_child

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnElement(
        self,
        element: Element,
    ) -> Iterator[VisitResult]:
        self.queue.append(element)

        if self.terminate_on_element:
            result = VisitResult.Terminate
        elif self.skip_all_on_element:
            result = VisitResult.SkipAll
        else:
            result = VisitResult.Continue

        yield result

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnElementDetails(
        self,
        element: Element,
    ) -> Iterator[VisitResult]:
        if self.terminate_on_element_details:
            result = VisitResult.Terminate
        elif self.skip_details_on_element_details:
            result = VisitResult.SkipDetails
        else:
            result = VisitResult.Continue

        yield result

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnElementChildren(
        self,
        element: Element,
        children_name: str,
        children: list[Element],
    ) -> Iterator[VisitResult]:
        if self.terminate_on_element_children:
            result = VisitResult.Terminate
        elif self.skip_children_on_element_children:
            result = VisitResult.SkipChildren
        else:
            result = VisitResult.Continue

        yield result

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnElement1(
        self,
        element: Element1,
    ) -> Iterator[VisitResult]:
        if self.terminate_on_element1:
            result = VisitResult.Terminate
        else:
            result = VisitResult.Continue

        yield result

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnElement2(
        self,
        element: Element2,
    ) -> Iterator[VisitResult]:
        if self.terminate_on_element2:
            result = VisitResult.Terminate
        elif self.skip_details_on_element2:
            result = VisitResult.SkipDetails
        else:
            result = VisitResult.Continue

        yield result

    # ----------------------------------------------------------------------
    @override
    def OnElement2__value1(
        self,
        element: Element,
        *,
        include_disabled: bool,
    ) -> VisitResult:
        self.queue.append(element)

        if self.terminate_on_element2_details:
            return VisitResult.Terminate

        if self.skip_details_on_element2_details:
            return VisitResult.SkipDetails

        return VisitResult.Continue

    # ----------------------------------------------------------------------
    @override
    def OnElement2__value2(
        self,
        element: Element,
        *,
        include_disabled: bool,
    ) -> VisitResult:
        self.queue.append(element)
        return VisitResult.Continue

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnElement3(
        self,
        element: Element3,
    ) -> Iterator[VisitResult]:
        if self.terminate_on_element3:
            result = VisitResult.Terminate
        elif self.skip_children_on_element3:
            result = VisitResult.SkipChildren
        else:
            result = VisitResult.Continue

        yield result

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnChildElement(
        self,
        element: ChildElement,
    ) -> Iterator[VisitResult]:
        if self.terminate_on_element3_child:
            result = VisitResult.Terminate
        elif self.skip_children_on_element3_child:
            result = VisitResult.SkipChildren
        else:
            result = VisitResult.Continue

        yield result


# ----------------------------------------------------------------------
class TestVisitResult:
    # ----------------------------------------------------------------------
    @pytest.mark.parametrize("include_disabled", [False, True])
    def test_Standard(self, executor, include_disabled):
        visitor = Visitor()

        assert executor(visitor, include_disabled=include_disabled) == VisitResult.Continue

        expected = [
            executor.element1,
            executor.element2,
            executor.value1,
            executor.value2,
            executor.element3,
            executor.child1,
            executor.child2,
        ]

        if include_disabled:
            expected.append(executor.element4)

        assert visitor.queue == expected

    # ----------------------------------------------------------------------
    def test_TerminateOnElement(self, executor):
        visitor = Visitor(terminate_on_element=True)

        assert executor(visitor) == VisitResult.Terminate
        assert visitor.queue == [executor.element1]

    # ----------------------------------------------------------------------
    def test_SkipAllOnElement(self, executor):
        visitor = Visitor(skip_all_on_element=True)

        assert executor(visitor) == VisitResult.Continue

        assert visitor.queue == [
            executor.element1,
            executor.element2,
            executor.element3,
        ]

    # ----------------------------------------------------------------------
    def test_TerminateOnElementDetails(self, executor):
        visitor = Visitor(terminate_on_element_details=True)

        assert executor(visitor) == VisitResult.Terminate

        assert visitor.queue == [
            executor.element1,
            executor.element2,
        ]

    # ----------------------------------------------------------------------
    def test_SkipDetailsOnElementDetails(self, executor):
        visitor = Visitor(skip_details_on_element_details=True)

        assert executor(visitor) == VisitResult.Continue

        assert visitor.queue == [
            executor.element1,
            executor.element2,
            executor.element3,
            executor.child1,
            executor.child2,
        ]

    # ----------------------------------------------------------------------
    def test_TerminateOnElementChildren(self, executor):
        visitor = Visitor(terminate_on_element_children=True)

        assert executor(visitor, include_disabled=True) == VisitResult.Terminate
        assert visitor.queue == [
            executor.element1,
            executor.element2,
            executor.value1,
            executor.value2,
            executor.element3,
        ]

    # ----------------------------------------------------------------------
    def test_SkipChildrenOnElementChildren(self, executor):
        visitor = Visitor(skip_children_on_element_children=True)

        assert executor(visitor, include_disabled=True) == VisitResult.Continue

        assert visitor.queue == [
            executor.element1,
            executor.element2,
            executor.value1,
            executor.value2,
            executor.element3,
            executor.element4,
        ]

    # ----------------------------------------------------------------------
    def test_TerminateOnElement1(self, executor):
        visitor = Visitor(terminate_on_element1=True)

        assert executor(visitor) == VisitResult.Terminate
        assert visitor.queue == [executor.element1]

    # ----------------------------------------------------------------------
    def test_TerminateOnElement2(self, executor):
        visitor = Visitor(terminate_on_element2=True)

        assert executor(visitor) == VisitResult.Terminate
        assert visitor.queue == [executor.element1, executor.element2]

    # ----------------------------------------------------------------------
    def test_SkipDetailsOnElement2(self, executor):
        visitor = Visitor(skip_details_on_element2=True)

        assert executor(visitor) == VisitResult.Continue

        assert visitor.queue == [
            executor.element1,
            executor.element2,
            executor.element3,
            executor.child1,
            executor.child2,
        ]

    # ----------------------------------------------------------------------
    def test_TerminateOnElement2Details(self, executor):
        visitor = Visitor(terminate_on_element2_details=True)

        assert executor(visitor) == VisitResult.Terminate

        assert visitor.queue == [
            executor.element1,
            executor.element2,
            executor.value1,
        ]

    # ----------------------------------------------------------------------
    def test_SkipDetailsOnElement2Details(self, executor):
        visitor = Visitor(skip_details_on_element2_details=True)

        assert executor(visitor) == VisitResult.Continue

        assert visitor.queue == [
            executor.element1,
            executor.element2,
            executor.value1,
            executor.element3,
            executor.child1,
            executor.child2,
        ]

    # ----------------------------------------------------------------------
    def test_TerminateOnElement3(self, executor):
        visitor = Visitor(terminate_on_element3=True)

        assert executor(visitor, include_disabled=True) == VisitResult.Terminate
        assert visitor.queue == [
            executor.element1,
            executor.element2,
            executor.value1,
            executor.value2,
            executor.element3,
        ]

    # ----------------------------------------------------------------------
    def test_SkipChildrenOnElement3(self, executor):
        visitor = Visitor(skip_children_on_element3=True)

        assert executor(visitor, include_disabled=True) == VisitResult.Continue

        assert visitor.queue == [
            executor.element1,
            executor.element2,
            executor.value1,
            executor.value2,
            executor.element3,
            executor.element4,
        ]

    # ----------------------------------------------------------------------
    def test_TerminateOnElement3Child(self, executor):
        visitor = Visitor(terminate_on_element3_child=True)

        assert executor(visitor, include_disabled=True) == VisitResult.Terminate
        assert visitor.queue == [
            executor.element1,
            executor.element2,
            executor.value1,
            executor.value2,
            executor.element3,
            executor.child1,
        ]

    # ----------------------------------------------------------------------
    def test_SkipChildrenOnElement3Child(self, executor):
        visitor = Visitor(skip_children_on_element3_child=True)

        assert executor(visitor, include_disabled=True) == VisitResult.Continue

        assert visitor.queue == [
            executor.element1,
            executor.element2,
            executor.value1,
            executor.value2,
            executor.element3,
            executor.child1,
            executor.element4,
        ]


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
@pytest.fixture
def executor():
    # ----------------------------------------------------------------------
    class Executor:
        # ----------------------------------------------------------------------
        def __init__(self):
            self.element1 = Element1(Mock(), "Element1")

            self.value1 = Element1(Mock(), "Element2A")
            self.value2 = Element1(Mock(), "Element2B")
            self.element2 = Element2(Mock(), self.value1, self.value2)

            self.child1 = ChildElement(Mock(), "Child1")
            self.child2 = ChildElement(Mock(), "Child2")
            self.element3 = Element3(Mock(), [self.child1, self.child2])

            self.element4 = Element1(Mock(), "Element4")
            self.element4.Disable()

        # ----------------------------------------------------------------------
        def __call__(
            self,
            visitor,
            *,
            include_disabled: bool = False,
        ) -> VisitResult:
            for element in [self.element1, self.element2, self.element3, self.element4]:
                result = element.Accept(visitor, include_disabled=include_disabled)
                if result & VisitResult.Terminate:
                    return result

            return VisitResult.Continue

    # ----------------------------------------------------------------------

    return Executor()
