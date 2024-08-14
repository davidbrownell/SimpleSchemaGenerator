# ----------------------------------------------------------------------
# |
# |  TypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-10 11:05:33
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the TypeDefinition object"""

from abc import abstractmethod
from dataclasses import dataclass, field, fields, Field, MISSING
from typing import Any, Callable, ClassVar, Optional, Type as PythonType, Union

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from ..Impl.TypeImpl import TypeImpl
from ...Common.Metadata import Metadata, MetadataItem
from ...Expressions.Expression import Expression
from .....Common.Error import Error, ExceptionError, SimpleSchemaGeneratorException
from .....Common.Region import Region
from ..... import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class TypeDefinition(TypeImpl):
    """A type that does not have cardinality or metadata."""

    # ----------------------------------------------------------------------
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = ()

    # This will be initialized when an instance is first created
    FIELDS: ClassVar[dict[str, Field]] = field(init=False)

    # ----------------------------------------------------------------------
    @classmethod
    def __new__(cls, *args, **kwargs):  # pylint: disable=unused-argument
        if not cls.SUPPORTED_PYTHON_TYPES:
            raise Exception(f"SUPPORTED_PYTHON_TYPES must be defined for '{cls.__name__}'.")

        cls.__initialize_fields__()
        return super(TypeDefinition, cls).__new__(cls)

    # ----------------------------------------------------------------------
    @classmethod
    def __initialize_fields__(cls) -> None:
        if hasattr(cls, "FIELDS"):
            # This type has already been initialized
            return

        type_definition_fields: dict[str, Field] = {
            type_field.name: type_field for type_field in fields(TypeDefinition) if type_field.init
        }

        derived_fields: dict[str, Field] = {
            type_field.name: type_field
            for type_field in fields(cls)
            if type_field.init and type_field.name not in type_definition_fields
        }

        cls.FIELDS = derived_fields

    # ----------------------------------------------------------------------
    @classmethod
    def CreateFromMetadata(
        cls,
        region: Region,
        metadata: Optional[Metadata],
    ) -> "TypeDefinition":
        cls.__initialize_fields__()

        return cls._Create(
            region,
            metadata,
            lambda field_name: _DoesNotExist.instance,
        )

    # ----------------------------------------------------------------------
    def DeriveNewTypeDefinition(
        self,
        region: Region,
        metadata: Metadata,
    ) -> "TypeDefinition":
        """Creates a new TypeDefinition using the current type as a template."""

        return self.__class__._Create(  # pylint: disable=protected-access
            region,
            metadata,
            lambda name: getattr(self, name),
        )

    # ----------------------------------------------------------------------
    @override
    def ToPythonInstance(
        self,
        expression_or_value: Expression | Any,
    ) -> Any:
        # ----------------------------------------------------------------------
        def Impl(
            value: Any,
        ) -> Any:
            if not isinstance(value, self.SUPPORTED_PYTHON_TYPES):
                raise Exception(
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

            except SimpleSchemaGeneratorException as ex:
                ex.errors[0].regions.append(expression_or_value.region)
                raise

            except Exception as ex:
                raise SimpleSchemaGeneratorException(ExceptionError.Create(ex)) from ex
                raise Error.CreateAsException(str(ex), expression_or_value.region) from ex

        return Impl(expression_or_value)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @classmethod
    def _Create(
        cls,
        region: Region,
        metadata: Optional[Metadata],
        on_missing_metadata_func: Callable[[str], Union[Any, "_DoesNotExist"]],
    ) -> "TypeDefinition":
        pop_metadata_item_func: Optional[Callable[[str], MetadataItem | _DoesNotExist]] = None

        if metadata is None:
            pop_metadata_item_func = lambda name: _DoesNotExist.instance
        else:
            # ----------------------------------------------------------------------
            def PopMetadataItem(
                name: str,
            ) -> MetadataItem | _DoesNotExist:
                assert metadata is not None
                return metadata.items.pop(name, _DoesNotExist.instance)

            # ----------------------------------------------------------------------

            pop_metadata_item_func = PopMetadataItem

        assert pop_metadata_item_func is not None

        construct_args: dict[str, Any] = {
            "region": region,
        }

        for class_field in cls.FIELDS.values():
            assert class_field.name not in construct_args, class_field.name

            metadata_item = pop_metadata_item_func(class_field.name)

            if metadata_item is _DoesNotExist.instance:
                metadata_value = on_missing_metadata_func(class_field.name)
                if metadata_value is _DoesNotExist.instance:
                    continue

            else:
                assert isinstance(metadata_item, MetadataItem), metadata_item

                assert False  # BugBug

                metadata_value = metadata_type.ToPythonInstance(metadata_item.expression)

            if metadata_value is not None or (
                class_field.default is MISSING and class_field.default_factory is MISSING
            ):
                construct_args[class_field.name] = metadata_value

        try:
            return cls(**construct_args)

        except SimpleSchemaGeneratorException as ex:
            ex.errors[0].regions.append(region)
            raise

        except Exception as ex:
            raise SimpleSchemaGeneratorException(ExceptionError.Create(ex)) from ex

    # ----------------------------------------------------------------------
    @abstractmethod
    def _ToPythonInstanceImpl(
        self,
        value: Any,
    ) -> Any:
        raise Exception("Abstract method")  # pragma: no cover


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
class _DoesNotExist:
    """Placeholder for fields that do not exist"""

    # Set below
    instance: "_DoesNotExist" = None  # type: ignore


_DoesNotExist.instance = _DoesNotExist()
