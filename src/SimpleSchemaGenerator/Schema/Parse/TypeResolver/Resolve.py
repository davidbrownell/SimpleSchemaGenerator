# ----------------------------------------------------------------------
# |
# |  Resolve.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-22 08:45:26
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains functionality to resolve types."""

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import cast, TypeVar

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common.Streams.DoneManager import DoneManager
from dbrownell_Common.Types import override

from .Common import PSEUDO_TYPE_NAME_PREFIX
from .Impl.Namespace import Namespace
from .Impl.TypeFactories import FundamentalTypeFactory, StructureTypeFactory
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Common.ParseIdentifier import ParseIdentifier
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Statements.ParseIncludeStatement import (
    ParseIncludeStatement,
)
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Statements.ParseItemStatement import (
    ParseItemStatement,
)
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Statements.ParseStructureStatement import (
    ParseStructureStatement,
)
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Types.ParseIdentifierType import (
    ParseIdentifierType,
)
from SimpleSchemaGenerator.Schema.Elements.Common.Cardinality import Cardinality
from SimpleSchemaGenerator.Schema.Elements.Common.Visibility import Visibility
from SimpleSchemaGenerator.Schema.Elements.Statements.RootStatement import RootStatement
from SimpleSchemaGenerator.Schema.Elements.Types.FundamentalTypes import fundamental_types
from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.TypeDefinition import TypeDefinition
from SimpleSchemaGenerator.Common.ExecuteInParallel import ExecuteInParallel as ExecuteInParallelImpl
from SimpleSchemaGenerator.Schema.Visitors.ElementVisitor import VisitResult, ElementVisitorHelper
from SimpleSchemaGenerator import Errors


# ----------------------------------------------------------------------
def Resolve(
    dm: DoneManager,
    roots: dict[Path, RootStatement],
    *,
    single_threaded: bool = False,
    quiet: bool = False,
    raise_if_single_exception: bool = True,
) -> dict[Path, Exception] | None:
    max_num_threads = 1 if single_threaded else None

    # Create namespaces
    with dm.VerboseNested("Creating namespaces...") as verbose_dm:
        # ----------------------------------------------------------------------
        def CreateNamespace(
            root: RootStatement,
        ) -> Namespace:
            root_namespace = Namespace(
                None,
                Visibility.Public,
                "root",
                root,
                None,
            )

            root.Accept(_CreateNamespacesVisitor(root, root_namespace))

            return root_namespace

        # ----------------------------------------------------------------------

        namespaces = _ExecuteInParallel(
            verbose_dm,
            roots,
            CreateNamespace,
            quiet=quiet,
            max_num_threads=max_num_threads,
            raise_if_single_exception=raise_if_single_exception,
        )

        if verbose_dm.result != 0:
            assert all(isinstance(value, Exception) for value in namespaces.values()), namespaces
            return cast(dict[Path, Exception], namespaces)

        namespaces = cast(dict[Path, Namespace], namespaces)

    # Resolve includes
    with dm.VerboseNested("Resolving includes...") as verbose_dm:
        results = _ExecuteInParallel(
            verbose_dm,
            namespaces,
            lambda root_namespace: root_namespace.ResolveIncludes(namespaces),
            quiet=quiet,
            max_num_threads=max_num_threads,
            raise_if_single_exception=raise_if_single_exception,
        )

        if verbose_dm.result != 0:
            assert all(isinstance(value, Exception) for value in results.values()), results
            return cast(dict[Path, Exception], results)

    # Ensure unique type names
    with dm.VerboseNested("Validating type names...") as verbose_dm:
        results = _ExecuteInParallel(
            verbose_dm,
            namespaces,
            lambda root_namespace: root_namespace.ResolveTypeNames(),
            quiet=quiet,
            max_num_threads=max_num_threads,
            raise_if_single_exception=raise_if_single_exception,
        )

        if verbose_dm.result != 0:
            assert all(isinstance(value, Exception) for value in results.values()), results
            return cast(dict[Path, Exception], results)

    # Resolve types
    with dm.VerboseNested("Resolving types...") as verbose_dm:
        fundamental_types = _LoadFundamentalTypes()

        results = _ExecuteInParallel(
            verbose_dm,
            namespaces,
            lambda root_namespace: root_namespace.ResolveTypes(fundamental_types),
            quiet=quiet,
            max_num_threads=max_num_threads,
            raise_if_single_exception=raise_if_single_exception,
        )

        if verbose_dm.result != 0:
            assert all(isinstance(value, Exception) for value in results.values()), results
            return cast(dict[Path, Exception], results)

    # Finalize types
    with dm.VerboseNested("Finalizing types...") as verbose_dm:
        results = _ExecuteInParallel(
            verbose_dm,
            namespaces,
            lambda root_namespace: root_namespace.Finalize(),
            quiet=quiet,
            max_num_threads=max_num_threads,
            raise_if_single_exception=raise_if_single_exception,
        )

        if verbose_dm.result != 0:
            assert all(isinstance(value, Exception) for value in results.values()), results
            return cast(dict[Path, Exception], results)

    # In this context, returning None indicates success
    return None


# ----------------------------------------------------------------------
# |
# |  Private Types
# |
# ----------------------------------------------------------------------
class _CreateNamespacesVisitor(ElementVisitorHelper):
    # ----------------------------------------------------------------------
    def __init__(
        self,
        root: RootStatement,
        root_namespace: Namespace,
    ) -> None:
        super().__init__()

        self._root = root
        self._namespace_stack: list[Namespace] = [root_namespace]

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnParseIncludeStatement(
        self,
        element: ParseIncludeStatement,
    ) -> Iterator[VisitResult]:
        self._namespace_stack[-1].AddIncludeStatement(element)

        yield VisitResult.Continue

        element.Disable()

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnParseItemStatement(
        self,
        element: ParseItemStatement,
    ) -> Iterator[VisitResult]:
        yield VisitResult.Continue

        if element.name.is_type:
            self._namespace_stack[-1].AddNestedItem(
                element.name.ToTerminalElement(),
                FundamentalTypeFactory(element, self._namespace_stack[-1]),
            )
        elif element.name.is_expression:
            self._namespace_stack[-1].AddItemStatement(element)
        else:
            raise AssertionError(element.name)

    # ----------------------------------------------------------------------
    @override
    @contextmanager
    def OnParseStructureStatement(
        self,
        element: ParseStructureStatement,
    ) -> Iterator[VisitResult]:
        if element.name.is_expression:
            if not element.children:
                raise Errors.SimpleSchemaGeneratorException(
                    Errors.ResolveStructureStatementEmptyPseudoElement.Create(element.region),
                )

            # Create a pseudo element for this statement. This ensures that there is always a
            # structure definition and then and item that references it for all structures
            # (regardless of how they were defined).
            unique_type_name = (
                f"{PSEUDO_TYPE_NAME_PREFIX}-Ln{element.region.begin.line}Col{element.region.begin.column}"
            )

            new_structure = ParseStructureStatement(
                element.region,
                ParseIdentifier(element.region, unique_type_name),
                element.bases,
                element.cardinality,
                element.unresolved_metadata,
                element.children,
            )

            new_item = ParseItemStatement(
                element.region,
                element.name,
                ParseIdentifierType(
                    element.region,
                    Cardinality(element.region, None, None),
                    None,
                    [
                        ParseIdentifier(element.region, unique_type_name),
                    ],
                    None,
                ),
            )

            # Add the new elements and disable the current one
            parents_children, sibling_index = self._namespace_stack[-1].GetSiblingInfo(element)

            # These inserted items will be parsed next
            parents_children.insert(sibling_index + 1, new_structure)
            parents_children.insert(sibling_index + 2, new_item)

            element.Disable()

            yield VisitResult.SkipAll
            return

        assert element.name.is_type, element.name

        namespace = Namespace(
            self._namespace_stack[-1],
            element.name.visibility.value,
            element.name.value,
            element,
            StructureTypeFactory(element, self._namespace_stack[-1]),
        )

        self._namespace_stack[-1].AddNestedItem(
            element.name.ToTerminalElement(),
            namespace,
        )

        self._namespace_stack.append(namespace)
        with ExitStack(self._namespace_stack.pop):
            yield VisitResult.Continue


# ----------------------------------------------------------------------
# |
# |  Private Functions
# |
# ----------------------------------------------------------------------
_ExecuteInParallelInputT = TypeVar("_ExecuteInParallelInputT")
_ExecuteInParallelOutputT = TypeVar("_ExecuteInParallelOutputT")


def _ExecuteInParallel(
    dm: DoneManager,
    items: dict[Path, _ExecuteInParallelInputT],
    func: Callable[[_ExecuteInParallelInputT], _ExecuteInParallelOutputT],
    *,
    quiet: bool,
    max_num_threads: int | None,
    raise_if_single_exception: bool,
) -> dict[Path, Exception] | dict[Path, _ExecuteInParallelOutputT]:
    return ExecuteInParallelImpl(
        dm,
        "Processing",
        items,
        lambda context, _: func(context),
        quiet=quiet,
        max_num_threads=max_num_threads,
        raise_if_single_exception=raise_if_single_exception,
    )


# ----------------------------------------------------------------------
def _LoadFundamentalTypes() -> dict[str, type[TypeDefinition]]:
    results: dict[str, type[TypeDefinition]] = {}

    for typedef in fundamental_types:
        assert typedef.NAME not in results, typedef.NAME
        results[typedef.NAME] = typedef

    return results
