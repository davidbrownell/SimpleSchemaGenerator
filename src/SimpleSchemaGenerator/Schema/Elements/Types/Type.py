# ----------------------------------------------------------------------
# |
# |  Type.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-18 10:19:59
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Type object"""

from contextlib import contextmanager
from dataclasses import dataclass, field, InitVar
from enum import auto, Enum
from types import NoneType
from typing import Any, cast, Iterator, Optional, Union
from weakref import ref, ReferenceType as WeakReferenceType

from dbrownell_Common.Types import extension, override

from SimpleSchemaGenerator.Schema.Elements.Common.TerminalElement import Element  # type: ignore[import-untyped]

from .Impl.TypeImpl import TypeImpl
from .TypeDefinitions.TypeDefinition import TypeDefinition
from .TypeDefinitions.VariantTypeDefinition import VariantTypeDefinition
from ..Common.Cardinality import Cardinality
from ..Common.Metadata import Metadata
from ..Common.TerminalElement import TerminalElement
from ..Common.Visibility import Visibility, VisibilityTrait
from ..Expressions.Expression import Expression
from ..Expressions.ListExpression import ListExpression
from ..Expressions.NoneExpression import NoneExpression
from ....Common.Error import Error
from ....Common.Region import Region
from .... import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Type(VisibilityTrait, TypeImpl):
    """A type that references another Type or TypeDefinition, but adds specific cardinality and/or metadata"""

    # ----------------------------------------------------------------------
    # |
    # |  Public Types
    # |
    # ----------------------------------------------------------------------
    class Category(Enum):
        """Value that identifies the kind of type being created"""

        Source = auto()  # Wrapper for the original TypeDefinition
        Reference = (
            auto()
        )  # References the type in the creation of a new Type (perhaps a container or optional)
        Alias = auto()  # A new name for an existing type

    # ----------------------------------------------------------------------
    # |
    # |  Public Data
    # |
    # ----------------------------------------------------------------------
    type: Union[TypeDefinition, "Type"]
    name: TerminalElement[str]

    cardinality: Cardinality

    _metadata: Union[
        Optional[Metadata],  # Valid before `ResolveMetadata` is called
        dict[  # Valid after `ResolveMetadata` is called
            str,
            Union[
                TerminalElement,  # Metadata item that was recognized and resolved
                Expression,  # Metadata item that was not recognized and therefore not resolved
            ],
        ],
    ]

    category: Category = field(init=False)

    _is_shared: Optional[bool] = field(
        init=False, default=None
    )  # Valid after `ResolvedIsShared` is called

    is_source: InitVar[bool] = field(kw_only=True, default=False)

    # Indicate that is reference's region should not be added in the exception's region stack.
    # This will generally be used when the type associated with the reference was dynamically
    # created in code and will not be meaningful to the caller.
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
        the_type: Union[TypeDefinition, "Type"],
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

        if isinstance(the_type, TypeDefinition):
            is_source = True

            if cardinality.is_single:
                referenced_type = the_type
            else:
                # Ensure that all Types ultimately resolve to a Type with a single cardinality that
                # points to a TypeDefinition. This will let us support the `::item` syntax, which
                # allows access to a single element that was defined within the context of an array.
                referenced_type = cls(  # type: ignore
                    region,
                    TerminalElement[Visibility](the_type.region, Visibility.Private),
                    the_type,
                    TerminalElement[str](
                        the_type.region,
                        f"{name.value}-Item-Ln{the_type.region.begin.line}-Col{the_type.region.begin.column}",
                    ),
                    Cardinality(the_type.region, None, None),
                    None,
                    is_source=True,
                    suppress_region_in_exceptions=suppress_region_in_exceptions,
                )
        else:
            is_source = False

            referenced_type = the_type  # type: ignore

        return cls(
            region,
            visibility,
            referenced_type,
            name,
            cardinality,
            metadata,
            is_source=is_source,
            suppress_region_in_exceptions=suppress_region_in_exceptions,
        )

    # ----------------------------------------------------------------------
    def __post_init__(
        self,
        is_source: bool,
    ) -> None:
        # Category
        if is_source:
            category = Type.Category.Source
        elif self.cardinality.is_single:
            category = Type.Category.Alias

            if isinstance(self.type, Type):
                object.__setattr__(self, "cardinality", self.type.cardinality)
        else:
            category = Type.Category.Reference

            if self.cardinality.is_optional and isinstance(self.type, Type):
                with self.type.Resolve() as resolved_type:
                    if resolved_type.cardinality.is_optional:
                        raise Errors.SimpleSchemaGeneratorException(
                            Errors.TypeOptionalToOptional.Create(self.cardinality.region)
                        )

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

    # ----------------------------------------------------------------------
    def ResolveMetadata(
        self,
        metadata: dict[str, Union[TerminalElement, Expression]],
    ) -> None:
        if self.is_metadata_resolved:
            raise RuntimeError("Metadata has already been resolved.")

        object.__setattr__(self, "_metadata", metadata)

    # ----------------------------------------------------------------------
    @property
    def is_shared_resolved(self) -> bool:
        return self._is_shared is not None

    @property
    def is_shared(self) -> bool:
        if self._is_shared is None:
            raise RuntimeError("Shared status has not been resolved.")

        return self._is_shared

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

        except Errors.SimpleSchemaGeneratorException as ex:
            if not self.suppress_region_in_exceptions and self.region not in ex.errors[0].regions:
                ex.errors[0].regions.append(self.region)

            raise

        except Exception as ex:
            raise Errors.SimpleSchemaGeneratorException(
                Error.Create(
                    ex,
                    self.region,
                    include_callstack=False,
                ),
            ) from ex

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
            if isinstance(resolved_type.type, VariantTypeDefinition):
                return resolved_type.type.ToPythonInstanceOverride(
                    resolved_type,
                    expression_or_value,
                )

            return resolved_type.ToPythonInstanceImpl(expression_or_value)

    # ----------------------------------------------------------------------
    @extension
    def ToPythonInstanceImpl(
        self,
        expression_or_value: Expression | Any,
    ) -> Any:
        # This method is called during normal operations or when a VariantType has determined that
        # special cardinality rules are not in play.
        assert not isinstance(expression_or_value, (NoneExpression, NoneType))

        self.cardinality.Validate(expression_or_value)

        items: Optional[list] = None

        if isinstance(expression_or_value, ListExpression):
            items = expression_or_value.value
        elif isinstance(expression_or_value, list):
            items = expression_or_value

        if items is not None:
            return [self.type.ToPythonInstance(item) for item in items]

        return self.type.ToPythonInstance(expression_or_value)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        display = self.type.display_type

        if not self.cardinality.is_single and display.endswith("}"):
            display = f"<{display}>"

        if self.category != Type.Category.Alias:
            display = f"{display}{self.cardinality}"

        return display

    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from VisibilityTrait._GenerateAcceptDetails(self)

        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "name", self.name
        )
        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "cardinality", self.cardinality
        )

        if isinstance(self._metadata, Metadata):
            yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
                "metadata", self._metadata
            )

        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "type",
            cast(WeakReferenceType[Element], ref(self.type)),
        )
