# ----------------------------------------------------------------------
# |
# |  TestHelperVisitor.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 11:14:36
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the TestHelperVisitor class"""

import types

from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Iterable, Iterator
from unittest.mock import Mock

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .ElementVisitor import ElementVisitor, VisitResult
from ..Common.Element import Element


# ----------------------------------------------------------------------
@dataclass
class TestHelperVisitor(ElementVisitor):
    """Writes visitation methods to a mock object"""

    # Tell pytest that it shouldn't treat this class as a collection of tests
    __test__ = False

    # ----------------------------------------------------------------------
    queue: list[Element | tuple[str, Element | list[Element]] | str] = field(default_factory=list)

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnElement(
        self,
        element: Element,
    ) -> Iterator[VisitResult]:
        self.queue.append(element)
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnElementDetails(
        self,
        element: Element,  # pylint: disable=unused-argument
    ) -> Iterator[VisitResult]:
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnElementChildren(
        self,
        element: Element,  # pylint: disable=unused-argument
        children_name: str,
        children: Iterable[Element],  # pylint: disable=unused-argument
    ) -> Iterator[VisitResult]:
        self.queue.append(f"Push '{children_name}'")
        yield VisitResult.Continue
        self.queue.append(f"Pop '{children_name}'")

    # ----------------------------------------------------------------------
    def __getattr__(
        self,
        method_name: str,
    ):
        index = method_name.find("__")
        if index != -1 and index + len("__") + 1 < len(method_name):
            name = method_name[index + len("__") :]
            return types.MethodType(
                lambda self, *args, name=name, **kwargs: self._DefaultDetailMethod(  # pylint: disable=protected-access
                    name, *args, **kwargs
                ),
                self,
            )

        return self.__class__._DefaultElementMethod

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
        detail_name: str,
        element_or_elements: Element | list[Element],
        *,
        include_disabled: bool,
    ) -> VisitResult:
        self.queue.append((detail_name, element_or_elements))

        if isinstance(element_or_elements, Mock):
            pass
        elif isinstance(element_or_elements, list):
            for element in element_or_elements:
                element.Accept(
                    self,
                    include_disabled=include_disabled,
                )
        else:
            element_or_elements.Accept(
                self,
                include_disabled=include_disabled,
            )

        return VisitResult.Continue
