# ----------------------------------------------------------------------
# |
# |  ElementVisitor.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-09 14:31:09
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains types used when creating Element visitors"""

from abc import ABC, abstractmethod
from contextlib import contextmanager
from enum import auto, Flag
from typing import Iterable, Iterator, TYPE_CHECKING, Union

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

if TYPE_CHECKING:
    from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element  # pragma: no cover


# ----------------------------------------------------------------------
class VisitResult(Flag):
    """Result returned during visitation that controls the visitation of other Elements."""

    # ----------------------------------------------------------------------
    Continue = 0

    SkipDetails = auto()
    SkipChildren = auto()

    Terminate = auto()

    # Amalgamations
    SkipAll = SkipDetails | SkipChildren


# ----------------------------------------------------------------------
class ElementVisitor(ABC):
    """Abstract base class for a visitor that accepts Elements"""

    # ----------------------------------------------------------------------
    @abstractmethod
    @contextmanager
    def OnElement(
        self,
        element: "Element",
    ) -> Iterator[VisitResult]:
        raise Exception("Abstract method")  # pragma: no cover

    # ----------------------------------------------------------------------
    @abstractmethod
    @contextmanager
    def OnElementDetails(
        self,
        element: "Element",
    ) -> Iterator[VisitResult]:
        raise Exception("Abstract method")  # pragma: no cover

    # ----------------------------------------------------------------------
    @abstractmethod
    @contextmanager
    def OnElementChildren(
        self,
        element: "Element",
        children_name: str,
        children: Iterable["Element"],
    ) -> Iterator[VisitResult]:
        raise Exception("Abstract method")  # pragma: no cover

    # ----------------------------------------------------------------------
    # Derived classes should implement the following methods:
    #
    #   @contextmanager On<Element Name>(element) -> Iterator[VisitResult]
    #   On<Element Name>__<Detail Name>(element_or_elements, include_disabled) -> VisitResult
    #


# ----------------------------------------------------------------------
class ElementVisitorHelper(ElementVisitor):
    """Base class that makes writing custom visitors easier by providing default implementations of all visitation methods"""

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnElement(
        self,
        element: "Element",  # pylint: disable=unused-argument
    ) -> Iterator[VisitResult]:
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnElementDetails(
        self,
        element: "Element",  # pylint: disable=unused-argument
    ) -> Iterator[VisitResult]:
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnElementChildren(
        self,
        element: "Element",  # pylint: disable=unused-argument
        children_name: str,  # pylint: disable=unused-argument
        children: Iterable["Element"],  # pylint: disable=unused-argument
    ) -> Iterator[VisitResult]:
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    def __getattr__(
        self,
        method_name: str,
    ):
        index = method_name.find("__")
        if index != -1 and index + len("__") + 1 < len(method_name):
            return self._DefaultDetailMethod

        return self.__class__._DefaultElementMethod  # pylint: disable=protected-access

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @staticmethod
    @contextmanager
    def _DefaultElementMethod(
        *args, **kwargs  # pylint: disable=unused-argument
    ) -> Iterator[VisitResult]:
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    def _DefaultDetailMethod(
        self,
        element_or_elements: Union["Element", list["Element"]],
        *,
        include_disabled: bool,
    ) -> VisitResult:
        if isinstance(element_or_elements, list):
            for element in element_or_elements:
                result = element.Accept(
                    self,
                    include_disabled=include_disabled,
                )

                if result & VisitResult.Terminate:
                    return result
        else:
            result = element_or_elements.Accept(
                self,
                include_disabled=include_disabled,
            )

            if result & VisitResult.Terminate:
                return result

        return VisitResult.Continue
