# ----------------------------------------------------------------------
# |
# |  TypeFactories.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-22 11:59:46
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the FundamentalTypeFactory and StructureTypeFactory objects"""

import threading

from abc import ABC, abstractmethod
from typing import cast, Type as PythonType, TYPE_CHECKING
from weakref import ref

from dbrownell_Common.ContextlibEx import ExitStack  # type: ignore[import-untyped]
from dbrownell_Common.Types import extension, override  # type: ignore[import-untyped]

from ...ANTLR.Grammar.Elements.Statements.ParseItemStatement import ParseItemStatement
from ...ANTLR.Grammar.Elements.Statements.ParseStructureStatement import ParseStructureStatement
from ....Elements.Common.TerminalElement import TerminalElement
from ....Elements.Common.Visibility import Visibility
from ....Elements.Statements.Statement import Statement
from ....Elements.Statements.StructureStatement import StructureStatement
from ....Elements.Types.FundamentalTypes import fundamental_types as all_fundamental_types
from ....Elements.Types.Type import Type
from ....Elements.Types.TypeDefinitions.StructureTypeDefinition import StructureTypeDefinition
from ....Elements.Types.TypeDefinitions.TypeDefinition import TypeDefinition
from ..... import Errors

if TYPE_CHECKING:  # pragma: no cover
    from .Namespace import Namespace


# ----------------------------------------------------------------------
class _TypeFactory(ABC):
    """Abstract base class for all type factories"""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        statement: ParseItemStatement | ParseStructureStatement,
        active_namespace: "Namespace",
    ) -> None:
        self._statement = statement

        self._active_namespace_ref = ref(active_namespace)

        self._created_type: Type | Exception | None = None
        self._created_type_ref_count: int = 0
        self._created_type_lock = threading.RLock()

    # ----------------------------------------------------------------------
    @property
    @extension
    def statement(self) -> Statement:
        return self._statement

    @property
    def active_namespace(self) -> "Namespace":
        active_namespace = self._active_namespace_ref()
        assert active_namespace is not None

        return active_namespace

    # ----------------------------------------------------------------------
    def GetOrCreate(
        self,
        ancestor_identities: list[TerminalElement[str]],
        fundamental_types: dict[str, PythonType[TypeDefinition]],
    ) -> Type:
        with self._created_type_lock:
            if self._created_type is None:
                result: Type | Exception

                try:
                    result = self._CreateImpl(ancestor_identities, fundamental_types)
                except Exception as ex:
                    result = ex

                self._created_type = result
            else:
                # We only want to increment the reference count when the type is referenced, not
                # when it is created
                self._created_type_ref_count += 1

        if isinstance(self._created_type, Exception):
            raise self._created_type

        if isinstance(self._created_type, Type):
            return self._created_type

        assert False, self._created_type  # pragma: no cover

    # ----------------------------------------------------------------------
    @abstractmethod
    def Finalize(self) -> None:
        """Finalizes the created element."""
        raise Exception("Abstract method")  # pragma: no cover

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @abstractmethod
    def _CreateImpl(
        self,
        ancestor_identities: list[TerminalElement[str]],
        fundamental_types: dict[str, PythonType[TypeDefinition]],
    ) -> Type:
        raise Exception("Abstract method")  # pragma: no cover


# ----------------------------------------------------------------------
class FundamentalTypeFactory(_TypeFactory):
    """Factory that creates a fundamental type"""

    # ----------------------------------------------------------------------
    @property
    @override
    def statement(self) -> ParseItemStatement:
        return cast(ParseItemStatement, super(FundamentalTypeFactory, self).statement)

    # ----------------------------------------------------------------------
    @override
    def Finalize(self) -> None:
        # Nothing to do here
        pass

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _CreateImpl(
        self,
        ancestor_identities: list[TerminalElement[str]],
        fundamental_types: dict[str, PythonType[TypeDefinition]],
    ) -> Type:
        statement = self.statement

        name_element = statement.name.ToTerminalElement()

        return self.active_namespace.ParseTypeToType(
            statement.name.visibility,
            name_element,
            statement.type,
            name_element,
            ancestor_identities,
            fundamental_types,
            region=statement.region,
        )


# ----------------------------------------------------------------------
class StructureTypeFactory(_TypeFactory):
    """Factory that creates a structure type"""

    # ----------------------------------------------------------------------
    @property
    @override
    def statement(self) -> ParseStructureStatement:
        return cast(ParseStructureStatement, super(StructureTypeFactory, self).statement)

    # ----------------------------------------------------------------------
    @override
    def Finalize(self) -> None:
        assert isinstance(self._created_type, Type), self._created_type

        the_type: Type | TypeDefinition = self._created_type

        assert isinstance(the_type, Type), the_type

        while isinstance(the_type, Type):
            the_type = the_type.type

        assert isinstance(the_type, StructureTypeDefinition), the_type

        for child in self.statement.children:
            if child.is_disabled__:
                continue

            the_type.structure.children.append(child)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _CreateImpl(
        self,
        ancestor_identities: list[TerminalElement[str]],
        fundamental_types: dict[str, PythonType[TypeDefinition]],
    ) -> Type:
        statement = self.statement
        active_namespace = self.active_namespace

        base_types: list[Type] = []

        if statement.bases:
            ancestor_identities.append(statement.name.ToTerminalElement())
            with ExitStack(ancestor_identities.pop):
                for base_index, base in enumerate(statement.bases):
                    base_type = active_namespace.ParseTypeToType(
                        TerminalElement[Visibility](base.region, Visibility.Private),
                        TerminalElement[str](base.region, f"Base{base_index}"),
                        base,
                        TerminalElement[str](
                            base.region, f"Base type '{base.display_type}' (index {base_index})"
                        ),
                        ancestor_identities,
                        fundamental_types,
                    )

                    with base_type.Resolve() as resolved_base_type:
                        if not resolved_base_type.cardinality.is_single:
                            raise Errors.SimpleSchemaGeneratorException(
                                Errors.TypeFactoryInvalidBaseCardinality.Create(base.region)
                            )

                        if not isinstance(
                            resolved_base_type.type, all_fundamental_types
                        ) and not isinstance(resolved_base_type.type, StructureTypeDefinition):
                            raise Errors.SimpleSchemaGeneratorException(
                                Errors.TypeFactoryInvalidBaseType.Create(resolved_base_type.region)
                            )

                        if len(statement.bases) > 1 and not isinstance(
                            resolved_base_type.type, StructureTypeDefinition
                        ):
                            raise Errors.SimpleSchemaGeneratorException(
                                Errors.TypeFactoryInvalidBaseTypeMultiInheritance.Create(
                                    resolved_base_type.region
                                )
                            )

                    base_types.append(base_type)

        return Type.Create(
            statement.name.visibility,
            statement.name.ToTerminalElement(),
            StructureTypeDefinition(
                statement.region,
                StructureStatement(
                    statement.region,
                    TerminalElement[str](statement.region, f"{statement.name.value}Struct"),
                    base_types,
                    [],  # The children will be populated during Finalize
                ),
            ),
            statement.cardinality,
            statement.unresolved_metadata,
        )
