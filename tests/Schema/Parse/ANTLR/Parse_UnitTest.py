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
    from TestHelpers import TerminalElementVisitor, TestElementVisitor, YamlVisitor


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
            r"\#.*\n",
            lambda *args: "\n",
            scrubbed_content,
            flags=re.MULTILINE,
        )

        for replace_token in [
            "->",
            "::",
            ":",
            ",",
            "(",
            ")",
            "{",
            "}",
            "[",
            "]",
            "=",
            "pass",
        ]:
            scrubbed_content = scrubbed_content.replace(replace_token, "".ljust(len(replace_token)))

        scrubbed_content = "{}\n".format(
            "\n".join(line.rstrip() for line in scrubbed_content.splitlines())
        )

        # Compare
        assert generated_content == scrubbed_content

    # ----------------------------------------------------------------------
    def test_Cardinality(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Cardinality.SimpleSchema"))

    # ----------------------------------------------------------------------
    def test_Expressions(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Expressions.SimpleSchema"))

    # ----------------------------------------------------------------------
    def test_Extensions(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Extensions.SimpleSchema"))

    # ----------------------------------------------------------------------
    def test_Structures(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Structures.SimpleSchema"))


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

        assert visitor.yaml_string == snapshot

    # ----------------------------------------------------------------------
    def test_Cardinality(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Cardinality.SimpleSchema"), snapshot)

    # ----------------------------------------------------------------------
    def test_Expressions(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Expressions.SimpleSchema"), snapshot)

    # ----------------------------------------------------------------------
    def test_Extensions(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Extensions.SimpleSchema"), snapshot)

    # ----------------------------------------------------------------------
    def test_Structures(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Structures.SimpleSchema"), snapshot)


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
        return "\n".join("".join(line).rstrip() for line in self._content)

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
        cardinality = str(element).replace("[", " ").replace("]", " ")

        self._PopulateLine(element, cardinality)
        yield VisitResult.SkipAll

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnTerminalElement(self, element: TerminalElement) -> Iterator[VisitResult]:
        self._PopulateLine(element, str(element.value))
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnParseIdentifier(self, element: ParseIdentifier) -> Iterator[VisitResult]:
        self._PopulateLine(element, element.value)
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    # |
    # |  Expressions
    # |
    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnBooleanExpression(self, element: BooleanExpression) -> Iterator[VisitResult]:
        if element.flags & BooleanExpression.Flags.YesNo:
            if element.flags & BooleanExpression.Flags.SingleChar:
                value = "y" if element.value else "n"
            else:
                value = "yes" if element.value else "no"
        elif element.flags & BooleanExpression.Flags.TrueFalse:
            value = "true" if element.value else "false"
        elif element.flags & BooleanExpression.Flags.OnOff:
            value = "on" if element.value else "off"
        else:
            assert False, (element.flags, element.value)

        if element.flags & BooleanExpression.Flags.LowerCase:
            pass  # Nothing to do as the value is already lowercase
        elif element.flags & BooleanExpression.Flags.UpperCase:
            value = value.upper()
        elif element.flags & BooleanExpression.Flags.PascalCase:
            value = value.capitalize()
        else:
            assert False, (element.flags, element.value)

        self._PopulateLine(element, value)
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnIntegerExpression(self, element: IntegerExpression) -> Iterator[VisitResult]:
        self._PopulateLine(element, str(element.value))
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnNoneExpression(self, element: NoneExpression) -> Iterator[VisitResult]:
        self._PopulateLine(element, "None")
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnNumberExpression(self, element: NumberExpression) -> Iterator[VisitResult]:
        value = str(element.value)

        if (
            len(value) > element.region.end.column - element.region.begin.column
            and int(element.value) == 0
        ):
            value = value.replace("0.", ".")

        self._PopulateLine(element, value)
        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnStringExpression(self, element: StringExpression) -> Iterator[VisitResult]:
        if element.quote_type in [
            StringExpression.QuoteType.TripleSingle,
            StringExpression.QuoteType.TripleDouble,
        ]:
            # _PopulateLine only works for tokens on a single line but these tokens span
            # multiple lines. Handle the special processing here. Extract this functionality
            # to an new _PopulateLine-like method if we ever have the need to support other
            # multi-line tokens.
            if element.quote_type == StringExpression.QuoteType.TripleSingle:
                quote = "'''"
            elif element.quote_type == StringExpression.QuoteType.TripleDouble:
                quote = '"""'
            else:
                assert False, element.quote_type  # pragma: no cover

            # The first character of the token opening will already appear in the line, as we ensure
            # that the column starting point has the correct number of characters in OnElement.
            # However, we need to make sure that all characters associated with the opening of the
            # string appear on the line.
            line_content = self._content[element.region.begin.line - 1]

            line_content[-1] = quote[0]
            line_content += list(quote[1:])

            # Apply the content
            line_offset = 1

            indentation = " " * (element.region.begin.column - 1)

            for line in element.value.split("\n"):
                line_content = self._content[element.region.begin.line - 1 + line_offset]
                assert not line_content, line_content

                line_content += list(f"{indentation}{line}")
                line_offset += 1

            # Apply the string closing token
            line_content = self._content[element.region.end.line - 1]

            for index, char in enumerate(reversed(quote)):
                line_content[-index - 2] = char

        else:
            if element.quote_type == StringExpression.QuoteType.Single:
                value = "'{}'".format(element.value.replace("'", "\\'"))
            elif element.quote_type == StringExpression.QuoteType.Double:
                value = '"{}"'.format(element.value.replace('"', '\\"'))
            else:
                assert False, element.quote_type  # pragma: no cover

            self._PopulateLine(element, value)

        yield VisitResult.Continue

    # ----------------------------------------------------------------------
    # |
    # |  Types
    # |
    # ----------------------------------------------------------------------
    @contextmanager
    @override
    def OnParseIdentifierType(self, element: ParseIdentifierType) -> Iterator[VisitResult]:
        yield VisitResult.Continue

        last_index = len(element.identifiers) - 1

        if last_index != 0:
            line_content = self._content[element.region.begin.line - 1]

            for index, identifier in enumerate(element.identifiers):
                if index != last_index:
                    line_content[identifier.region.end.column - 1] = "."

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def _PopulateLine(
        self,
        element: Element,
        value: str,
    ) -> None:
        line_content = self._content[element.region.begin.line - 1]

        for index in range(len(value)):
            line_content[element.region.begin.column - 1 + index] = value[index]


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
