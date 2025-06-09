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
import textwrap

from contextlib import contextmanager
from pathlib import Path, PurePath
from typing import Callable, cast, Iterator

import pytest

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
    Path(__file__).parent.parent.parent.parent.parent / "src" / "SimpleSchemaGenerator" / "SampleSchemas"
)


# ----------------------------------------------------------------------
class TestRegions:
    # ----------------------------------------------------------------------
    @staticmethod
    def Execute(
        path: Path,
        *,
        expected_num_results: int = 1,
    ) -> None:
        # Parse the content
        root = _ExecuteSingleFile(path, expected_num_results=expected_num_results)

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
            "|",
            "pass",
        ]:
            scrubbed_content = scrubbed_content.replace(replace_token, "".ljust(len(replace_token)))

        scrubbed_content = "\n".join(line.rstrip() for line in scrubbed_content.splitlines())
        if scrubbed_content:
            scrubbed_content += "\n"

        # Compare
        assert generated_content == scrubbed_content

    # ----------------------------------------------------------------------
    def test_Cardinality(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Cardinality.SimpleSchema"))

    # ----------------------------------------------------------------------
    def test_Empty(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Empty.SimpleSchema"))

    # ----------------------------------------------------------------------
    def test_Expressions(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Expressions.SimpleSchema"))

    # ----------------------------------------------------------------------
    def test_Extensions(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Extensions.SimpleSchema"))

    # ----------------------------------------------------------------------
    @pytest.mark.skip("Import statements are not easily transformed back into text.")
    def test_Import(self):
        self.Execute(
            PathEx.EnsureFile(sample_schemas / "Import.SimpleSchema"),
            expected_num_results=4,
        )

    # ----------------------------------------------------------------------
    def test_Miscellaneous(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Miscellaneous.SimpleSchema"))

    # ----------------------------------------------------------------------
    def test_Structures(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Structures.SimpleSchema"))

    # ----------------------------------------------------------------------
    @pytest.mark.skip("Tabs are not supported by the function that recreates the content.")
    def test_Tabs(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Tabs.SimpleSchema"))

    # ----------------------------------------------------------------------
    def test_Tuples(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Tuples.SimpleSchema"))

    # ----------------------------------------------------------------------
    def test_Variants(self):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Variants.SimpleSchema"))


# ----------------------------------------------------------------------
class TestParsing:
    # ----------------------------------------------------------------------
    @staticmethod
    def Execute(
        path: Path,
        snapshot,
        *,
        expected_num_results: int = 1,
        yaml_content_decoration_func: Callable[[str], str] | None = None,
    ) -> None:
        # Parse the content
        root = _ExecuteSingleFile(path, expected_num_results=expected_num_results)

        # Generate the content
        visitor = YamlVisitor()

        root.Accept(visitor)

        yaml_string = visitor.yaml_string
        if yaml_content_decoration_func:
            yaml_string = yaml_content_decoration_func(yaml_string)

        assert yaml_string == snapshot

    # ----------------------------------------------------------------------
    def test_Cardinality(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Cardinality.SimpleSchema"), snapshot)

    # ----------------------------------------------------------------------
    def test_Empty(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Empty.SimpleSchema"), snapshot)

    # ----------------------------------------------------------------------
    def test_Expressions(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Expressions.SimpleSchema"), snapshot)

    # ----------------------------------------------------------------------
    def test_Extensions(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Extensions.SimpleSchema"), snapshot)

    # ----------------------------------------------------------------------
    def test_Import(self, snapshot):
        working_dir = PathEx.EnsureDir(Path(__file__).parent.parent.parent.parent.parent)
        working_dir_str = working_dir.as_posix()

        self.Execute(
            PathEx.EnsureFile(sample_schemas / "Import.SimpleSchema"),
            snapshot,
            expected_num_results=4,
            yaml_content_decoration_func=lambda content: content.replace(working_dir_str, "<working_dir>"),
        )

    # ----------------------------------------------------------------------
    def test_Miscellaneous(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Miscellaneous.SimpleSchema"), snapshot)

    # ----------------------------------------------------------------------
    def test_Structures(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Structures.SimpleSchema"), snapshot)

    # ----------------------------------------------------------------------
    def test_Tabs(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Tabs.SimpleSchema"), snapshot)

    # ----------------------------------------------------------------------
    def test_Tuples(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Tuples.SimpleSchema"), snapshot)

    # ----------------------------------------------------------------------
    def test_Variants(self, snapshot):
        self.Execute(PathEx.EnsureFile(sample_schemas / "Variants.SimpleSchema"), snapshot)


# ----------------------------------------------------------------------
class TestImport:
    # ----------------------------------------------------------------------
    @staticmethod
    @pytest.fixture
    def import_fs(fs):
        fs.create_file("one/A/Dir1/File.SimpleSchema")

        return fs

    # ----------------------------------------------------------------------
    @staticmethod
    @pytest.fixture
    def workspaces(import_fs) -> dict[Path, dict[PurePath, Callable[[], str]]]:
        return {
            Path("one"): {},
        }

    # ----------------------------------------------------------------------
    def test_ExplicitDir(self, import_fs, workspaces):
        workspaces[Path("<root>")] = {
            PurePath("TestFile.SimpleSchema"): lambda: textwrap.dedent(
                """\
                from A/Dir1/ import File
                """,
            ),
        }

        results = _Execute(workspaces)

        assert len(results) == 2
        assert Path("<root>").resolve() in results

        imported_data = results[Path("one").resolve()]

        assert len(imported_data) == 1
        assert PurePath("A/Dir1/File.SimpleSchema") in imported_data

    # ----------------------------------------------------------------------
    def test_ExplicitRootDir(self, import_fs, workspaces):
        workspaces[Path("<root>")] = {
            PurePath("TestFile.SimpleSchema"): lambda: textwrap.dedent(
                """\
                from /A/Dir1/ import File
                """,
            ),
        }

        results = _Execute(workspaces)

        assert len(results) == 2
        assert Path("<root>").resolve() in results

        imported_data = results[Path("one").resolve()]

        assert len(imported_data) == 1
        assert PurePath("A/Dir1/File.SimpleSchema") in imported_data

    # ----------------------------------------------------------------------
    def test_Filename(self, import_fs, workspaces):
        workspaces[Path("<root>")] = {
            PurePath("TestFile.SimpleSchema"): lambda: textwrap.dedent(
                """\
                from /A/Dir1/File import Object
                """,
            ),
        }

        results = _Execute(workspaces)

        assert len(results) == 2
        assert Path("<root>").resolve() in results

        imported_data = results[Path("one").resolve()]

        assert len(imported_data) == 1
        assert PurePath("A/Dir1/File.SimpleSchema") in imported_data

    # ----------------------------------------------------------------------
    def test_Star(self, import_fs, workspaces):
        workspaces[Path("<root>")] = {
            PurePath("TestFile.SimpleSchema"): lambda: textwrap.dedent(
                """\
                from A/Dir1/File import *
                """,
            ),
        }

        results = _Execute(workspaces)

        assert len(results) == 2
        assert Path("<root>").resolve() in results

        imported_data = results[Path("one").resolve()]

        assert len(imported_data) == 1
        assert PurePath("A/Dir1/File.SimpleSchema") in imported_data

    # ----------------------------------------------------------------------
    def test_InitialDot(self, import_fs, workspaces):
        import_fs.create_file("<root>/Import.SimpleSchema")

        workspaces[Path("<root>")] = {
            PurePath("TestFile.SimpleSchema"): lambda: textwrap.dedent(
                """\
                from ./Import import *
                """,
            ),
        }

        results = _Execute(workspaces)

        assert len(results) == 2

        data = results[Path("<root>").resolve()]

        assert len(data) == 2
        assert PurePath("TestFile.SimpleSchema") in data
        assert PurePath("Import.SimpleSchema") in data

    # ----------------------------------------------------------------------
    def test_RelativeImport(self, import_fs, workspaces):
        import_fs.create_file("<root>/Import.SimpleSchema")

        workspaces[Path("<root>")] = {
            PurePath("Dir1/Dir2/TestFile.SimpleSchema"): lambda: textwrap.dedent(
                """\
                from ../../Import import *
                """,
            ),
        }

        results = _Execute(workspaces)

        assert len(results) == 2

        data = results[Path("<root>").resolve()]

        assert len(data) == 2
        assert PurePath("Dir1/Dir2/TestFile.SimpleSchema") in data
        assert PurePath("Import.SimpleSchema") in data

    # ----------------------------------------------------------------------
    def test_ErrorDirectoryDoesNotExist(self, import_fs, workspaces):
        workspaces[Path("<root>")] = {
            PurePath("TestFile.SimpleSchema"): lambda: textwrap.dedent(
                """\
                from DoesNotExist/ import File
                """,
            ),
        }

        filename = (Path("<root>") / "TestFile.SimpleSchema").resolve()

        with pytest.raises(
            Exception,
            match=re.escape(
                f"'DoesNotExist' is not a valid directory. ({filename}, Ln 1, Col 6 -> Ln 1, Col 18)"
            ),
        ):
            _Execute(workspaces)

    # ----------------------------------------------------------------------
    def test_ErrorFileDoesNotExist(self, import_fs, workspaces):
        workspaces[Path("<root>")] = {
            PurePath("TestFile.SimpleSchema"): lambda: textwrap.dedent(
                """\
                from DoesNotExist import *
                """,
            ),
        }

        filename = (Path("<root>") / "TestFile.SimpleSchema").resolve()

        with pytest.raises(
            Exception,
            match=re.escape(
                f"'DoesNotExist' is not a valid filename. ({filename}, Ln 1, Col 6 -> Ln 1, Col 18)"
            ),
        ):
            _Execute(workspaces)

    # ----------------------------------------------------------------------
    def test_ErrorStarIncludeWithDir(self, import_fs, workspaces):
        workspaces[Path("<root>")] = {
            PurePath("TestFile.SimpleSchema"): lambda: textwrap.dedent(
                """\
                from A/Dir1/ import *
                """,
            ),
        }

        filename = (Path("<root>") / "TestFile.SimpleSchema").resolve()
        imported_directory = (Path("one") / "A" / "Dir1").resolve()

        with pytest.raises(
            Exception,
            match=re.escape(
                f"Filenames must be provided with wildcard imports; '{imported_directory}' is a directory. ({filename}, Ln 1, Col 1 -> Ln 2, Col 1)"
            ),
        ):
            _Execute(workspaces)

    # ----------------------------------------------------------------------
    def test_ErrorExplicitDirectoryInvalidFile(self, import_fs, workspaces):
        workspaces[Path("<root>")] = {
            PurePath("TestFile.SimpleSchema"): lambda: textwrap.dedent(
                """\
                from A/Dir1/ import DoesNotExist
                """,
            ),
        }

        filename = (Path("<root>") / "TestFile.SimpleSchema").resolve()

        with pytest.raises(
            Exception,
            match=re.escape(
                f"'DoesNotExist' is not a valid filename. ({filename}, Ln 1, Col 6 -> Ln 1, Col 33)"
            ),
        ):
            _Execute(workspaces)

    # ----------------------------------------------------------------------
    def test_ErrorInvalidWorkspace(self, import_fs, workspaces):
        import_fs.create_file("<root>/InvalidImport.SimpleSchema")

        workspaces[Path("<root>/Dir1")] = {
            PurePath("Dir2/TestFile.SimpleSchema"): lambda: textwrap.dedent(
                """\
                from ../../InvalidImport import *
                """,
            ),
        }

        filename = (Path("<root>") / "Dir1" / "Dir2" / "TestFile.SimpleSchema").resolve()
        included_filename = (Path("<root>") / "InvalidImport.SimpleSchema").resolve()

        with pytest.raises(
            Exception,
            match=re.escape(
                f"The included file '{included_filename}' is not a descendant of any workspace. ({filename}, Ln 1, Col 1 -> Ln 2, Col 1)",
            ),
        ):
            _Execute(workspaces)


# ----------------------------------------------------------------------
def test_ErrorInvalidSyntax():
    with pytest.raises(
        Exception,
        match=re.escape(
            f"no viable alternative at input 'value: String {{indentmetadata1: \"value\"newLinededentdedent' ({_SINGLE_CONTENT_FILENAME} <Ln 4, Col 1>)"
        ),
    ):
        _ExecuteSingleContent(
            textwrap.dedent(
                """\
                InvalidObject ->
                    value: String {
                        metadata1: "value"
                """,
            ),
        )


# ----------------------------------------------------------------------
def test_ErrorStringInvalidIndentation():
    with pytest.raises(
        Exception,
        match=re.escape(f"Invalid multiline string indentation. ({_SINGLE_CONTENT_FILENAME} <Ln 3, Col 14>)"),
    ):
        _ExecuteSingleContent(
            textwrap.dedent(
                """\
                Object {
                    metadata1: '''
                             Not valid
                               '''
                }
                """,
            ),
        )


# ----------------------------------------------------------------------
def test_ErrorStringInvalidOpeningToken():
    with pytest.raises(
        Exception,
        match=re.escape(
            f"Triple-quote delimiters that initiate multiline strings cannot have any content on the same line as the opening token. ({_SINGLE_CONTENT_FILENAME} <Ln 2, Col 18>)"
        ),
    ):
        _ExecuteSingleContent(
            textwrap.dedent(
                """\
                Object {
                    metadata: '''Invalid
                              '''
                }
                """,
            ),
        )


# ----------------------------------------------------------------------
def test_ErrorStringInvalidClosingToken():
    with pytest.raises(
        Exception,
        match=re.escape(
            f"Triple-quote delimiters that terminate multiline strings cannot have any content on the same line as the closing token. ({_SINGLE_CONTENT_FILENAME} <Ln 3, Col 15>)"
        ),
    ):
        _ExecuteSingleContent(
            textwrap.dedent(
                """\
                Object {
                    metadata: '''
                              Invalid'''
                }
                """,
            ),
        )


# ----------------------------------------------------------------------
def test_ErrorInvalidStructureBase():
    with pytest.raises(
        Exception,
        match=re.escape(
            f"Base types must be identifiers. ({_SINGLE_CONTENT_FILENAME}, Ln 1, Col 9 -> Ln 1, Col 27)"
        ),
    ):
        _ExecuteSingleContent(
            textwrap.dedent(
                """\
                Object: (Integer | Number) ->
                    pass
                """,
            ),
        )


# ----------------------------------------------------------------------
# |
# |  Private Types
# |
# ----------------------------------------------------------------------
class _RegionVisitor(TerminalElementVisitor):
    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__()
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
            raise AssertionError(element.flags, element.value)

        if element.flags & BooleanExpression.Flags.LowerCase:
            pass  # Nothing to do as the value is already lowercase
        elif element.flags & BooleanExpression.Flags.UpperCase:
            value = value.upper()
        elif element.flags & BooleanExpression.Flags.PascalCase:
            value = value.capitalize()
        else:
            raise AssertionError(element.flags, element.value)

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

        if len(value) > element.region.end.column - element.region.begin.column and int(element.value) == 0:
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
                raise AssertionError(element.quote_type)  # pragma: no cover

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
                raise AssertionError(element.quote_type)  # pragma: no cover

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
    expected_content: str | None = None,
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
def _ExecuteSingleFile(
    schema_filename: Path,
    *,
    expected_num_results: int = 1,
) -> RootStatement:
    with schema_filename.open(encoding="utf-8") as f:
        content = f.read()

    result = _Execute({schema_filename.parent: {PurePath(schema_filename.name): lambda: content}})

    assert len(result) == 1
    result = next(iter(result.values()))

    assert len(result) == expected_num_results
    result = next(iter(result.values()))

    assert isinstance(result, RootStatement), result
    return result


# ----------------------------------------------------------------------
_SINGLE_CONTENT_FILENAME = Path.cwd() / "Filename.SimpleSchema"


def _ExecuteSingleContent(
    content: str,
) -> RootStatement:
    result = _Execute(
        {_SINGLE_CONTENT_FILENAME.parent: {PurePath(_SINGLE_CONTENT_FILENAME.name): lambda: content}}
    )

    assert len(result) == 1
    result = next(iter(result.values()))

    assert len(result) == 1
    result = next(iter(result.values()))

    assert isinstance(result, RootStatement), result
    return result
