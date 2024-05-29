# ----------------------------------------------------------------------
# |
# |  Namespace.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-05-27 15:09:09
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Namespace object"""

import bisect

from enum import auto, Enum
from typing import Optional, Type as PythonType, Union
from weakref import ref, ReferenceType as WeakReferenceType

from .TypeFactories import ReferenceTypeFactory, StructureTypeFactory

from ...ANTLR.Grammar.Elements.Statements.ParseIncludeStatement import ParseIncludeStatement  # type: ignore[import-untyped]
from ...ANTLR.Grammar.Elements.Statements.ParseItemStatement import ParseItemStatement  # type: ignore[import-untyped]
from ...ANTLR.Grammar.Elements.Statements.ParseStructureStatement import ParseStructureStatement  # type: ignore[import-untyped]
from ...ANTLR.Grammar.Elements.Types.ParseType import ParseType  # type: ignore[import-untyped]

from ....Elements.Common.TerminalElement import TerminalElement  # type: ignore[import-untyped]
from ....Elements.Common.Visibility import Visibility  # type: ignore[import-untyped]
from ....Elements.Statements.RootStatement import RootStatement  # type: ignore[import-untyped]

from .....Common.Region import Region

from ..... import Errors


# ----------------------------------------------------------------------
# |
# |  Public Types
# |
# ----------------------------------------------------------------------
class Namespace:
    """\
    Object associated with a RootStatement, ParseStructureStatement, or generated dynamically
    by a ParseIncludeStatement that manages a collection of types.
    """

    # ----------------------------------------------------------------------
    def __init__(
        self,
        parent: Optional["Namespace"],
        visibility: Visibility,
        name: str,
        statement: RootStatement | ParseIncludeStatement | ParseStructureStatement,
        structure_type_factory: Optional[StructureTypeFactory],
    ) -> None:
        assert isinstance(
            statement, (RootStatement, ParseIncludeStatement, ParseStructureStatement)
        ), statement
        assert structure_type_factory is None or isinstance(
            statement, ParseStructureStatement
        ), statement

        self._parent_ref: Optional[WeakReferenceType[Namespace]] = (
            None if parent is None else ref(parent)
        )

        self.visibility = visibility
        self.name = name
        self.statement = statement

        self._structure_type_factory = structure_type_factory

        self._data = _StateControlledData()
        self._included_items: set[int] = set()

    # ----------------------------------------------------------------------
    @property
    def parent(self) -> Optional["Namespace"]:
        if self._parent_ref is None:
            return None

        parent = self._parent_ref()
        assert parent is not None

        return parent

    @property
    def nested(self) -> dict[str, Union["Namespace", ReferenceTypeFactory]]:
        return self._data.final_nested

    # ----------------------------------------------------------------------
    def ParseTypeToType(
        self,
        visibility: Visibility,
        type_name: TerminalElement[str],
        parse_type: ParseType,
        identify: TerminalElement[str],
        ancestor_identities: list[TerminalElement[str]],
        fundamental_types: dict[str, PythonType[FundamentalType]],
        *,
        region: Optional[Region] = None,
    ) -> ReferenceType:
        pass  # BugBug

    # ----------------------------------------------------------------------
    def GetSiblingInfo(
        self,
        element: Element,
    ) -> tuple[list[Element], int]:
        parent_statement = self.statement

        pass  # BugBug

    # ----------------------------------------------------------------------
    def AddIncludeStatement(
        self,
        statement: ParseIncludeStatement,
    ) -> None:
        for item in statement.items:
            self._ValidateVisibility(item.element_name.visibility)
            self._ValidateVisibility(item.reference_name.visibility)

        self._data.include_statements.append(statement)

    # ----------------------------------------------------------------------
    def AddItemStatement(
        self,
        statement: ParseItemStatement,
    ) -> None:
        assert statement.name.is_expression, statement.name

        self._ValidateVisibility(statement.name.visibility)

        self._data.item_statements.append(statement)

    # ----------------------------------------------------------------------
    def AddNestedItem(
        self,
        name: TerminalElement[str],
        item: Union["Namespace", ReferenceTypeFactory],
    ) -> None:
        self._ValidateVisibility(self.__class__._GetVisibility(item))

        # Insert in sorted order
        bisect.insort(
            self._data.working_nested.setdefault(name.value, []),
            (name.region, item),
            key=lambda v: v[0],
        )

    # ----------------------------------------------------------------------
    # BugBug: ResolveIncludes
    # BugBug: ResolveTypes
    # BugBug: Finalize

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @staticmethod
    def _GetVisibility(
        item: Union["Namespace", ReferenceTypeFactory],
    ) -> TerminalElement[Visibility]:
        if isinstance(item, Namespace):
            if isinstance(item.statement, RootStatement):
                # This line will never be invoked, but it just seems wrong not to include it.
                # Disabling code coverage as a result.
                return TerminalElement[Visibility](
                    item.statement.region, item.visibility
                )  # pragma: no cover
            elif isinstance(item.statement, ParseIncludeStatement):
                return TerminalElement[Visibility](item.statement.region, item.visibility)
            elif isinstance(item.statement, ParseStructureStatement):
                return item.statement.name.visibility
            else:
                assert False, item.statement  # pragma: no cover

        # We can't use isinstance here, as that would create a circular dependency
        return item.statement.name.visibility  # type: ignore

    # ----------------------------------------------------------------------
    def _ValidateVisibility(
        self,
        visibility: TerminalElement[Visibility],
    ) -> None:
        if isinstance(self.statement, RootStatement) and visibility.value == Visibility.Protected:
            raise Errors.NamespaceVisibilityError.CreateAsException(visibility.region)

    # ----------------------------------------------------------------------
    def _ValidateTypeName(
        self,
        name: str,
        region: Region,
        *,
        is_initial_validation: bool,
    ) -> None:
        assert self._data.state == _State.ResolvingTypeNames, self._data.state

        error_region: Optional[Region] = None

        values = self._data.working_nested.get(name, None)

        if is_initial_validation:
            assert values is not None

            if len(values) > 1:
                error_region = values[1][0]

        elif values is not None:
            error_region = region

        if error_region is not None:
            assert values
            original_region = values[0][0]

            raise Errors.NamespaceDuplicateTypeName.CreateAsException(
                error_region,
                name=name,
                original_region=original_region,
            )

        parent = self.parent
        if parent is not None:
            parent._ValidateTypeName(  # pylint: disable=protected-access
                name, region, is_initial_validation=False
            )


# ----------------------------------------------------------------------
# |
# |  Private Types
# |
# ----------------------------------------------------------------------
class _State(Enum):
    """Resolving types is a multi-step process; these values represent each step within that process"""

    Initialized = auto()

    ResolvingIncludes = auto()
    ResolvedIncludes = auto()

    ResolvingTypeNames = auto()
    ResolvedTypeNames = auto()

    ResolvingTypes = auto()
    ResolvedTypes = auto()

    Finalizing = auto()
    Finalized = auto()


# ----------------------------------------------------------------------
class _StateControlledData:
    """A collection of data whose lifetime is logically controlled by the state"""

    # ----------------------------------------------------------------------
    def __init__(self):
        self._include_statements: list[ParseIncludeStatement] = []
        self._item_statements: list[ParseItemStatement] = []

        self._working_nested: dict[str, list[tuple[Region, Namespace | ReferenceTypeFactory]]] = {}
        self._final_nested: dict[str, Namespace | ReferenceTypeFactory] = {}

        self._state = _State.Initialized

    # ----------------------------------------------------------------------
    @property
    def state(self) -> _State:
        return self._state

    @state.setter
    def state(
        self,
        new_state: _State,
    ) -> None:
        assert new_state.value == self._state.value + 1, (new_state, self._state)
        self._state = new_state

        if self._state == _State.ResolvedIncludes:
            del self._include_statements
        elif self._state == _State.ResolvedTypeNames:
            del self._working_nested
        elif self._state == _State.ResolvedTypes:
            del self._item_statements

    @property
    def include_statements(self) -> list[ParseIncludeStatement]:
        assert self._state.value <= _State.ResolvingIncludes.value
        return self._include_statements

    @property
    def item_statements(self) -> list[ParseItemStatement]:
        assert self._state.value <= _State.ResolvingTypes.value
        return self._item_statements

    @property
    def working_nested(self) -> dict[str, list[tuple[Region, Namespace | ReferenceTypeFactory]]]:
        assert self._state.value <= _State.ResolvingTypeNames.value
        return self._working_nested

    @property
    def final_nested(self) -> dict[str, Namespace | ReferenceTypeFactory]:
        assert self._state.value >= _State.ResolvingTypeNames.value
        return self._final_nested
