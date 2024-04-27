# ----------------------------------------------------------------------
# |
# |  Parse_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-20 17:56:22
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Parse.py."""

import re
import sys

from contextlib import contextmanager
from pathlib import Path, PurePath
from typing import Callable, cast, Iterator, Optional

from dbrownell_Common import PathEx
from dbrownell_Common.Streams.DoneManager import DoneManager
from dbrownell_Common.TestHelpers.StreamTestHelpers import GenerateDoneManagerAndContent
from dbrownell_Common.Types import override

from SimpleSchemaGenerator.Schema.Parse.ANTLR.Parse import *
from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element
from SimpleSchemaGenerator.Schema.Visitors.ElementVisitor import VisitResult

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TerminalElementVisitor, TestElementVisitor, ToYamlString, YamlVisitor


# ----------------------------------------------------------------------
sample_schemas = PathEx.EnsureDir(
    Path(__file__).parent.parent.parent.parent.parent
    / "src"
    / "SimpleSchemaGenerator"
    / "SampleSchemas"
)


# ----------------------------------------------------------------------
class TestRegions:
    # ----------------------------------------------------------------------
    @staticmethod
    def Execute(
        path: Path,
    ) -> None:
        # Parse the content
        root = _ExecuteSingle(path)

        # Generate the content from the regions
        visitor = _RegionVisitor()

        root.Accept(visitor)

        generated_content = visitor.content

        # Scrub the file content
        with path.open(encoding="utf-8") as f:
            scrubbed_content = f.read()

        # Remove comments
        scrubbed_content = re.sub(
            r"\s*#.*$",
            lambda *args: "",
            scrubbed_content,
            flags=re.MULTILINE,
        )

        for replace_char in ["->", "::", ":", ",", "(", ")", "{", "}"]:
            scrubbed_content = scrubbed_content.replace(replace_char, "".ljust(len(replace_char)))

        scrubbed_content = "\n".join(line.rstrip() for line in scrubbed_content.splitlines())

        # Compare
        assert generated_content == scrubbed_content

    # ----------------------------------------------------------------------
    def test_Cardinality(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Cardinality.SimpleSchema"))


# ----------------------------------------------------------------------
class TestParsing:
    # ----------------------------------------------------------------------
    @staticmethod
    def Execute(
        path: Path,
        snapshot,
    ) -> None:
        # Parse the content
        root = _ExecuteSingle(path)

        # Generate the content
        visitor = YamlVisitor()

        root.Accept(visitor)

        d = visitor.root

        assert ToYamlString(d) == snapshot

    # ----------------------------------------------------------------------
    def test_Cardinality(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Cardinality.SimpleSchema"), snapshot)


# ----------------------------------------------------------------------
# |
# |  Private Types
# |
# ----------------------------------------------------------------------
class _RegionVisitor(TerminalElementVisitor):
    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super(_RegionVisitor, self).__init__()
        self._content: list[list[str]] = []

    # ----------------------------------------------------------------------
    @property
    def content(self) -> str:
        return "\n".join("".join(line).rstrip() for line in self._content).rstrip()

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnElement(
        self,
        element: Element,
    ) -> Iterator[VisitResult]:
        if element.region.end.line > len(self._content):
            self._content.extend([] for _ in range(element.region.end.line - len(self._content)))

        # ----------------------------------------------------------------------
        def AdjustLine(
            line: list[str],
            location: Location,
        ) -> None:
            if location.column > len(line):
                line.extend(" " for _ in range(location.column - len(line)))

        # ----------------------------------------------------------------------

        AdjustLine(self._content[element.region.begin.line - 1], element.region.begin)
        AdjustLine(self._content[element.region.end.line - 1], element.region.end)

        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnCardinality(self, element: Cardinality) -> Iterator[VisitResult]:
        value = str(element)

        line_content = self._content[element.region.begin.line - 1]

        for index in range(len(value)):
            line_content[element.region.begin.column - 1 + index] = value[index]

        yield VisitResult.SkipAll

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnTerminalElement(self, element: TerminalElement) -> Iterator[VisitResult]:
        value = str(element.value)

        line_content = self._content[element.region.begin.line - 1]

        for index in range(len(value)):
            line_content[element.region.begin.column - 1 + index] = value[index]

        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnParseIdentifier(self, element: ParseIdentifier) -> Iterator[VisitResult]:
        assert element.region.begin.line == element.region.end.line
        assert element.region.end.column - element.region.begin.column == len(element.value)

        line_content = self._content[element.region.begin.line - 1]

        for index in range(len(element.value)):
            line_content[element.region.begin.column - 1 + index] = element.value[index]

        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnIntegerExpression(self, element: IntegerExpression) -> Iterator[VisitResult]:
        value = str(element.value)

        line_content = self._content[element.region.begin.line - 1]

        for index in range(len(value)):
            line_content[element.region.begin.column - 1 + index] = value[index]

        yield VisitResult.Continue


# ----------------------------------------------------------------------
# |
# |  Private Functions
# |
# ----------------------------------------------------------------------
def _Execute(
    workspaces: dict[
        Path,  # workspace root
        dict[
            PurePath,  # relative path
            Callable[[], str],  # get content
        ],
    ],
    *,
    single_threaded: bool = False,
    quiet: bool = False,
    raise_if_single_exception: bool = True,
    expected_result: int = 0,
    expected_content: Optional[str] = None,
) -> dict[
    Path,  # workspace root
    dict[
        PurePath,  # relative path
        Exception | RootStatement,
    ],
]:
    dm_and_content = GenerateDoneManagerAndContent()

    dm = cast(DoneManager, next(dm_and_content))

    result = Parse(
        dm,
        workspaces,
        single_threaded=single_threaded,
        quiet=quiet,
        raise_if_single_exception=raise_if_single_exception,
    )

    assert dm.result == expected_result

    if expected_content is not None:
        content = cast(str, next(dm_and_content))
        assert content == expected_content

    return result


# ----------------------------------------------------------------------
def _ExecuteSingle(
    schema_filename: Path,
) -> RootStatement:
    with schema_filename.open(encoding="utf-8") as f:
        content = f.read()

    result = _Execute({schema_filename.parent: {PurePath(schema_filename.name): lambda: content}})

    assert len(result) == 1
    result = next(iter(result.values()))

    assert len(result) == 1
    result = next(iter(result.values()))

    assert isinstance(result, RootStatement), result
    return result
