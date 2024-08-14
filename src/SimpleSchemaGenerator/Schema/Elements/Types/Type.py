# ----------------------------------------------------------------------
# |
# |  Type.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-10 12:32:10
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Type object."""

from contextlib import contextmanager
from dataclasses import dataclass, field, InitVar
from enum import auto, Enum
from typing import Any, ClassVar, Iterator, Optional, Type as PythonType, Union

from .Impl.TypeImpl import TypeImpl
from .TypeDefinitions.TypeDefinition import TypeDefinition
from ..Common.Cardinality import Cardinality
from ..Common.Metadata import Metadata
from ..Common.TerminalElement import TerminalElement
from ..Common.Visibility import Visibility, VisibilityTrait
from ..Expressions.Expression import Expression
from ....Common.Region import Region


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Type(VisibilityTrait, TypeImpl):
    """A fully resolved type that includes cardinality and metadata."""

    # ----------------------------------------------------------------------
    # |
    # |  Public Types
    # |
    # ----------------------------------------------------------------------
    class Category(Enum):
        """Identifies the category of the type."""

        Definition = auto()  # This is a type definition with cardinality and metadata
        Reference = (
            auto()
        )  # References the type in the creation of a new type (perhaps a container or optional)
        Alias = auto()  # A different name for another Type

    # ----------------------------------------------------------------------
    # |
    # |  Public Data
    # |
    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Type"

    type: Union["Type", TypeDefinition]
    name: TerminalElement[str]

    cardinality: Cardinality

    _metadata: Union[
        Optional[Metadata],  # Valid before `ResolveMetadata` is called
        dict[str, Union[TerminalElement, Expression]],  # Valid after `ResolveMetadata` is called
    ]

    category: Category = field(init=False)

    # Valid after `ResolveIsShared` is called
    _is_shared: Optional[bool] = field(init=False, default=None)

    is_definition: InitVar[bool] = field(kw_only=True, default=False)

    # Indicate that is reference's range should not be added in the exception's region stack.
    # This will generally be used when the associated type was dynamically created in code and
    # its region will not be meaningful to the caller.
    suppress_region_in_exceptions: bool = field(kw_only=True, default=False)

    # ----------------------------------------------------------------------
    # |
    # |  Public Methods
    # |
    # ----------------------------------------------------------------------
    @classmethod
    def Create(
        cls,
        visibility: TerminalElement[Visibility],
        name: TerminalElement[str],
        the_type: Union["Type", TypeDefinition],
        cardinality: Cardinality,
        metadata: Optional[Metadata],
        *,
        region: Optional[Region] = None,
        suppress_region_in_exceptions: bool = False,
    ) -> "Type":
        if metadata and not metadata.items:
            metadata = None

        if region is None:
            region = the_type.region

        is_definition: bool | None = None
        referenced_type: Type | TypeDefinition | None = None

        if isinstance(the_type, TypeDefinition):
            is_definition = True

            if cardinality.is_single:
                referenced_type = the_type
                assert is_definition
            else:
                # This code ensures that we always have a Type instance with a cardinality of 1.
                # It is important to have this instance in case other types reference the container
                # item with the "::item" suffix.
                referenced_type = cls(
                    region,
                    TerminalElement[Visibility](the_type.region, Visibility.Private),
                    the_type,
                    TerminalElement[str](
                        the_type.region,
                        f"{name.value}-Item-Ln{the_type.region.begin.line}Col{the_type.region.begin.column}",
                    ),
                    Cardinality(the_type.region, None, None),
                    None,
                    is_definition=True,
                    suppress_region_in_exceptions=suppress_region_in_exceptions,
                )

        else:
            is_definition = False
            referenced_type = the_type

        assert is_definition is not None
        assert referenced_type is not None

        return cls(
            region,
            visibility,
            referenced_type,
            name,
            cardinality,
            metadata,
            is_definition=is_definition,
            suppress_region_in_exceptions=suppress_region_in_exceptions,
        )

    # ----------------------------------------------------------------------
    def __post_init__(
        self,
        is_definition: bool,
    ) -> None:
        super(Type, self).__post_init__()

        # Category
        if is_definition:
            category = Type.Category.Definition

        elif self.cardinality.is_single:
            category = Type.Category.Alias

            if isinstance(self.type, Type):
                object.__setattr__(self, "cardinality", self.type.cardinality)

        else:
            category = Type.Category.Reference

            if self.cardinality.is_optional and isinstance(self.type, Type):
                with self.type.Resolve() as resolved_type:
                    if resolved_type.cardinality.is_optional:
                        assert False, "BugBug"

        object.__setattr__(self, "category", category)

    # ----------------------------------------------------------------------
    @property
    def is_metadata_resolved(self) -> bool:
        return isinstance(self._metadata, dict)

    @property
    def unresolved_metadata(self) -> Optional[Metadata]:
        if isinstance(self._metadata, dict):
            raise RuntimeError("Metadata has been resolved.")

        return self._metadata

    @property
    def resolved_metadata(self) -> dict[str, Union[TerminalElement, Expression]]:
        if self._metadata is None or isinstance(self._metadata, Metadata):
            raise RuntimeError("Metadata has not been resolved.")

        return self._metadata

    @property
    def is_shared_resolved(self) -> bool:
        return self._is_shared is not None

    @property
    def is_shared(self) -> bool:
        if self._is_shared is None:
            raise RuntimeError("Shared status has not been resolved.")

        return self._is_shared

    # ----------------------------------------------------------------------
    def ResolveMetadata(
        self,
        metadata: dict[str, Union[TerminalElement, Expression]],
    ) -> None:
        if self.is_metadata_resolved:
            raise RuntimeError("Metadata has already been resolved.")

        object.__setattr__(self, "_metadata", metadata)

    # ----------------------------------------------------------------------
    def ResolveIsShared(
        self,
        is_shared: bool,
    ) -> None:
        if self.is_shared_resolved:
            raise RuntimeError("Shared status has already been resolved.")

        object.__setattr__(self, "_is_shared", is_shared)

    # ----------------------------------------------------------------------
    @contextmanager
    def Resolve(self) -> Iterator["Type"]:
        try:
            if self.category != Type.Category.Alias or isinstance(self.type, TypeDefinition):
                yield self
                return

            assert isinstance(self.type, Type), self.type
            with self.type.Resolve() as resolved_type:
                yield resolved_type

        except SimpleSchemaGeneratorException as ex:
            assert False, "BugBug1"

        except Exception as ex:
            raise SimpleSchemaGeneratorException(ExceptionError.Create(ex)) from ex

    # ----------------------------------------------------------------------
    @override
    def ToPythonInstance(
        self,
        expression_or_value: Expression | Any,
    ) -> Any:
        if isinstance(expression_or_value, (NoneExpression, NoneType)):
            self.cardinality.Validate(expression_or_value)
            return None

        if self.cardinality.is_optional:
            return self.type.ToPythonInstance(expression_or_value)

        with self.Resolve() as resolved_type:
            # Variants are special in that the subtypes may be collections or individual types.
            # If we are looking at a variant, let it handle the cardinality stuff using its own
            # custom logic.
            if isinstance(resolved_type.type, VariantType):
                return resolved_type.type.ToPythonReferenceOverride(
                    resolved_type,
                    expression_or_value,
                )

            return resolved_type.ToPythonInstanceImpl(expression_or_value)

    # ----------------------------------------------------------------------
    def ToPythonInstanceImpl(
        self,
        expression_or_value: Expression | Any,
    ) -> Any:
