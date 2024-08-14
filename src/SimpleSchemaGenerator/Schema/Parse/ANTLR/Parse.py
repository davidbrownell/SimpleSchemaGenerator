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

from antlr4.error.ErrorListener import ConsoleErrorListener
from dbrownell_Common.ContextlibEx import ExitStack  # type: ignore[import-untyped]
from dbrownell_Common import ExecuteTasks  # type: ignore[import-untyped]
from dbrownell_Common import PathEx  # type: ignore[import-untyped]
from dbrownell_Common.Streams.DoneManager import DoneManager  # type: ignore[import-untyped]

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

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent / "GeneratedCode")))
with ExitStack(lambda: sys.path.pop(0)):
    from .GeneratedCode.SimpleSchemaLexer import SimpleSchemaLexer
    from .GeneratedCode.SimpleSchemaParser import SimpleSchemaParser
    from .GeneratedCode.SimpleSchemaVisitor import SimpleSchemaVisitor


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

        super(AntlrException, self).__init__(f"{message} ({source} <{location}>)")

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
    tab_width: int = 4,
) -> dict[
    Path,  # workspace root
    dict[
        PurePath,  # relative path
        Exception | RootStatement,
    ],
]:
    if file_extensions is None:
        file_extensions = DEFAULT_FILE_EXTENSIONS

    # Ensure that the workspaces paths are fully resolved
    for workspace_name, workspace_value in list(workspaces.items()):
        resolved_workspace_name = workspace_name.resolve()

        if resolved_workspace_name != workspace_name:
            workspaces[resolved_workspace_name] = workspace_value
            del workspaces[workspace_name]

    workspace_names: list[Path] = [workspace for workspace in workspaces.keys()]

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
        # This variable is used in PrepareTask, but cannot be created until PrepareTask
        # has been defined.
        create_include_statement_func: Optional[_CreateIncludeStatementFuncType] = None

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

                        parser.removeErrorListener(ConsoleErrorListener.INSTANCE)
                        parser.addErrorListener(_ErrorListener(fullpath))

                        ast = parser.entry_point__()
                        assert ast

                        assert create_include_statement_func is not None

                        visitor = _SimpleSchemaVisitor(
                            content,
                            fullpath,
                            lambda line: cast(None, status.OnProgress(line, None)),
                            create_include_statement_func,
                            is_included_file=is_included_file,
                            tab_width=tab_width,
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

        create_include_statement_func = _CreateIncludeStatementFuncFactory(
            file_extensions,
            workspace_names,
            results,
            results_lock,
            enqueue_func,
            PrepareTask,
        )

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
        if e is not None:
            raise AntlrException(msg, self._source, line, column + 1, e)


# ----------------------------------------------------------------------
class _CreateIncludeStatementFuncType(Protocol):
    def __call__(
        self,
        include_path: Path,
        region: Region,
        root_indicator: Optional[Region],
        directory_indicator: Optional[Region],
        filename_or_directory: TerminalElement[Path],
        items: list[ParseIncludeStatementItem],
        *,
        is_star_include: bool,
    ) -> ParseIncludeStatement: ...


# ----------------------------------------------------------------------
class _VisitorMixin:
    """Contains functionality that doesn't change when the grammar is regenerated"""

    # ----------------------------------------------------------------------
    # |
    # |  Public Methods
    # |
    # ----------------------------------------------------------------------
    def __init__(
        self,
        content: str,
        filename: Path,
        on_progress_func: Callable[[int], None],
        create_include_statement_func: _CreateIncludeStatementFuncType,
        *,
        is_included_file: bool,
        tab_width: int,
    ):
        self.content = content
        self.filename = filename
        self.is_included_file = is_included_file
        self.tab_width = tab_width

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
            assert False, value  # pragma: no cover

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
            assert False, value  # pragma: no cover

        if value.isupper():
            flags |= BooleanExpression.Flags.UpperCase
        elif value.islower():
            flags |= BooleanExpression.Flags.LowerCase
        elif value[0].isupper() and value[1:].islower():
            flags |= BooleanExpression.Flags.PascalCase
        else:
            assert False, value  # pragma: no cover

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

            # Get the length of the initial whitespace by looking at the characters that come
            # before the opening token.
            initial_whitespace = 0
            char_index = token.start - 1

            while char_index > 0:
                char = self.content[char_index]

                if char == "\n":
                    break

                if char == "\t":
                    initial_whitespace += self.tab_width
                else:
                    initial_whitespace += 1

                char_index -= 1

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
                        whitespace += self.tab_width
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
    def visitInclude_statement(self, ctx: SimpleSchemaParser.Include_statementContext):
        children = self._GetChildren(ctx)
        assert len(children) >= 1, children

        region = self.CreateRegion(ctx)

        # Does the filename have a root indicator?
        if isinstance(children[0], Region):
            root_indicator = children.pop(0)
        else:
            root_indicator = None

        # Get the filename parts
        filename_parts: list[ParseIdentifier | TerminalElement[str]] = []

        while children and isinstance(children[0], (ParseIdentifier, TerminalElement)):
            filename_parts.append(children.pop(0))

        filename = TerminalElement[Path](
            Region(
                filename_parts[0].region.filename,
                filename_parts[0].region.begin,
                filename_parts[-1].region.end,
            ),
            Path(*(part.value for part in filename_parts)),
        )

        if children and isinstance(children[0], Region):
            directory_indicator = children.pop(0)
        else:
            directory_indicator = None

        if len(children) == 1 and isinstance(children[0], str) and children[0] == "*":
            children = []
            is_star_include = True
        else:
            assert all(isinstance(child, ParseIncludeStatementItem) for child in children), children
            children = cast(list[ParseIncludeStatementItem], children)

            is_star_include = False

        self._stack.append(
            self._create_include_statement_func(
                self.filename,
                region,
                root_indicator,
                directory_indicator,
                filename,
                children,
                is_star_include=is_star_include,
            ),
        )

    # ----------------------------------------------------------------------
    def visitInclude_statement_from(self, ctx: SimpleSchemaParser.Include_statement_fromContext):
        entire_region = self.CreateRegion(ctx)

        # Look for the root identifier
        if (
            len(ctx.children) > 1
            and isinstance(ctx.children[0], antlr4.TerminalNode)
            and ctx.children[0].symbol.text == "/"
        ):
            self._stack.append(
                Region(
                    entire_region.filename,
                    entire_region.begin,
                    Location(
                        entire_region.end.line,
                        entire_region.begin.column + 1,
                    ),
                ),
            )

        # Process the elements
        result = self.visitChildren(ctx)

        # Look for the directory identifier
        if (
            len(ctx.children) > 1
            and isinstance(ctx.children[-1], antlr4.TerminalNode)
            and ctx.children[-1].symbol.text == "/"
        ):
            self._stack.append(
                Region(
                    entire_region.filename,
                    Location(
                        entire_region.begin.line,
                        entire_region.end.column - 1,
                    ),
                    entire_region.end,
                ),
            )

        return result

    # ----------------------------------------------------------------------
    def visitInclude_statement_from_parent_dir(
        self, ctx: SimpleSchemaParser.Include_statement_from_parent_dirContext
    ):
        self._stack.append(TerminalElement[str](self.CreateRegion(ctx), ".."))

    # ----------------------------------------------------------------------
    def visitInclude_statement_import_star(
        self, ctx: SimpleSchemaParser.Include_statement_import_starContext
    ):
        self._stack.append("*")

    # ----------------------------------------------------------------------
    def visitInclude_statement_import_element(
        self, ctx: SimpleSchemaParser.Include_statement_import_elementContext
    ):
        children = self._GetChildren(ctx)

        num_children = len(children)
        assert 1 <= num_children <= 2, children

        assert isinstance(children[0], ParseIdentifier), children
        element_name = cast(ParseIdentifier, children[0])

        if num_children > 1:
            assert isinstance(children[0], ParseIdentifier), children
            reference_name = children[1]
        else:
            reference_name = ParseIdentifier(element_name.region, element_name.value)

        self._stack.append(
            ParseIncludeStatementItem(
                self.CreateRegion(ctx),
                element_name,
                reference_name,
            )
        )

    # ----------------------------------------------------------------------
    def visitExtension_statement(self, ctx: SimpleSchemaParser.Extension_statementContext):
        children = self._GetChildren(ctx)

        num_children = len(children)
        assert 1 <= num_children <= 3, children

        assert isinstance(children[0], ParseIdentifier), children
        name = children[0].ToTerminalElement()

        positional_args: Optional[list[Expression]] = None
        keyword_args: Optional[list[ExtensionStatementKeywordArg]] = None

        for child in children[1:]:
            assert isinstance(child, list) and child, child

            if isinstance(child[0], ExtensionStatementKeywordArg):
                assert keyword_args is None, (keyword_args, child)
                keyword_args = child
            else:
                assert positional_args is None, positional_args
                positional_args = child

        self._stack.append(
            ExtensionStatement(
                self.CreateRegion(ctx),
                name,
                cast(list[Expression], positional_args or []),
                keyword_args or [],
            ),
        )

    # ----------------------------------------------------------------------
    def visitExtension_statement_positional_args(
        self, ctx: SimpleSchemaParser.Extension_statement_positional_argsContext
    ):
        children = self._GetChildren(ctx)
        assert all(isinstance(child, Expression) for child in children), children

        self._stack.append(children)

    # ----------------------------------------------------------------------
    def visitExtension_statement_keyword_args(
        self, ctx: SimpleSchemaParser.Extension_statement_keyword_argsContext
    ):
        children = self._GetChildren(ctx)
        assert all(isinstance(child, ExtensionStatementKeywordArg) for child in children), children

        self._stack.append(children)

    # ----------------------------------------------------------------------
    def visitExtension_statement_keyword_arg(
        self, ctx: SimpleSchemaParser.Extension_statement_keyword_argContext
    ):
        children = self._GetChildren(ctx)

        assert len(children) == 2, children
        assert isinstance(children[0], ParseIdentifier), children
        assert isinstance(children[1], Expression), children

        self._stack.append(
            ExtensionStatementKeywordArg(
                self.CreateRegion(ctx),
                children[0].ToTerminalElement(),
                children[1],
            ),
        )

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
                    raise Errors.SimpleSchemaGeneratorException(
                        Errors.ParseStructureStatementInvalidBase.Create(child.region)
                    )

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
                assert False, child  # pragma: no cover

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

    # ----------------------------------------------------------------------
    def visitParse_variant_type(self, ctx: SimpleSchemaParser.Parse_variant_typeContext):
        children = self._GetChildren(ctx)

        assert children
        assert all(isinstance(child, ParseType) for child in children), children

        self._stack.append(
            lambda region, cardinality, metadata: ParseVariantType(
                region,
                cardinality,
                metadata,
                cast(list[ParseType], children),
            ),
        )

    # ----------------------------------------------------------------------
    def visitParse_tuple_type(self, ctx: SimpleSchemaParser.Parse_tuple_typeContext):
        children = self._GetChildren(ctx)

        assert children
        assert all(isinstance(child, ParseType) for child in children), children

        self._stack.append(
            lambda region, cardinality, metadata: ParseTupleType(
                region,
                cardinality,
                metadata,
                cast(list[ParseType], children),
            ),
        )


# ----------------------------------------------------------------------
# |
# |  Private Functions
# |
# ----------------------------------------------------------------------
class _PrepareTaskFuncType(Protocol):
    def __call__(
        self,
        workspace_root: Path,
        relative_path: PurePath,
        content_func: Callable[[], str],
        *,
        is_included_file: bool,
    ) -> tuple[int, ExecuteTasks.YieldQueueExecutorTypes.ExecuteFuncType]: ...


def _CreateIncludeStatementFuncFactory(
    file_extensions: list[str],
    workspace_names: list[Path],
    results: dict[Path, dict[PurePath, None | Exception | RootStatement]],
    results_lock: threading.Lock,
    enqueue_func: ExecuteTasks.YieldQueueExecutorTypes.EnqueueFuncType,
    prepare_task_func: _PrepareTaskFuncType,
) -> _CreateIncludeStatementFuncType:
    # ----------------------------------------------------------------------
    def ResolveIncludeFilename(
        path: Path,
        *,
        allow_directory: bool,
    ) -> Optional[Path]:
        path = path.resolve()

        if path.is_file() or (allow_directory and path.is_dir()):
            return path

        for extension in file_extensions:
            potential_path = path.parent / (path.name + extension)
            if potential_path.is_file():
                return potential_path

        return None

    # ----------------------------------------------------------------------
    def Impl(
        include_path: Path,
        region: Region,
        root_indicator: Optional[Region],
        directory_indicator: Optional[Region],
        filename_or_directory: TerminalElement[Path],
        items: list[ParseIncludeStatementItem],
        *,
        is_star_include: bool,
    ) -> ParseIncludeStatement:
        root: Optional[Path] = None

        search_paths: list[list[Path]] = []

        if root_indicator is None:
            search_paths.append([include_path.parent])

        search_paths.append(workspace_names)

        for potential_root in itertools.chain(*search_paths):
            fullpath = ResolveIncludeFilename(
                potential_root / filename_or_directory.value,
                allow_directory=directory_indicator is not None,
            )

            if fullpath is not None and (directory_indicator is None or fullpath.is_dir()):
                root = fullpath
                break

        if root is None:
            if directory_indicator is not None:
                raise Errors.SimpleSchemaGeneratorException(
                    Errors.ParseCreateIncludeStatementInvalidDirectory.Create(
                        filename_or_directory.region,
                        filename_or_directory.value,
                    ),
                )
            else:
                raise Errors.SimpleSchemaGeneratorException(
                    Errors.ParseCreateIncludeStatementInvalidFilename.Create(
                        filename_or_directory.region,
                        filename_or_directory.value,
                    ),
                )

        filename: Optional[Path] = None
        filename_region: Optional[Region] = None
        include_type: Optional[ParseIncludeStatementType] = None

        if root.is_dir():
            if is_star_include:
                raise Errors.SimpleSchemaGeneratorException(
                    Errors.ParseCreateIncludeStatementDirWithStar.Create(region, root)
                )

            filename = ResolveIncludeFilename(
                root / items[0].element_name.value,
                allow_directory=False,
            )

            filename_region = Region(
                filename_or_directory.region.filename,
                filename_or_directory.region.begin,
                items[0].element_name.region.end,
            )

            if filename is None:
                raise Errors.SimpleSchemaGeneratorException(
                    Errors.ParseCreateIncludeStatementInvalidFilename.Create(
                        filename_region,
                        items[0].element_name.value,
                    ),
                )

            include_type = ParseIncludeStatementType.Module
            items = []

        else:
            if is_star_include:
                assert not items
                include_type = ParseIncludeStatementType.Star
            else:
                include_type = ParseIncludeStatementType.Package

            filename = root
            filename_region = filename_or_directory.region

        assert filename is not None
        assert filename.is_file(), filename
        assert filename_region is not None
        assert include_type is not None

        # Get the workspace associated with the file
        workspace: Optional[Path] = None

        for workspace_name in workspace_names:
            if PathEx.IsDescendant(filename, workspace_name):
                workspace = workspace_name
                break

        if workspace is None:
            raise Errors.SimpleSchemaGeneratorException(
                Errors.ParseCreateIncludeStatementInvalidWorkspace.Create(region, filename)
            )

        # Get the relative path for the workspace
        relative_path = PathEx.CreateRelativePath(workspace, filename)
        assert relative_path is not None

        # Determine if this is a file that should be enqueued for parsing
        should_enqueue = False

        with results_lock:
            workspace_results = results[workspace]

            if relative_path not in workspace_results:
                workspace_results[relative_path] = None
                should_enqueue = True

        if should_enqueue:
            # ----------------------------------------------------------------------
            def GetContent() -> str:
                with filename.open(encoding="utf-8") as f:
                    return f.read()

            # ----------------------------------------------------------------------

            enqueue_func(
                str(filename),
                lambda on_simple_status_func: prepare_task_func(
                    workspace,
                    relative_path,
                    GetContent,
                    is_included_file=True,
                ),
            )

        return ParseIncludeStatement(
            region,
            include_type,
            TerminalElement(filename_region, filename),
            items,
        )

    # ----------------------------------------------------------------------

    return Impl
