# ----------------------------------------------------------------------
# |
# |  Parse.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-14 16:53:06
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Functionality that parses SimpleSchema files via ANTLR"""

import itertools
import sys
import threading

from functools import cached_property
from pathlib import Path, PurePath
from typing import Any, Callable, cast, Optional, Protocol

import antlr4  # type: ignore[import-untyped]

from dbrownell_Common.ContextlibEx import ExitStack  # type: ignore[import-untyped]
from dbrownell_Common import ExecuteTasks  # type: ignore[import-untyped]
from dbrownell_Common import PathEx  # type: ignore[import-untyped]
from dbrownell_Common.Streams.DoneManager import DoneManager  # type: ignore[import-untyped]

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent / "GeneratedCode")))
with ExitStack(lambda: sys.path.pop(0)):
    from .GeneratedCode.SimpleSchemaLexer import SimpleSchemaLexer
    from .GeneratedCode.SimpleSchemaParser import SimpleSchemaParser
    from .GeneratedCode.SimpleSchemaVisitor import SimpleSchemaVisitor

from .Grammar.Elements.Common.ParseIdentifier import ParseIdentifier
from .Grammar.Elements.Statements.ParseItemStatement import ParseItemStatement
from .Grammar.Elements.Statements.ParseIncludeStatement import (
    ParseIncludeStatement,
    ParseIncludeStatementItem,
    ParseIncludeStatementType,
)
from .Grammar.Elements.Statements.ParseStructureStatement import ParseStructureStatement
from .Grammar.Elements.Types.ParseIdentifierType import ParseIdentifierType
from .Grammar.Elements.Types.ParseTupleType import ParseTupleType
from .Grammar.Elements.Types.ParseType import ParseType
from .Grammar.Elements.Types.ParseVariantType import ParseVariantType
from ...Elements.Common.Cardinality import Cardinality
from ...Elements.Common.Metadata import Metadata, MetadataItem
from ...Elements.Common.TerminalElement import TerminalElement
from ...Elements.Expressions.BooleanExpression import BooleanExpression
from ...Elements.Expressions.Expression import Expression
from ...Elements.Expressions.IntegerExpression import IntegerExpression
from ...Elements.Expressions.ListExpression import ListExpression
from ...Elements.Expressions.NoneExpression import NoneExpression
from ...Elements.Expressions.NumberExpression import NumberExpression
from ...Elements.Expressions.StringExpression import StringExpression
from ...Elements.Expressions.TupleExpression import TupleExpression
from ...Elements.Statements.ExtensionStatement import (
    ExtensionStatement,
    ExtensionStatementKeywordArg,
)
from ...Elements.Statements.RootStatement import RootStatement
from ...Elements.Statements.Statement import Statement
from .... import Errors
from ....Common.Region import Location, Region


# ----------------------------------------------------------------------
# |
# |  Public Types
# |
# ----------------------------------------------------------------------
class AntlrException(Exception):
    """Exception raised for parsing-related errors"""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        message: str,
        source: Path,
        line: int,
        column: int,
        ex: Optional[antlr4.RecognitionException],
    ):
        location = Location(line, column)

        super(AntlrException, self).__init__(f"{message} ({source} <{location}>")

        self.source = source
        self.location = location
        self.ex = ex


# ----------------------------------------------------------------------
DEFAULT_FILE_EXTENSIONS: list[str] = [
    ".SimpleSchema",
]


# ----------------------------------------------------------------------
# |
# |  Public Functions
# |
# ----------------------------------------------------------------------
def Parse(
    dm: DoneManager,
    workspaces: dict[
        Path,  # workspace_root
        dict[
            PurePath,  # relative_path
            Callable[[], str],  # get content
        ],
    ],
    file_extensions: Optional[list[str]] = None,
    *,
    single_threaded: bool = False,
    quiet: bool = False,
    raise_if_single_exception: bool = True,
) -> dict[
    Path,  # workspace root
    dict[
        PurePath,  # relative path
        Exception | RootStatement,
    ],
]:
    if file_extensions is None:
        file_extensions = DEFAULT_FILE_EXTENSIONS

    workspace_names: list[Path] = [workspace.resolve() for workspace in workspaces.keys()]

    # Sort the names so we search from the longest path to the shortest path
    workspace_names.sort(
        key=lambda value: len(str(value)),
        reverse=True,
    )

    # Prepare the results
    results: dict[
        Path,  # workspace root
        dict[
            PurePath,  # relative path
            None | Exception | RootStatement,
        ],
    ] = {}
    results_lock = threading.Lock()

    for workspace_root, sources in workspaces.items():
        these_results: dict[PurePath, None | Exception | RootStatement] = {}

        for relative_path in sources.keys():
            these_results[relative_path] = None

        results[workspace_root] = these_results

    # Enqueue the tasks
    with ExecuteTasks.YieldQueueExecutor(
        dm,
        "Parsing...",
        quiet=quiet,
        max_num_threads=1 if single_threaded else None,
    ) as enqueue_func:

        # TODO: # ----------------------------------------------------------------------
        # TODO: def ResolveIncludeFilename(
        # TODO:     path: Path,
        # TODO:     *,
        # TODO:     allow_directory: bool,
        # TODO: ) -> Optional[Path]:
        # TODO:     path = path.resolve()
        # TODO:
        # TODO:     if path.is_file() or (allow_directory and path.is_dir()):
        # TODO:         return path
        # TODO:
        # TODO:     for extension in file_extensions:
        # TODO:         potential_path = path.parent / (path.name + extension)
        # TODO:         if potential_path.is_file():
        # TODO:             return potential_path
        # TODO:
        # TODO:     return None
        # TODO:
        # ----------------------------------------------------------------------
        def CreateIncludeStatement(
            including_filename: Path,
            region: Region,
            filename_or_directory: TerminalElement[Path],
            items: list[ParseIncludeStatementItem],
            *,
            is_star_include: bool,
        ) -> ParseIncludeStatement:
            return None  # TODO: Remove me

        # TODO:     root: Optional[Path] = None
        # TODO:
        # TODO:     for potential_root in itertools.chain(
        # TODO:         [including_filename.parent],
        # TODO:         workspace_names,
        # TODO:     ):
        # TODO:         fullpath = ResolveIncludeFilename(
        # TODO:             potential_root / filename_or_directory.value,
        # TODO:             allow_directory=True,
        # TODO:         )
        # TODO:
        # TODO:         if fullpath is not None:
        # TODO:             root = fullpath
        # TODO:             break
        # TODO:
        # TODO:     if root is None:
        # TODO:         raise Errors.ParseCreateIncludeStatementInvalidPath.CreateAsException(
        # TODO:             filename_or_directory.region,
        # TODO:             filename_or_directory.value,
        # TODO:         )
        # TODO:
        # TODO:     filename: Optional[Path] = None
        # TODO:     filename_region: Optional[Region] = None
        # TODO:
        # TODO:     include_type: Optional[ParseIncludeStatementType] = None
        # TODO:
        # TODO:     if root.is_dir():
        # TODO:         if is_star_include:
        # TODO:             raise Errors.ParseCreateIncludeStatementDirWithStar.CreateAsException(
        # TODO:                 region, root
        # TODO:             )
        # TODO:
        # TODO:         if len(items) != 1:
        # TODO:             raise Errors.ParseCreateIncludeStatementTooManyItems.CreateAsException(
        # TODO:                 items[1].region
        # TODO:             )
        # TODO:
        # TODO:         filename = ResolveIncludeFilename(
        # TODO:             root / items[0].element_name.value,
        # TODO:             allow_directory=False,
        # TODO:         )
        # TODO:
        # TODO:         filename_region = Region(
        # TODO:             filename_or_directory.region.filename,
        # TODO:             filename_or_directory.region.begin,
        # TODO:             items[0].element_name.region.end,
        # TODO:         )
        # TODO:
        # TODO:         if filename is None:
        # TODO:             raise Errors.ParseCreateIncludeStatementInvalidFilename.CreateAsException(
        # TODO:                 filename_region, items[0].element_name.value
        # TODO:             )
        # TODO:
        # TODO:         include_type = ParseIncludeStatementType.Module
        # TODO:         items = []
        # TODO:
        # TODO:     else:
        # TODO:         if is_star_include:
        # TODO:             assert not items
        # TODO:             include_type = ParseIncludeStatementType.Star
        # TODO:         else:
        # TODO:             include_type = ParseIncludeStatementType.Package
        # TODO:
        # TODO:         filename = root
        # TODO:         filename_region = filename_or_directory.region
        # TODO:
        # TODO:     assert filename is not None
        # TODO:     assert filename.is_file(), filename
        # TODO:     assert filename_region is not None
        # TODO:     assert include_type is not None
        # TODO:
        # TODO:     # Get the workspace associated with the file
        # TODO:     workspace: Optional[Path] = None
        # TODO:
        # TODO:     for workspace_name in workspace_names:
        # TODO:         if PathEx.IsDescendant(filename, workspace_name):
        # TODO:             workspace = workspace_name
        # TODO:             break
        # TODO:
        # TODO:     if workspace is None:
        # TODO:         raise Errors.ParseCreateIncludeStatementInvalidWorkspace.CreateAsException(
        # TODO:             region, filename
        # TODO:         )
        # TODO:
        # TODO:     # Get the relative path for the workspace
        # TODO:     relative_path = PathEx.CreateRelativePath(workspace, filename)
        # TODO:     assert relative_path is not None
        # TODO:
        # TODO:     # Determine if this is a file that should be enqueued for parsing
        # TODO:     should_enqueue = False
        # TODO:
        # TODO:     with results_lock:
        # TODO:         workspace_results = results[workspace]
        # TODO:
        # TODO:         if relative_path not in workspace_results:
        # TODO:             workspace_results[relative_path] = None
        # TODO:             should_enqueue = True
        # TODO:
        # TODO:     if should_enqueue:
        # TODO:         # ----------------------------------------------------------------------
        # TODO:         def GetContent() -> str:
        # TODO:             with filename.open(encoding="utf-8") as f:
        # TODO:                 return f.read()
        # TODO:
        # TODO:         # ----------------------------------------------------------------------
        # TODO:
        # TODO:         enqueue_func(
        # TODO:             str(filename),
        # TODO:             lambda on_simple_status_func: PrepareTask(
        # TODO:                 workspace,
        # TODO:                 relative_path,
        # TODO:                 GetContent,
        # TODO:                 is_included_file=True,
        # TODO:             ),
        # TODO:         )
        # TODO:
        # TODO:     return ParseIncludeStatement(
        # TODO:         region,
        # TODO:         include_type,
        # TODO:         TerminalElement(filename_region, filename),
        # TODO:         items,
        # TODO:     )

        # ----------------------------------------------------------------------
        def PrepareTask(
            workspace_root: Path,
            relative_path: PurePath,
            content_func: Callable[[], str],
            *,
            is_included_file: bool,
        ) -> tuple[int, ExecuteTasks.YieldQueueExecutorTypes.ExecuteFuncType]:
            content = content_func()

            # ----------------------------------------------------------------------
            def Execute(
                status: ExecuteTasks.Status,
            ) -> Optional[str]:
                result: None | Exception | RootStatement = None

                # ----------------------------------------------------------------------
                def OnExit():
                    assert result is not None
                    assert results[workspace_root][relative_path] is None
                    results[workspace_root][relative_path] = result

                # ----------------------------------------------------------------------

                with ExitStack(OnExit):
                    try:
                        fullpath = workspace_root / relative_path

                        # Parse the object
                        antlr_stream = antlr4.InputStream(content)

                        lexer = SimpleSchemaLexer(antlr_stream)

                        # Initialize instance variables that we have explicitly added to the ANTLR
                        # grammar file
                        lexer.CustomInitialization()

                        tokens = antlr4.CommonTokenStream(lexer)

                        tokens.fill()

                        parser = SimpleSchemaParser(tokens)
                        parser.addErrorListener(_ErrorListener(fullpath))

                        ast = parser.entry_point__()
                        assert ast

                        visitor = _SimpleSchemaVisitor(
                            fullpath,
                            lambda line: cast(None, status.OnProgress(line, None)),
                            CreateIncludeStatement,
                            is_included_file=is_included_file,
                        )

                        ast.accept(visitor)

                        result = visitor.root

                    except Exception as ex:
                        result = ex
                        raise

                return None

            # ----------------------------------------------------------------------

            return len(content.split("\n")), Execute

        # ----------------------------------------------------------------------

        is_single_workspace = len(workspaces) == 1

        for workspace_root, sources in workspaces.items():
            for relative_path, content_func in sources.items():
                enqueue_func(
                    str(relative_path if is_single_workspace else workspace_root / relative_path),
                    lambda on_simple_status_func, workspace_root=workspace_root, relative_path=relative_path, content_func=content_func: PrepareTask(
                        workspace_root,
                        relative_path,
                        content_func,
                        is_included_file=False,
                    ),
                )

    if dm.result != 0 and raise_if_single_exception:
        exceptions: list[Exception] = []

        for workspace_results in results.values():
            for result in workspace_results.values():
                if isinstance(result, Exception):
                    exceptions.append(result)

        if len(exceptions) == 1:
            raise exceptions[0]

    for workspace_root, workspace_results in results.items():
        for relative_path, result in workspace_results.items():
            assert result is not None, (workspace_root, relative_path)

    return cast(dict[Path, dict[PurePath, Exception | RootStatement]], results)


# ----------------------------------------------------------------------
# |
# |  Private Types
# |
# ----------------------------------------------------------------------
class _ErrorListener(antlr4.DiagnosticErrorListener):
    # ----------------------------------------------------------------------
    def __init__(
        self,
        source: Path,
        *args,
        **kwargs,
    ):
        super(_ErrorListener, self).__init__(*args, **kwargs)

        self._source = source

    # ----------------------------------------------------------------------
    def syntaxError(
        self,
        recognizer: SimpleSchemaParser,  # pylint: disable=unused-argument
        offendingSymbol: antlr4.Token,  # pylint: disable=unused-argument
        line: int,
        column: int,
        msg: str,
        e: antlr4.RecognitionException,
    ):
        raise AntlrException(msg, self._source, line, column + 1, e)


# ----------------------------------------------------------------------
class _VisitorMixin:
    """Contains functionality that doesn't change when the grammar is regenerated"""

    # ----------------------------------------------------------------------
    # |
    # |  Public Types
    # |
    # ----------------------------------------------------------------------
    class CreateIncludeStatementFunc(Protocol):
        def __call__(
            self,
            include_path: Path,
            region: Region,
            filename_or_directory: TerminalElement[Path],
            items: list[ParseIncludeStatementItem],
            *,
            is_star_include: bool,
        ) -> ParseIncludeStatement: ...  # pragma: no cover

    # ----------------------------------------------------------------------
    # |
    # |  Public Methods
    # |
    # ----------------------------------------------------------------------
    def __init__(
        self,
        filename: Path,
        on_progress_func: Callable[[int], None],
        create_include_statement_func: "_VisitorMixin.CreateIncludeStatementFunc",
        *,
        is_included_file: bool,
    ):
        self.filename = filename
        self.is_included_file = is_included_file

        self._on_progress_func = on_progress_func
        self._create_include_statement_func = create_include_statement_func

        self._current_line: int = 0
        self._stack: list[Any] = []

    # ----------------------------------------------------------------------
    @cached_property
    def root(self) -> RootStatement:
        if not self._stack:
            region = Region(self.filename, Location(1, 1), Location(1, 1))
        else:
            region = Region(
                self.filename,
                self._stack[0].region.begin,
                self._stack[-1].region.end,
            )

        assert all(isinstance(item, Statement) for item in self._stack)
        return RootStatement(region, cast(list[Statement], self._stack))

    # ----------------------------------------------------------------------
    def CreateRegion(
        self,
        ctx: antlr4.ParserRuleContext,
    ) -> Region:
        assert isinstance(ctx.start, antlr4.Token), ctx.start
        assert isinstance(ctx.stop, antlr4.Token), ctx.stop

        if ctx.stop.type == SimpleSchemaParser.DEDENT:
            stop_line = ctx.stop.line
            stop_col = ctx.stop.column
        elif ctx.stop.type == SimpleSchemaParser.NEWLINE and ctx.stop.text == "newLine":
            stop_line = ctx.stop.line

            if ctx.stop.line == ctx.start.line:
                # This is the scenario where the statement is followed by a dedent followed by another
                # statement. We don't want the range of this item to overlap with the range of the next
                # item, so use the values as they are, even though it means that a statement that
                # terminates with a newline will not have that newline here.
                stop_col = ctx.stop.column
            else:
                stop_col = ctx.stop.column if ctx.stop.column == 0 else ctx.start.column
        else:
            content = ctx.stop.text
            lines = content.split("\n")
            num_lines = len(lines)

            if ctx.stop.type == SimpleSchemaParser.NEWLINE:
                assert content.startswith("\n"), content
                assert num_lines == 2, lines

            stop_line = ctx.stop.line + num_lines - 1
            stop_col = len(lines[-1])

            if num_lines == 1:
                stop_col += ctx.stop.column

        self._OnProgress(stop_line)

        return Region(
            self.filename,
            Location(ctx.start.line, ctx.start.column + 1),
            Location(stop_line, stop_col + 1),
        )

    # ----------------------------------------------------------------------
    # |
    # |  Protected Methods
    # |
    # ----------------------------------------------------------------------
    def _GetChildren(self, ctx) -> list[Any]:
        prev_num_stack_items = len(self._stack)

        cast(SimpleSchemaVisitor, self).visitChildren(ctx)

        results = self._stack[prev_num_stack_items:]
        del self._stack[prev_num_stack_items:]

        return results

    # ----------------------------------------------------------------------
    def _OnProgress(
        self,
        end_line: int,
    ) -> None:
        if end_line > self._current_line:
            self._current_line = end_line
            self._on_progress_func(self._current_line)


# ----------------------------------------------------------------------
class _SimpleSchemaVisitor(SimpleSchemaVisitor, _VisitorMixin):
    # ----------------------------------------------------------------------
    # |
    # |  Common
    # |
    # ----------------------------------------------------------------------
    def visitIdentifier(self, ctx: SimpleSchemaParser.IdentifierContext):
        region = self.CreateRegion(ctx)
        value = ctx.IDENTIFIER().symbol.text

        self._stack.append(ParseIdentifier(region, value))

    # ----------------------------------------------------------------------
    def visitMetadata_clause(self, ctx: SimpleSchemaParser.Metadata_clauseContext):
        children = self._GetChildren(ctx)
        assert all(isinstance(child, MetadataItem) for child in children), children

        self._stack.append(Metadata(self.CreateRegion(ctx), cast(list[MetadataItem], children)))

    # ----------------------------------------------------------------------
    def visitMetadata_clause_item(self, ctx: SimpleSchemaParser.Metadata_clause_itemContext):
        children = self._GetChildren(ctx)

        assert len(children) == 2, children
        assert isinstance(children[0], ParseIdentifier), children
        assert isinstance(children[1], Expression), children

        name = children[0].ToTerminalElement()
        value = children[1]

        self._stack.append(MetadataItem(self.CreateRegion(ctx), name, value))

    # ----------------------------------------------------------------------
    def visitCardinality_clause(self, ctx: SimpleSchemaParser.Cardinality_clauseContext):
        children = self._GetChildren(ctx)

        assert len(children) == 2, children

        assert isinstance(children[0], IntegerExpression), children
        min_expression = cast(IntegerExpression, children[0])

        assert children[1] is None or isinstance(children[1], IntegerExpression), children
        max_expression = cast(Optional[IntegerExpression], children[1])

        self._stack.append(Cardinality(self.CreateRegion(ctx), min_expression, max_expression))

    # ----------------------------------------------------------------------
    def visitCardinality_clause_optional(
        self, ctx: SimpleSchemaParser.Cardinality_clause_optionalContext
    ):
        region = self.CreateRegion(ctx)

        self._stack += [IntegerExpression(region, 0), IntegerExpression(region, 1)]

    # ----------------------------------------------------------------------
    def visitCardinality_clause_zero_or_more(
        self, ctx: SimpleSchemaParser.Cardinality_clause_zero_or_moreContext
    ):
        self._stack += [IntegerExpression(self.CreateRegion(ctx), 0), None]

    # ----------------------------------------------------------------------
    def visitCardinality_clause_one_or_more(
        self, ctx: SimpleSchemaParser.Cardinality_clause_one_or_moreContext
    ):
        self._stack += [IntegerExpression(self.CreateRegion(ctx), 1), None]

    # ----------------------------------------------------------------------
    def visitCardinality_clause_fixed(
        self, ctx: SimpleSchemaParser.Cardinality_clause_fixedContext
    ):
        children = self._GetChildren(ctx)
        assert len(children) == 1, children
        assert isinstance(children[0], IntegerExpression), children

        # There have to be 2 distinct IntegerExpression objects so that the parent can be set for
        # each.
        self._stack += [
            children[0],
            IntegerExpression(children[0].region, children[0].value),
        ]

    # ----------------------------------------------------------------------
    # |
    # |  Expressions
    # |
    # ----------------------------------------------------------------------
    def visitNumber_expression(self, ctx: SimpleSchemaParser.Number_expressionContext):
        self._stack.append(
            NumberExpression(self.CreateRegion(ctx), float(ctx.NUMBER().symbol.text))
        )

    # ----------------------------------------------------------------------
    def visitInteger_expression(self, ctx: SimpleSchemaParser.Integer_expressionContext):
        self._stack.append(
            IntegerExpression(self.CreateRegion(ctx), int(ctx.INTEGER().symbol.text))
        )

    # ----------------------------------------------------------------------
    def visitTrue_expression(self, ctx: SimpleSchemaParser.True_expressionContext):
        assert len(ctx.children) == 1, ctx.children
        child = ctx.children[0]

        value = child.symbol.text
        lower_value = value.lower()

        flags: BooleanExpression.Flags = 0

        if lower_value in ["y", "yes"]:
            flags |= BooleanExpression.Flags.YesNo

            if lower_value == "y":
                flags |= BooleanExpression.Flags.SingleChar
        elif lower_value == "true":
            flags |= BooleanExpression.Flags.TrueFalse
        elif lower_value == "on":
            flags |= BooleanExpression.Flags.OnOff
        else:
            assert False, value  # pragma: no cover

        if value.isupper():
            flags |= BooleanExpression.Flags.UpperCase
        elif value.islower():
            flags |= BooleanExpression.Flags.LowerCase
        elif value[0].isupper() and value[1:].islower():
            flags |= BooleanExpression.Flags.PascalCase
        else:
            assert False, value

        self._stack.append(BooleanExpression(self.CreateRegion(ctx), True, flags))

    # ----------------------------------------------------------------------
    def visitFalse_expression(self, ctx: SimpleSchemaParser.False_expressionContext):
        assert len(ctx.children) == 1, ctx.children
        child = ctx.children[0]

        value = child.symbol.text
        lower_value = value.lower()

        flags: BooleanExpression.Flags = 0

        if lower_value in ["n", "no"]:
            flags |= BooleanExpression.Flags.YesNo

            if lower_value == "n":
                flags |= BooleanExpression.Flags.SingleChar
        elif lower_value == "false":
            flags |= BooleanExpression.Flags.TrueFalse
        elif lower_value == "off":
            flags |= BooleanExpression.Flags.OnOff
        else:
            assert False, value

        if value.isupper():
            flags |= BooleanExpression.Flags.UpperCase
        elif value.islower():
            flags |= BooleanExpression.Flags.LowerCase
        elif value[0].isupper() and value[1:].islower():
            flags |= BooleanExpression.Flags.PascalCase
        else:
            assert False, value

        self._stack.append(BooleanExpression(self.CreateRegion(ctx), False, flags))

    # ----------------------------------------------------------------------
    def visitNone_expression(self, ctx: SimpleSchemaParser.None_expressionContext):
        self._stack.append(NoneExpression(self.CreateRegion(ctx)))

    # ----------------------------------------------------------------------
    def visitString_expression(self, ctx: SimpleSchemaParser.String_expressionContext):
        context = ctx

        while not isinstance(context, antlr4.TerminalNode):
            assert len(context.children) == 1
            context = context.children[0]

        token = context.symbol  # type: ignore
        value = token.text

        # At the very least, we should have a beginning and ending quote
        assert len(value) > 2

        if value.startswith('"""') or value.startswith("'''"):
            quote_type = (
                StringExpression.QuoteType.TripleDouble
                if value.startswith('"""')
                else StringExpression.QuoteType.TripleSingle
            )

            initial_whitespace = token.column

            # ----------------------------------------------------------------------
            def TrimPrefix(
                line: str,
                line_offset: int,
            ) -> str:
                index = 0
                whitespace = 0

                while index < len(line) and whitespace < initial_whitespace:
                    if line[index] == " ":
                        whitespace += 1
                    elif line[index] == "\t":
                        whitespace += 4
                    else:
                        raise AntlrException(
                            Errors.antlr_invalid_indentation,
                            self.filename,
                            ctx.start.line + line_offset,
                            whitespace + 1,
                            None,
                        )

                    index += 1

                return line[index:]

            # ----------------------------------------------------------------------

            lines = value.split("\n")

            initial_line = lines[0].rstrip()
            if len(initial_line) != 3:
                raise AntlrException(
                    Errors.antlr_invalid_opening_token,
                    self.filename,
                    ctx.start.line,
                    ctx.start.column + 1 + 3,
                    None,
                )

            final_line = lines[-1]
            if len(TrimPrefix(final_line, len(lines))) != 3:
                raise AntlrException(
                    Errors.antlr_invalid_closing_token,
                    self.filename,
                    ctx.start.line + len(lines) - 1,
                    ctx.start.column + 1,
                    None,
                )

            lines = [TrimPrefix(line, index + 1) for index, line in enumerate(lines[1:-1])]

            value = "\n".join(lines)

        elif value[0] == '"' and value[-1] == '"':
            value = value[1:-1].replace('\\"', '"')
            quote_type = StringExpression.QuoteType.Double
        elif value[0] == "'" and value[-1] == "'":
            value = value[1:-1].replace("\\'", "'")
            quote_type = StringExpression.QuoteType.Single
        else:
            assert False, value  # pragma: no cover

        self._stack.append(StringExpression(self.CreateRegion(ctx), value, quote_type))

    # ----------------------------------------------------------------------
    def visitList_expression(self, ctx: SimpleSchemaParser.List_expressionContext):
        children = self._GetChildren(ctx)
        assert all(isinstance(child, Expression) for child in children), children

        self._stack.append(ListExpression(self.CreateRegion(ctx), cast(list[Expression], children)))

    # ----------------------------------------------------------------------
    def visitTuple_expression(self, ctx: SimpleSchemaParser.Tuple_expressionContext):
        children = self._GetChildren(ctx)
        assert all(isinstance(child, Expression) for child in children), children

        self._stack.append(
            TupleExpression(self.CreateRegion(ctx), cast(tuple[Expression], tuple(children)))
        )

    # ----------------------------------------------------------------------
    # |
    # |  Statements
    # |
    # ----------------------------------------------------------------------
    # TODO: def visitInclude_statement(self, ctx: SimpleSchemaParser.Include_statementContext):
    # TODO:     return self.visitChildren(ctx)  # TODO
    # TODO:
    # TODO: # ----------------------------------------------------------------------
    # TODO: def visitInclude_statement_from(self, ctx: SimpleSchemaParser.Include_statement_fromContext):
    # TODO:     return self.visitChildren(ctx)  # TODO
    # TODO:
    # TODO: # ----------------------------------------------------------------------
    # TODO: def visitInclude_statement_import_star(
    # TODO:     self, ctx: SimpleSchemaParser.Include_statement_import_starContext
    # TODO: ):
    # TODO:     return self.visitChildren(ctx)  # TODO
    # TODO:
    # TODO: # ----------------------------------------------------------------------
    # TODO: def visitInclude_statement_import_element(
    # TODO:     self, ctx: SimpleSchemaParser.Include_statement_import_elementContext
    # TODO: ):
    # TODO:     return self.visitChildren(ctx)  # TODO

    # TODO: # ----------------------------------------------------------------------
    # TODO: def visitExtension_statement(self, ctx: SimpleSchemaParser.Extension_statementContext):
    # TODO:     children = self._GetChildren(ctx)
    # TODO:
    # TODO:     num_children = len(children)
    # TODO:     assert 1 <= num_children <= 3, children
    # TODO:
    # TODO:     assert isinstance(children[0], ParseIdentifier), children
    # TODO:     name = children[0].ToTerminalElement()
    # TODO:
    # TODO:     positional_args: Optional[list[Expression]] = None
    # TODO:     keyword_args: Optional[list[ExtensionStatementKeywordArg]] = None
    # TODO:
    # TODO:     for child in children:
    # TODO:         assert isinstance(child, list) and child, child
    # TODO:
    # TODO:         if isinstance(child[0], ExtensionStatementKeywordArg):
    # TODO:             assert keyword_args is None, (keyword_args, child)
    # TODO:             keyword_args = child
    # TODO:         else:
    # TODO:             assert positional_args is None, positional_args
    # TODO:             positional_args = child
    # TODO:
    # TODO:     self._stack.append(
    # TODO:         ExtensionStatement(
    # TODO:             self.CreateRegion(ctx),
    # TODO:             name,
    # TODO:             cast(list[Expression], positional_args or []),
    # TODO:             keyword_args or [],
    # TODO:         ),
    # TODO:     )
    # TODO:
    # TODO: # ----------------------------------------------------------------------
    # TODO: def visitExtension_statement_positional_args(
    # TODO:     self, ctx: SimpleSchemaParser.Extension_statement_positional_argsContext
    # TODO: ):
    # TODO:     children = self._GetChildren(ctx)
    # TODO:     assert all(isinstance(child, Expression) for child in children), children
    # TODO:
    # TODO:     self._stack.append(children)
    # TODO:
    # TODO: # ----------------------------------------------------------------------
    # TODO: def visitExtension_statement_keyword_args(
    # TODO:     self, ctx: SimpleSchemaParser.Extension_statement_keyword_argsContext
    # TODO: ):
    # TODO:     children = self._GetChildren(ctx)
    # TODO:     assert all(isinstance(child, ExtensionStatementKeywordArg) for child in children), children
    # TODO:
    # TODO:     self._stack.append(children)
    # TODO:
    # TODO: # ----------------------------------------------------------------------
    # TODO: def visitExtension_statement_keyword_arg(
    # TODO:     self, ctx: SimpleSchemaParser.Extension_statement_keyword_argContext
    # TODO: ):
    # TODO:     children = self._GetChildren(ctx)
    # TODO:
    # TODO:     assert len(children) == 2, children
    # TODO:     assert isinstance(children[0], ParseIdentifier), children
    # TODO:     assert isinstance(children[1], Expression), children
    # TODO:
    # TODO:     self._stack.append(
    # TODO:         ExtensionStatementKeywordArg(
    # TODO:             self.CreateRegion(ctx),
    # TODO:             children[0].ToTerminalElement(),
    # TODO:             children[1],
    # TODO:         ),
    # TODO:     )

    # ----------------------------------------------------------------------
    def visitParse_item_statement(self, ctx: SimpleSchemaParser.Parse_item_statementContext):
        children = self._GetChildren(ctx)
        assert len(children) == 2

        assert isinstance(children[0], ParseIdentifier), children
        assert isinstance(children[1], ParseType), children

        self._stack.append(ParseItemStatement(self.CreateRegion(ctx), children[0], children[1]))

    # ----------------------------------------------------------------------
    def visitParse_structure_statement(
        self, ctx: SimpleSchemaParser.Parse_structure_statementContext
    ):
        children = self._GetChildren(ctx)

        num_children = len(children)
        assert num_children >= 1, children

        assert isinstance(children[0], ParseIdentifier), children
        name = children[0]

        bases: list[ParseIdentifierType] = []
        cardinality: Optional[Cardinality] = None
        metadata: Optional[Metadata] = None
        statements: list[Statement] = []

        for child in children[1:]:
            if isinstance(child, ParseType):
                if isinstance(child, ParseIdentifierType):
                    bases.append(child)
                else:
                    raise Errors.ParseStructureStatementInvalidBase.CreateAsException(child.region)

            elif isinstance(child, Cardinality):
                assert cardinality is None, cardinality
                cardinality = child

            elif isinstance(child, Metadata):
                assert metadata is None, metadata
                metadata = child

            elif isinstance(child, Statement):
                statements.append(child)

            else:
                assert False, child  # pragma: no cover

        region = self.CreateRegion(ctx)

        if cardinality is None:
            cardinality = Cardinality(region, None, None)

        self._stack.append(
            ParseStructureStatement(
                region,
                name,
                bases or None,
                cardinality,
                metadata,
                statements,
            ),
        )

    # ----------------------------------------------------------------------
    def visitParse_structure_simplified_statement(
        self, ctx: SimpleSchemaParser.Parse_structure_simplified_statementContext
    ):
        children = self._GetChildren(ctx)

        assert len(children) == 2, children
        assert isinstance(children[0], ParseIdentifier), children
        assert isinstance(children[1], Metadata), children

        region = self.CreateRegion(ctx)

        self._stack.append(
            ParseStructureStatement(
                region,
                children[0],
                None,
                Cardinality(region, None, None),
                children[1],
                [],
            ),
        )

    # ----------------------------------------------------------------------
    # |
    # |  Types
    # |
    # ----------------------------------------------------------------------
    def visitParse_type(self, ctx: SimpleSchemaParser.Parse_typeContext):
        children = self._GetChildren(ctx)

        num_children = len(children)
        assert 1 <= num_children <= 3, children

        assert callable(children[0]), children
        create_func = cast(
            Callable[
                [
                    Region,
                    Cardinality,
                    Optional[Metadata],
                ],
                ParseType,
            ],
            children[0],
        )

        cardinality: Optional[Cardinality] = None
        metadata: Optional[Metadata] = None

        for child in children[1:]:
            if isinstance(child, Cardinality):
                assert cardinality is None, cardinality
                cardinality = child

            elif isinstance(child, Metadata):
                assert metadata is None, metadata
                metadata = child

            else:
                assert False, child

        region = self.CreateRegion(ctx)

        if cardinality is None:
            cardinality = Cardinality(region, None, None)

        self._stack.append(create_func(region, cardinality, metadata))

    # ----------------------------------------------------------------------
    def visitParse_identifier_type(self, ctx: SimpleSchemaParser.Parse_identifier_typeContext):
        children = self._GetChildren(ctx)
        assert len(children) >= 1, children

        identifiers: list[ParseIdentifier] = []
        is_global: Optional[Region] = None

        for child_index, child in enumerate(children):
            if isinstance(child, ParseIdentifier):
                identifiers.append(child)

            elif isinstance(child, Region):
                assert child_index == 0, child_index
                assert is_global is None, (is_global, child)
                is_global = child

            else:
                assert False, child  # pragma: no cover

        assert identifiers, children

        self._stack.append(
            lambda region, cardinality, metadata: ParseIdentifierType(
                region,
                cardinality,
                metadata,
                identifiers,
                is_global,
            ),
        )

    # ----------------------------------------------------------------------
    def visitParse_identifier_type_global(
        self, ctx: SimpleSchemaParser.Parse_identifier_type_globalContext
    ):
        # It is enough to add a region value, as that will signal that the modifier exists when
        # creating the type.
        self._stack.append(self.CreateRegion(ctx))

    # TODO: # ----------------------------------------------------------------------
    # TODO: def visitParse_variant_type(self, ctx: SimpleSchemaParser.Parse_variant_typeContext):
    # TODO:     children = self._GetChildren(ctx)
    # TODO:
    # TODO:     assert children
    # TODO:     assert all(isinstance(child, ParseType) for child in children), children
    # TODO:
    # TODO:     self._stack.append(
    # TODO:         lambda region, cardinality, metadata: ParseVariantType(
    # TODO:             region,
    # TODO:             cardinality,
    # TODO:             metadata,
    # TODO:             cast(list[ParseType], children),
    # TODO:         ),
    # TODO:     )

    # TODO: # ----------------------------------------------------------------------
    # TODO: def visitParse_tuple_type(self, ctx: SimpleSchemaParser.Parse_tuple_typeContext):
    # TODO:     children = self._GetChildren(ctx)
    # TODO:
    # TODO:     assert children
    # TODO:     assert all(isinstance(child, ParseType) for child in children), children
    # TODO:
    # TODO:     self._stack.append(
    # TODO:         lambda region, cardinality, metadata: ParseTupleType(
    # TODO:             region,
    # TODO:             cardinality,
    # TODO:             metadata,
    # TODO:             cast(list[ParseType], children),
    # TODO:         ),
    # TODO:     )
