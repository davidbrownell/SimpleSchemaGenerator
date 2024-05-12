# ----------------------------------------------------------------------
# |
# |  Element.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-09 14:28:10
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Element object"""

from abc import ABC
from dataclasses import dataclass, field
from typing import Generator, Optional, Union
from weakref import ReferenceType as WeakReferenceType

from dbrownell_Common.Types import extension  # type: ignore[import-untyped]

from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator.Schema.Visitors.ElementVisitor import ElementVisitor, VisitResult


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Element(ABC):
    """Base class for all elements encountered during the parsing process."""

    # ----------------------------------------------------------------------
    # |
    # |  Public Data
    # |
    # ----------------------------------------------------------------------
    region: Region

    _disabled: bool = field(init=False, default=False)

    # ----------------------------------------------------------------------
    @property
    def is_disabled__(self) -> bool:
        return self._disabled

    # ----------------------------------------------------------------------
    def Disable(self) -> None:
        assert self.is_disabled__ is False
        object.__setattr__(self, "_disabled", True)

    # ----------------------------------------------------------------------
    def Accept(
        self,
        visitor: ElementVisitor,
        *,
        include_disabled: bool = False,
    ) -> VisitResult:
        if self.is_disabled__ and not include_disabled:
            return VisitResult.Continue

        with visitor.OnElement(self) as element_result:
            if element_result & VisitResult.Terminate:
                return element_result

            if element_result & VisitResult.SkipAll:
                return element_result

            method_name = f"On{self.__class__.__name__}"

            method = getattr(visitor, method_name, None)
            assert method is not None, method_name

            with method(self) as visit_result:
                if visit_result & VisitResult.Terminate:
                    return visit_result

                # Details
                if not visit_result & VisitResult.SkipDetails:
                    detail_items = list(self._GenerateAcceptDetails())

                    if detail_items:
                        with visitor.OnElementDetails(self) as details_visit_result:
                            if details_visit_result & VisitResult.Terminate:
                                return details_visit_result

                            if not details_visit_result & VisitResult.SkipDetails:
                                for detail_item in detail_items:
                                    detail_method_name = f"{method_name}__{detail_item.name}"

                                    detail_method = getattr(visitor, detail_method_name, None)
                                    assert detail_method is not None, detail_method_name

                                    detail_item_result = detail_method(
                                        detail_item.value,
                                        include_disabled=include_disabled,
                                    )

                                    if detail_item_result & VisitResult.Terminate:
                                        return detail_item_result

                                    if detail_item_result & VisitResult.SkipDetails:
                                        break

                # Children
                if not visit_result & VisitResult.SkipChildren:
                    children_info = self._GetAcceptChildren()

                    if children_info:
                        with visitor.OnElementChildren(
                            self,
                            children_info.children_name,
                            children_info.children,
                        ) as children_visit_result:
                            if children_visit_result & VisitResult.Terminate:
                                return children_visit_result

                            if not children_visit_result & VisitResult.SkipChildren:
                                for child in children_info.children:
                                    child_visit_result = child.Accept(
                                        visitor,
                                        include_disabled=include_disabled,
                                    )

                                    if child_visit_result & VisitResult.Terminate:
                                        return child_visit_result

                                    if child_visit_result & VisitResult.SkipChildren:
                                        break

                return visit_result

    # ----------------------------------------------------------------------
    # |
    # |  Protected Types
    # |
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class _GenerateAcceptDetailsItem:
        name: str
        value: Union[
            "Element",
            WeakReferenceType["Element"],
            list["Element"],
            list[WeakReferenceType["Element"]],
        ]

    _GenerateAcceptDetailsResultType = Generator[_GenerateAcceptDetailsItem, None, None]

    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class _GetAcceptChildrenResult:
        children_name: str
        children: list["Element"]

    _GetAcceptChildrenResultType = Optional[_GetAcceptChildrenResult]

    # ----------------------------------------------------------------------
    # |
    # |  Private Methods
    # |
    # ----------------------------------------------------------------------
    # TODO: Ensure all Elements invoke base classes
    @extension
    def _GenerateAcceptDetails(self) -> _GenerateAcceptDetailsResultType:
        # Nothing by default
        if False:  # pylint: disable=using-constant-test
            yield

    # ----------------------------------------------------------------------
    # TODO: Ensure all Elements invoke base classes
    @extension
    def _GetAcceptChildren(self) -> _GetAcceptChildrenResultType:
        # Nothing by default
        return None
