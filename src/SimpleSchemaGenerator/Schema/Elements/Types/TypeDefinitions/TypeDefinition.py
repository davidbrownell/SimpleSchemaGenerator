# ----------------------------------------------------------------------
# |
# |  TypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-14 13:21:18
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the TypeDefinition object."""

from abc import abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field, fields, Field, MISSING, _MISSING_TYPE
from typing import Any, ClassVar

from dbrownell_Common.Types import override

from SimpleSchemaGenerator.Schema.Elements.Types.Impl.TypeImpl import TypeImpl
from SimpleSchemaGenerator.Schema.Elements.Common.Metadata import Metadata, MetadataItem

from SimpleSchemaGenerator.Schema.Elements.Expressions.Expression import Expression

from SimpleSchemaGenerator.Common.Error import Error
from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class TypeDefinition(TypeImpl):
    """A type that does not have cardinality or metadata."""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = ""
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = ()
    FIELDS: ClassVar[dict[str, Field]] = field(init=False)

    # ----------------------------------------------------------------------
    @classmethod
    def __new__(cls, *args, **kwargs) -> "TypeDefinition":
        if cls.NAME == "":
            raise Exception(f"NAME must be defined for '{cls.__name__}'.")  # noqa: EM102, TRY003

        if not cls.SUPPORTED_PYTHON_TYPES:
            raise Exception(f"SUPPORTED_PYTHON_TYPES must be defined for '{cls.__name__}'.")  # noqa: EM102, TRY003

        cls.__initialize_fields__()
        return super().__new__(cls)

    # ----------------------------------------------------------------------
    @classmethod
    def __initialize_fields__(cls) -> None:
        if hasattr(cls, "FIELDS"):
            return

        type_definition_fields: set[str] = {
            type_field.name for type_field in fields(TypeDefinition) if type_field.init
        }

        class_fields: dict[str, Field] = {
            type_field.name: type_field
            for type_field in fields(cls)
            if type_field.init and type_field.name not in type_definition_fields
        }

        cls.FIELDS = class_fields

    # ----------------------------------------------------------------------
    @classmethod
    def CreateFromMetadata(
        cls,
        region: Region,
        metadata: Metadata | None,
    ) -> "TypeDefinition":
        cls.__initialize_fields__()

        return cls._Create(
            region,
            metadata,
            lambda _: MISSING,
        )

    # ----------------------------------------------------------------------
    def DeriveNewType(
        self,
        region: Region,
        metadata: Metadata,
    ) -> "TypeDefinition":
        return self.__class__._Create(  # noqa: SLF001
            region,
            metadata,
            lambda field_name: getattr(self, field_name),
        )

    # ----------------------------------------------------------------------
    @override
    def ToPythonInstance(
        self,
        expression_or_value: Expression | object,
    ) -> object:
        # ----------------------------------------------------------------------
        def Impl(
            value: object,
        ) -> object:
            if not isinstance(value, self.SUPPORTED_PYTHON_TYPES):
                raise TypeError(
                    Errors.basic_type_validate_invalid_python_type.format(
                        python_type=type(value).__name__,
                        type=self.display_type,
                    ),
                )

            return self._ToPythonInstanceImpl(value)

        # ----------------------------------------------------------------------

        if isinstance(expression_or_value, Expression):
            try:
                return Impl(expression_or_value.value)
            except Errors.SimpleSchemaGeneratorError as ex:
                ex.errors[0].regions.append(expression_or_value.region)
                raise
            except Exception as ex:
                raise Errors.SimpleSchemaGeneratorError(
                    Error.Create(
                        ex,
                        expression_or_value.region,
                        include_callstack=False,
                    ),
                ) from ex

        return Impl(expression_or_value)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        return self.NAME

    # ----------------------------------------------------------------------
    @classmethod
    def _Create(
        cls,
        region: Region,
        metadata: Metadata | None,
        on_missing_metadata_func: Callable[[str], _MISSING_TYPE | object],
    ) -> "TypeDefinition":
        pop_metadata_item_func: Callable[[str], MetadataItem | _MISSING_TYPE] | None = None

        if metadata is None:
            # ----------------------------------------------------------------------
            def PopMetadataItem(name: str) -> MetadataItem | _MISSING_TYPE:  # noqa: ARG001
                return MISSING

            # ----------------------------------------------------------------------

            pop_metadata_item_func = PopMetadataItem
        else:
            # ----------------------------------------------------------------------
            def PopMetadataItem(
                name: str,
            ) -> MetadataItem | _MISSING_TYPE:
                assert metadata is not None
                return metadata.items.pop(name, MISSING)

            # ----------------------------------------------------------------------

            pop_metadata_item_func = PopMetadataItem

        assert pop_metadata_item_func is not None

        construct_args: dict[str, Any] = {
            "region": region,
        }

        for field_value in cls.FIELDS.values():
            assert field_value.name not in construct_args, field_value.name

            metadata_item = pop_metadata_item_func(field_value.name)

            if metadata_item is MISSING:
                metadata_value = on_missing_metadata_func(field_value.name)
                if metadata_value is MISSING:
                    continue
            else:
                assert isinstance(metadata_item, MetadataItem), metadata_item

                # Note that this content is imported here to avoid circular dependencies
                from SimpleSchemaGenerator.Schema.Elements.Types.Impl.CreateTypeFromPythonAnnotation import (
                    CreateTypeFromPythonAnnotation,
                )

                metadata_type = CreateTypeFromPythonAnnotation(
                    field_value.type,
                    has_default_value=field_value.default is not MISSING
                    or field_value.default_factory is not MISSING,
                )

                metadata_value = metadata_type.ToPythonInstance(metadata_item.expression)

            if metadata_value is not None or (
                field_value.default is MISSING and field_value.default_factory is MISSING
            ):
                construct_args[field_value.name] = metadata_value

        try:
            return cls(**construct_args)
        except Errors.SimpleSchemaGeneratorError as ex:
            ex.errors[0].regions.append(metadata.region if metadata is not None else region)
            raise
        except Exception as ex:
            raise Errors.SimpleSchemaGeneratorError(
                Error.Create(
                    ex,
                    metadata.region if metadata is not None else region,
                    include_callstack=False,
                ),
            ) from ex

    # ----------------------------------------------------------------------
    @abstractmethod
    def _ToPythonInstanceImpl(
        self,
        value: object,
    ) -> object:
        raise Exception("Abstract method")  # pragma: no cover  # noqa: EM101, TRY003
