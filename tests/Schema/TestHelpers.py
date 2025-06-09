# ----------------------------------------------------------------------
# |
# |  TestHelpers.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-23 15:03:54
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Helpers used when testing SimpleSchema elements."""

import sys
import threading
import types
import yaml

from contextlib import contextmanager
from functools import cached_property
from pathlib import Path
from typing import Any, Iterable, Iterator
from unittest.mock import Mock
from weakref import ref

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common.Types import extension, override

from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element
from SimpleSchemaGenerator.Schema.Elements.Common.TerminalElement import TerminalElement
from SimpleSchemaGenerator.Schema.Elements.Expressions.BooleanExpression import BooleanExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.NoneExpression import NoneExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.NumberExpression import NumberExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.StringExpression import StringExpression
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Common.ParseIdentifier import (
    ParseIdentifier,
)

from SimpleSchemaGenerator.Schema.Visitors.ElementVisitor import ElementVisitor, VisitResult


# ----------------------------------------------------------------------
def TestElementVisitor(
    element: Element,
) -> list[Element | tuple[str, Element | list[Element]]]:
    visitor = _SingleElementVisitor(element)

    element.Accept(visitor)
    return visitor.queue


# ----------------------------------------------------------------------
class TerminalElementVisitor(ElementVisitor):
    """Visitor that requires definitions for terminal nodes."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        self._terminal_element_lookup_map: dict[type, bool] = {}

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnElement(
        self,
        element: Element,
    ) -> Iterator[VisitResult]:
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnElementDetails(
        self,
        element: Element,
    ) -> Iterator[VisitResult]:
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnElementChildren(
        self,
        element: Element,
        children_name: str,
        children: Iterable["Element"],
    ) -> Iterator[VisitResult]:
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @extension
    def OnElementDetailsItem(
        self,
        member_name: str,
        element_or_elements: Element | list[Element],
    ) -> Iterator[VisitResult]:
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    def __getattr__(
        self,
        method_name: str,
    ):
        index = method_name.find("__")
        if index != -1 and index + len("__") + 1 < len(method_name):
            attribute_name = method_name[index + len("__") :]

            return lambda *args, **kwargs: self._DefaultDetailMethod(attribute_name, *args, **kwargs)

        return self._DefaultElementMethod

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @contextmanager
    def _DefaultElementMethod(
        self,
        element: Element,
    ) -> Iterator[VisitResult]:
        is_terminal_element = self._terminal_element_lookup_map.get(element.__class__, None)
        if is_terminal_element is None:
            is_terminal_element = (
                type(element)._GenerateAcceptDetails is Element._GenerateAcceptDetails  # noqa: SLF001
                and type(element)._GetAcceptChildren is Element._GetAcceptChildren  # noqa: SLF001
            )

            self._terminal_element_lookup_map[element.__class__] = is_terminal_element

        assert not is_terminal_element, (
            f"Terminal element '{element.__class__.__name__}' not handled in '{self.__class__.__name__}'."
        )

        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    def _DefaultDetailMethod(
        self,
        attribute_name: str,
        element_or_elements: Element | list[Element],
        *,
        include_disabled: bool,
    ) -> VisitResult:
        with self.OnElementDetailsItem(attribute_name, element_or_elements) as visit_result:
            if visit_result & VisitResult.Terminate:
                return visit_result

            if not visit_result & VisitResult.SkipDetails:
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


# ----------------------------------------------------------------------
class YamlVisitor(TerminalElementVisitor):
    """Writes elements to a dictionary for testing purposes."""

    # Prevent this class from being considered a test class
    __test__ = False

    # ----------------------------------------------------------------------
    def __init__(
        self,
        *,
        include_disabled_status: bool = False,
    ) -> None:
        super().__init__()

        self.include_disabled_status = include_disabled_status

        self._stack: list[dict[str, Any]] = []
        self._display_type_as_reference: bool = False

    # ----------------------------------------------------------------------
    @cached_property
    def yaml_string(self) -> str:
        global _global_monkey_patched_dumper  # pylint: disable=global-statement

        with _global_monkey_patched_dumper_lock:
            if _global_monkey_patched_dumper is None:
                _global_monkey_patched_dumper = _MonkeyPatchedDumper()

        assert len(self._stack) == 1, self._stack
        return _global_monkey_patched_dumper(self._stack)

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnElement(
        self,
        element: Element,
    ) -> Iterator[VisitResult]:
        self._stack.append(
            {
                "__type__": element.__class__.__name__,
            },
        )

        if self.include_disabled_status:
            self._stack[-1]["__disabled__"] = element.is_disabled__

        # TODO: if isinstance(element, UniqueNameTrait):
        # TODO:     pass

        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnElementChildren(
        self,
        element: Element,  # pylint: disable=unused-argument
        children_name: str,
        children: list[Element],  # pylint: disable=unused-argument
    ) -> Iterator[VisitResult]:
        prev_num_items = len(self._stack)

        yield VisitResult.Continue

        children_results = self._stack[prev_num_items:]
        self._stack = self._stack[:prev_num_items]

        d = self._stack[-1]

        d[children_name] = children_results

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnElementDetailsItem(
        self,
        member_name: str,
        element_or_elements: Element | list[Element],
    ) -> Iterator[VisitResult]:
        prev_num_items = len(self._stack)

        yield VisitResult.Continue

        items = self._stack[prev_num_items:]
        self._stack = self._stack[:prev_num_items]

        if not isinstance(element_or_elements, list):
            assert len(items) == 1
            items = items[0]

        self._stack[-1][member_name] = items

    # ----------------------------------------------------------------------
    # |
    # |  Common Elements
    # |
    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnTerminalElement(self, element: TerminalElement) -> Iterator[VisitResult]:
        d = self._stack[-1]

        value = element.value

        if isinstance(value, Path):
            value = value.as_posix()

        d["value"] = value

        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    # |
    # |  Expression Elements
    # |
    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnBooleanExpression(self, element: BooleanExpression) -> Iterator[VisitResult]:
        d = self._stack[-1]

        d["value"] = element.value

        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnIntegerExpression(self, element: IntegerExpression) -> Iterator[VisitResult]:
        d = self._stack[-1]

        d["value"] = element.value

        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnNoneExpression(self, element: NoneExpression) -> Iterator[VisitResult]:
        # Nothing to add
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnNumberExpression(self, element: NumberExpression) -> Iterator[VisitResult]:
        d = self._stack[-1]

        d["value"] = element.value

        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnStringExpression(self, element: StringExpression) -> Iterator[VisitResult]:
        d = self._stack[-1]

        d["value"] = element.value

        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    # |
    # |  Parse Elements
    # |
    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnParseIdentifier(self, element: ParseIdentifier) -> Iterator[VisitResult]:
        d = self._stack[-1]

        d["value"] = element.value

        yield VisitResult.Continue


# ----------------------------------------------------------------------
_global_monkey_patched_dumper = None
_global_monkey_patched_dumper_lock = threading.Lock()


# ----------------------------------------------------------------------
def ToYamlString(
    content: Any,
) -> str:
    global _global_monkey_patched_dumper  # pylint: disable=global-statement

    with _global_monkey_patched_dumper_lock:
        if _global_monkey_patched_dumper is None:
            _global_monkey_patched_dumper = _MonkeyPatchedDumper()

    return _global_monkey_patched_dumper(content)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
class _MonkeyPatchedDumper(object):
    # rtyaml is designed to round-trip python objects when yaml fails to do so. Unfortunately,
    # rtyaml hard-codes the loader and dumper used as a part of the process and the
    # hard-coded values are compiled binaries that look at content length to determine if
    # yaml complex keys are used or not. This introduces risk, as some content may be slightly
    # different on different machines (for example, filenames prior to scrubbing them for
    # consistency). This code will introduce monkey patches to ensure that rtyaml never
    # uses complex keys.

    # ----------------------------------------------------------------------
    def __init__(self):
        if "rtyaml" in sys.modules:
            raise Exception("This function must be called before rtyaml is imported.")

        # Monkey patch the content
        original_safe_loader = yaml.CSafeLoader
        original_dumper = yaml.CDumper

        yaml.CSafeLoader = yaml.SafeLoader
        yaml.CDumper = yaml.Dumper

        # ----------------------------------------------------------------------
        def RestorePatches():
            yaml.CSafeLoader = original_safe_loader
            yaml.CDumper = original_dumper

        # ----------------------------------------------------------------------

        with ExitStack(RestorePatches):
            import rtyaml

        # Create a dumper that never produces complex keys

        # ----------------------------------------------------------------------
        class CustomDumper(rtyaml.Dumper):
            """Dumper that forces the use of simple keys"""

            # ----------------------------------------------------------------------
            def __init__(self, *args, **kwargs):
                super().__init__(
                    *args,
                    **{
                        **kwargs,
                        **{
                            "width": 100000,
                        },
                    },
                )

            # ----------------------------------------------------------------------
            def check_simple_key(self):
                # Always use simple keys
                return True

        # ----------------------------------------------------------------------
        def CustomDumpFunc(
            data,
            stream=None,
            Dumper=rtyaml.Dumper,  # pylint: disable=unused-argument
            **kwargs,
        ):
            return yaml.dump(data, stream, CustomDumper, **kwargs)

        # ----------------------------------------------------------------------

        self._dump_func = lambda content: rtyaml.do_dump(content, None, CustomDumpFunc)

    # ----------------------------------------------------------------------
    def __call__(self, content):
        return self._dump_func(content)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
class _SingleElementVisitor(ElementVisitor):
    """\
    Writes visitation methods to a mock object. This is used by unit tests to verify an Element's
    visitation is implemented as expected.
    """

    # ----------------------------------------------------------------------
    def __init__(self, element_under_test: Element) -> None:
        super().__init__()

        self._element_under_test = element_under_test
        self.queue: list[Element | tuple[str, Element | list[Element]]] = []

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnElement(
        self,
        element: Element,
    ) -> Iterator[VisitResult]:
        if element is not self._element_under_test:
            yield VisitResult.SkipAll
            return

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
        self.queue.append((f"<children>: {children_name}", list(children)))
        yield VisitResult.SkipChildren

    # ----------------------------------------------------------------------
    def __getattr__(
        self,
        method_name: str,
    ):
        index = method_name.find("__")
        if index != -1 and index + len("__") + 1 < len(method_name):
            name = method_name[index + len("__") :]
            return types.MethodType(
                lambda self, *args, name=name, **kwargs: self._DefaultDetailMethod(  # noqa: SLF001
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
        *args,
        **kwargs,  # pylint: disable=unused-argument
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
        if isinstance(element_or_elements, ref):
            self.queue.append((detail_name, element_or_elements()))
            return VisitResult.Continue

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
