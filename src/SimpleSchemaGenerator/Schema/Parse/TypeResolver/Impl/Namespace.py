# ----------------------------------------------------------------------
# |
# |  Namespace.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-22 11:56:08
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
from pathlib import Path
from typing import Optional, Type as PythonType, Union
from weakref import ref, ReferenceType as WeakReferenceType

from dbrownell_Common.ContextlibEx import ExitStack  # type: ignore[import-untyped]

from .TypeFactories import FundamentalTypeFactory, StructureTypeFactory
from ...ANTLR.Grammar.Elements.Statements.ParseIncludeStatement import (
    ParseIncludeStatement,
    ParseIncludeStatementType,
)
from ...ANTLR.Grammar.Elements.Statements.ParseItemStatement import ParseItemStatement
from ...ANTLR.Grammar.Elements.Statements.ParseStructureStatement import ParseStructureStatement
from ...ANTLR.Grammar.Elements.Types.ParseIdentifierType import ParseIdentifierType
from ...ANTLR.Grammar.Elements.Types.ParseTupleType import ParseTupleType
from ...ANTLR.Grammar.Elements.Types.ParseType import ParseType
from ...ANTLR.Grammar.Elements.Types.ParseVariantType import ParseVariantType
from ....Elements.Common.Element import Element
from ....Elements.Common.Metadata import Metadata, MetadataItem
from ....Elements.Common.TerminalElement import TerminalElement
from ....Elements.Common.Visibility import Visibility
from ....Elements.Statements.ItemStatement import ItemStatement
from ....Elements.Statements.RootStatement import RootStatement
from ....Elements.Statements.Statement import Statement
from ....Elements.Types.Type import Type
from ....Elements.Types.TypeDefinitions.StructureTypeDefinition import StructureTypeDefinition
from ....Elements.Types.TypeDefinitions.TupleTypeDefinition import TupleTypeDefinition
from ....Elements.Types.TypeDefinitions.TypeDefinition import TypeDefinition
from ....Elements.Types.TypeDefinitions.VariantTypeDefinition import VariantTypeDefinition
from .....Common.Region import Region
from ..... import Errors


# ----------------------------------------------------------------------
# |
# |  Public Types
# |
# ----------------------------------------------------------------------
class Namespace:
    """\
    Object associated with a RootStatement, ParseStructureStatement, or generated dynamically by
    a ParseIncludeStatement that manages a collection of types.
    """

    # ----------------------------------------------------------------------
    def __init__(
        self,
        parent: Optional["Namespace"],
        visibility: Visibility,
        name: str,
        statement: RootStatement | ParseIncludeStatement | ParseStructureStatement,
        structure_type_factory: StructureTypeFactory | None,
    ) -> None:
        assert isinstance(
            statement, (RootStatement, ParseIncludeStatement, ParseStructureStatement)
        ), statement
        assert structure_type_factory is None or isinstance(
            statement, ParseStructureStatement
        ), statement

        self._parent_ref: WeakReferenceType[Namespace] | None = (
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
    def nested(self) -> dict[str, Union["Namespace", FundamentalTypeFactory]]:
        return self._data.final_nested

    # ----------------------------------------------------------------------
    def ParseTypeToType(
        self,
        visibility: TerminalElement[Visibility],
        type_name: TerminalElement[str],
        parse_type: ParseType,
        identity: TerminalElement[str],
        ancestor_identities: list[TerminalElement[str]],
        fundamental_types: dict[str, PythonType[TypeDefinition]],
        *,
        region: Region | None = None,
    ) -> Type:
        if identity in ancestor_identities:
            raise Errors.SimpleSchemaGeneratorException(
                Errors.NamespaceCycle.Create(
                    ancestor_identities[0].region,
                    name=ancestor_identities[0].value,
                    ancestors_str="\n".join(
                        f"    * '{ancestor.value}' {ancestor.region}"
                        for ancestor in ancestor_identities
                    ),
                    ancestors=ancestor_identities,
                ),
            )

        ancestor_identities.append(identity)
        with ExitStack(ancestor_identities.pop):
            if isinstance(parse_type, ParseIdentifierType):
                return self._ParseIdentifierTypeToType(
                    visibility,
                    type_name,
                    parse_type,
                    ancestor_identities,
                    fundamental_types,
                    region=region,
                )

            type_definition_class: PythonType[TupleTypeDefinition | VariantTypeDefinition]

            if isinstance(parse_type, ParseTupleType):
                type_definition_class = TupleTypeDefinition
            elif isinstance(parse_type, ParseVariantType):
                type_definition_class = VariantTypeDefinition
            else:
                assert False, parse_type  # pragma: no cover

            type_definition = type_definition_class(
                parse_type.region,
                [
                    self.ParseTypeToType(
                        TerminalElement[Visibility](child_type.region, Visibility.Private),
                        TerminalElement[str](
                            child_type.region,
                            f"{type_definition_class.NAME}_Ln{parse_type.region.begin.line}Col{parse_type.region.begin.column}_Type{child_type_index}",
                        ),
                        child_type,
                        TerminalElement[str](child_type.region, child_type.display_type),
                        ancestor_identities,
                        fundamental_types,
                    )
                    for child_type_index, child_type in enumerate(parse_type.types)  # type: ignore
                ],
            )

            return Type.Create(
                visibility,
                type_name,
                type_definition,
                parse_type.cardinality,
                parse_type.unresolved_metadata,
                region=region or parse_type.region,
            )

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
        item: Union["Namespace", FundamentalTypeFactory],
    ) -> None:
        self._ValidateVisibility(self.__class__._GetVisibility(item))

        # Insert in sorted order
        bisect.insort(
            self._data.working_nested.setdefault(name.value, []),
            (name.region, item),
            key=lambda v: v[0],
        )

    # ----------------------------------------------------------------------
    def GetSiblingInfo(
        self,
        element: Element,
    ) -> tuple[list[Element], int]:
        """Returns information on where the provided element can be found relative to its siblings."""
        parent_statement = self.statement

        accept_children_result = (
            parent_statement._GetAcceptChildren()  # pylint: disable=protected-access
        )
        assert accept_children_result is not None

        children = accept_children_result.children

        for child_index, child in enumerate(children):
            if child is element:
                return children, child_index

        assert False, (children, element)  # pragma: no cover

    # ----------------------------------------------------------------------
    def ResolveIncludes(
        self,
        all_namespaces: dict[Path, "Namespace"],
    ) -> None:
        self._data.state = _State.ResolvingIncludes

        # ----------------------------------------------------------------------
        def ApplyIncludedItems(
            parent_namespace: Namespace,
            included_namespace: Namespace,
            include_statement_region: Region,
        ) -> None:
            for key, nested_include_item in included_namespace._data.working_nested.items():
                # Don't worry if there are multiple values (which indicates an error) right now, as
                # that scenario will be handled later. However, we need this information in order to
                # calculate errors.
                nested_include_item = nested_include_item[0][1]

                if (
                    self.__class__._GetVisibility(nested_include_item).value != Visibility.Public
                ):  # pylint: disable=protected-access
                    continue

                parent_namespace.AddNestedItem(
                    TerminalElement[str](include_statement_region, key),
                    nested_include_item,
                )

                parent_namespace._included_items.add(id(nested_include_item))

        # ----------------------------------------------------------------------

        for statement in self._data.include_statements:
            included_namespace = all_namespaces.get(statement.filename.value, None)
            assert included_namespace is not None, statement.filename

            if statement.include_type == ParseIncludeStatementType.Module:
                module_namespace = Namespace(
                    self.parent,
                    Visibility.Private,
                    statement.filename.value.stem,
                    statement,
                    None,
                )

                ApplyIncludedItems(module_namespace, included_namespace, statement.region)

                self.AddNestedItem(
                    TerminalElement[str](statement.region, module_namespace.name),
                    module_namespace,
                )

            elif statement.include_type == ParseIncludeStatementType.Package:
                for include_item in statement.items:
                    nested_include_item = included_namespace._data.working_nested.get(
                        include_item.element_name.value, None
                    )
                    if nested_include_item is None:
                        raise Errors.SimpleSchemaGeneratorException(
                            Errors.NamespaceInvalidIncludeItem.Create(
                                include_item.element_name.region,
                                include_item.element_name.value,
                            ),
                        )

                    # Don't worry if there are multiple values (which indicates an error) right now, as
                    # that scenario will be handled later. However, we need this information in order to
                    # calculate errors.
                    nested_include_item = nested_include_item[0][1]

                    if (
                        self.__class__._GetVisibility(nested_include_item).value
                        != Visibility.Public
                    ):
                        raise Errors.SimpleSchemaGeneratorException(
                            Errors.NamespaceInvalidIncludeItemVisibility.Create(
                                include_item.element_name.region,
                                include_item.element_name.value,
                            ),
                        )

                    self.AddNestedItem(
                        include_item.reference_name.ToTerminalElement(),
                        nested_include_item,
                    )

                    self._included_items.add(id(nested_include_item))

            elif statement.include_type == ParseIncludeStatementType.Star:
                ApplyIncludedItems(self, included_namespace, statement.region)

            else:
                assert False, statement.include_type  # pragma: no cover

        for nested_values in self._data.working_nested.values():
            nested_value = nested_values[0][1]

            if not isinstance(nested_value, Namespace):
                continue

            if id(nested_value) in self._included_items:
                continue

            nested_value.ResolveIncludes(all_namespaces)

        self._data.state = _State.ResolvedIncludes

    # ----------------------------------------------------------------------
    def ResolveTypeNames(self) -> None:
        self._data.state = _State.ResolvingTypeNames

        nested: dict[str, Namespace | FundamentalTypeFactory] = {}

        for key, nested_values in self._data.working_nested.items():
            nested_value_region, nested_value = nested_values[0]

            self._ValidateTypeName(
                key,
                nested_value_region,
                is_initial_validation=True,
            )

            if isinstance(nested_value, Namespace) and id(nested_value) not in self._included_items:
                nested_value.ResolveTypeNames()

            nested[key] = nested_value

        assert not self.nested
        self._data.final_nested.update(nested)

        self._data.state = _State.ResolvedTypeNames

    # ----------------------------------------------------------------------
    def ResolveTypes(
        self,
        fundamental_types: dict[str, PythonType[TypeDefinition]],
    ) -> None:
        self._data.state = _State.ResolvingTypes

        # ----------------------------------------------------------------------
        def ReplaceElement(
            existing_statement: Statement,
            new_element: Element,
        ) -> None:
            siblings, sibling_index = self.GetSiblingInfo(existing_statement)

            siblings.insert(sibling_index + 1, new_element)
            siblings[sibling_index].Disable()

        # ----------------------------------------------------------------------

        for nested_value in self._data.final_nested.values():
            is_import = id(nested_value) in self._included_items

            type_factory: FundamentalTypeFactory | StructureTypeFactory

            if isinstance(nested_value, Namespace):
                if not is_import:
                    nested_value.ResolveTypes(fundamental_types)

                if isinstance(nested_value.statement, ParseIncludeStatement):
                    # If here, we are looking at a namespace that was created for a
                    # module import. No need to generate an element based on this
                    # namespace, as there isn't an element that actually exists.
                    assert (  # pylint: disable=protected-access
                        nested_value._structure_type_factory is None
                    )

                    continue

                assert (  # pylint: disable=protected-access
                    nested_value._structure_type_factory is not None
                )
                type_factory = (
                    nested_value._structure_type_factory  # pylint: disable=protected-access
                )

            else:
                type_factory = nested_value

            new_type = type_factory.GetOrCreate([], fundamental_types)

            if not is_import:
                ReplaceElement(type_factory.statement, new_type)

        for item_statement in self._data.item_statements:
            item_statement_name = item_statement.name.ToTerminalElement()

            new_statement = ItemStatement(
                item_statement.region,
                item_statement.name.visibility,
                item_statement_name,
                self.ParseTypeToType(
                    TerminalElement[Visibility](item_statement.region, Visibility.Private),
                    TerminalElement[str](
                        item_statement.region,
                        f"ItemStatement-Ln{item_statement.region.begin.line}Col{item_statement.region.begin.column}",
                    ),
                    item_statement.type,
                    TerminalElement[str](
                        item_statement.type.region, f"{item_statement_name.value}'s Type"
                    ),
                    [],
                    fundamental_types,
                ),
            )

            ReplaceElement(item_statement, new_statement)

        self._data.state = _State.ResolvedTypes

    # ----------------------------------------------------------------------
    def Finalize(self) -> None:
        self._data.state = _State.Finalizing

        if self._structure_type_factory:  # pylint: disable=protected-access
            self._structure_type_factory.Finalize()  # pylint: disable=protected-access

        for nested_value in self._data.final_nested.values():
            if id(nested_value) not in self._included_items:
                nested_value.Finalize()

        self._data.state = _State.Finalized

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def _ParseIdentifierTypeToType(
        self,
        visibility: TerminalElement[Visibility],
        name: TerminalElement[str],
        parse_type: ParseIdentifierType,
        ancestor_identities: list[TerminalElement[str]],
        fundamental_types: dict[str, PythonType[TypeDefinition]],
        *,
        region: Optional[Region],
    ) -> Type:
        if parse_type.is_global_reference is None:
            # ----------------------------------------------------------------------
            def GetNamespaceType() -> Type | None:
                namespace_root = self

                while True:
                    current_namespace = namespace_root

                    for identifier_index, identifier in enumerate(parse_type.identifiers):
                        potential_namespace_or_factory = current_namespace.nested.get(
                            identifier.value, None
                        )

                        if potential_namespace_or_factory is None:
                            if identifier_index == 0:
                                break

                            raise Errors.SimpleSchemaGeneratorException(
                                Errors.NamespaceInvalidType.Create(
                                    identifier.region, identifier.value
                                ),
                            )

                        # TODO: Handle visibility

                        is_last_identifier = identifier_index == len(parse_type.identifiers) - 1

                        if isinstance(potential_namespace_or_factory, Namespace):
                            if potential_namespace_or_factory._structure_type_factory is not None:
                                if is_last_identifier:
                                    return potential_namespace_or_factory._structure_type_factory.GetOrCreate(
                                        ancestor_identities, fundamental_types
                                    )

                            current_namespace = potential_namespace_or_factory

                        elif isinstance(potential_namespace_or_factory, FundamentalTypeFactory):
                            if is_last_identifier:
                                return potential_namespace_or_factory.GetOrCreate(
                                    ancestor_identities, fundamental_types
                                )

                            # The problem isn't with the current identifier, but rather the one
                            # that follows it.
                            raise Errors.SimpleSchemaGeneratorException(
                                Errors.NamespaceInvalidType.Create(
                                    parse_type.identifiers[identifier_index + 1].region,
                                    parse_type.identifiers[identifier_index + 1].value,
                                ),
                            )

                        else:
                            assert False, potential_namespace_or_factory  # pragma: no cover

                    # Move up the hierarchy
                    parent_namespace = namespace_root.parent
                    if parent_namespace is None:
                        break

                    namespace_root = parent_namespace

                return None

            # ----------------------------------------------------------------------

            namespace_type: Type | TypeDefinition | None = GetNamespaceType()

            if namespace_type is not None:
                assert isinstance(namespace_type, Type)

                # Determine if there is type-altering metadata present
                if parse_type.unresolved_metadata is not None:
                    with namespace_type.Resolve() as resolved_type:
                        if isinstance(resolved_type.type, TypeDefinition) and not isinstance(
                            resolved_type.type, StructureTypeDefinition
                        ):
                            type_definition = resolved_type.type

                            type_metadata_items: list[MetadataItem] = []

                            for metadata_item in list(
                                parse_type.unresolved_metadata.items.values()
                            ):
                                if metadata_item.name.value in type_definition.FIELDS:
                                    type_metadata_items.append(
                                        parse_type.unresolved_metadata.items.pop(
                                            metadata_item.name.value
                                        )
                                    )

                            if type_metadata_items:
                                namespace_type = type_definition.DeriveNewType(
                                    parse_type.region,
                                    Metadata(parse_type.region, type_metadata_items),
                                )

                return Type.Create(
                    visibility,
                    name,
                    namespace_type,
                    parse_type.cardinality,
                    parse_type.unresolved_metadata,
                    region=region or parse_type.region,
                )

        if len(parse_type.identifiers) == 1:
            fundamental_type_class = fundamental_types.get(parse_type.identifiers[0].value, None)
            if fundamental_type_class is not None:
                return Type.Create(
                    visibility,
                    name,
                    fundamental_type_class.CreateFromMetadata(
                        parse_type.region, parse_type.unresolved_metadata
                    ),
                    parse_type.cardinality,
                    parse_type.unresolved_metadata,
                    region=region or parse_type.region,
                )

        raise Errors.SimpleSchemaGeneratorException(
            Errors.NamespaceInvalidType.Create(
                parse_type.identifiers[0].region,
                parse_type.identifiers[0].value,
            ),
        )

    # ----------------------------------------------------------------------
    @staticmethod
    def _GetVisibility(
        item: Union["Namespace", FundamentalTypeFactory],
    ) -> TerminalElement[Visibility]:
        if isinstance(item, Namespace):
            if isinstance(item.statement, RootStatement):
                # This line will never be invoked, but it just seems wrong not to include it.
                # Disabling coverage on this line.
                return TerminalElement[Visibility](item.statement.region, item.visibility)
            elif isinstance(item.statement, ParseIncludeStatement):
                return TerminalElement[Visibility](item.statement.region, item.visibility)
            elif isinstance(item.statement, ParseStructureStatement):
                return item.statement.name.visibility
            else:
                assert False, item.statement  # pragma: no cover

        return item.statement.name.visibility

    # ----------------------------------------------------------------------
    def _ValidateVisibility(
        self,
        visibility: TerminalElement[Visibility],
    ) -> None:
        if isinstance(self.statement, RootStatement) and visibility.value == Visibility.Protected:
            raise Errors.SimpleSchemaGeneratorException(
                Errors.NamespaceVisibilityError.Create(visibility.region)
            )

    # ----------------------------------------------------------------------
    def _ValidateTypeName(
        self,
        name: str,
        region: Region,
        *,
        is_initial_validation: bool,
    ) -> None:
        assert self._data.state == _State.ResolvingTypeNames, self._data.state

        error_region: Region | None = None

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

            raise Errors.SimpleSchemaGeneratorException(
                Errors.NamespaceDuplicateTypeName.Create(
                    error_region,
                    name=name,
                    original_region=original_region,
                ),
            )

        parent = self.parent
        if parent is not None and not isinstance(parent.statement, RootStatement):
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

        self._working_nested: dict[str, list[tuple[Region, Namespace | FundamentalTypeFactory]]] = (
            {}
        )
        self._final_nested: dict[str, Namespace | FundamentalTypeFactory] = {}

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
        assert self._state.value <= _State.ResolvedIncludes.value
        return self._include_statements

    @property
    def item_statements(self) -> list[ParseItemStatement]:
        assert self._state.value <= _State.ResolvingTypes.value
        return self._item_statements

    @property
    def working_nested(self) -> dict[str, list[tuple[Region, Namespace | FundamentalTypeFactory]]]:
        assert self._state.value <= _State.ResolvingTypeNames.value
        return self._working_nested

    @property
    def final_nested(self) -> dict[str, Namespace | FundamentalTypeFactory]:
        assert self._state.value >= _State.ResolvingTypeNames.value
        return self._final_nested
