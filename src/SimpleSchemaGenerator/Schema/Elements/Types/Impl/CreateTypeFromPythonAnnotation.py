# ----------------------------------------------------------------------
# |
# |  CreateTypeFromPythonAnnotation.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-18 10:17:42
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains functionality that creates a Type from a Python type annotation."""

from enum import EnumMeta
from types import GenericAlias, NoneType
from typing import Any, _BaseGenericAlias, _UnionGenericAlias

from ..Type import Type
from ..TypeDefinitions.BooleanTypeDefinition import BooleanTypeDefinition
from ..TypeDefinitions.EnumTypeDefinition import EnumTypeDefinition
from ..TypeDefinitions.IntegerTypeDefinition import IntegerTypeDefinition
from ..TypeDefinitions.NumberTypeDefinition import NumberTypeDefinition
from ..TypeDefinitions.StringTypeDefinition import StringTypeDefinition
from ..TypeDefinitions.TupleTypeDefinition import TupleTypeDefinition
from ..TypeDefinitions.TypeDefinition import TypeDefinition
from ..TypeDefinitions.VariantTypeDefinition import VariantTypeDefinition
from ...Common.Cardinality import Cardinality
from ...Common.TerminalElement import TerminalElement
from ...Common.Visibility import Visibility
from ...Expressions.IntegerExpression import IntegerExpression
from .....Common.Region import Region
from ..... import Errors


# ----------------------------------------------------------------------
def CreateTypeFromPythonAnnotation(
    python_type_annotation,
    *,
    has_default_value: bool,
) -> Type:
    cardinality_min: int = 0 if has_default_value else 1
    cardinality_max: int | None = 1

    type_definition: TypeDefinition | None = None

    if isinstance(python_type_annotation, _UnionGenericAlias):
        # Optional or Variant
        types: list[Any] = []

        for contained_type in python_type_annotation.__args__:
            if contained_type is NoneType:
                continue

            types.append(contained_type)

        if len(types) == 1:
            # Optional
            cardinality_min = 0
            python_type_annotation = types[0]
        else:
            # Variant
            type_definition = VariantTypeDefinition(
                Region.CreateFromCode(),
                [
                    CreateTypeFromPythonAnnotation(the_type, has_default_value=False)
                    for the_type in types
                ],
            )

    while type_definition is None and (
        isinstance(python_type_annotation, GenericAlias)
        or isinstance(python_type_annotation, _BaseGenericAlias)
    ):
        if python_type_annotation.__origin__ == list:
            cardinality_max = None

            assert len(python_type_annotation.__args__) == 1, python_type_annotation.__args__
            python_type_annotation = python_type_annotation.__args__[0]

        elif python_type_annotation.__origin__ == tuple:
            type_definition = TupleTypeDefinition(
                Region.CreateFromCode(),
                [
                    CreateTypeFromPythonAnnotation(the_type, has_default_value=False)
                    for the_type in python_type_annotation.__args__
                ],
            )

    if type_definition is None:
        if isinstance(python_type_annotation, EnumMeta):
            type_definition = EnumTypeDefinition(Region.CreateFromCode(), python_type_annotation)
        elif python_type_annotation == bool:
            type_definition = BooleanTypeDefinition(Region.CreateFromCode())
        elif python_type_annotation == int:
            type_definition = IntegerTypeDefinition(Region.CreateFromCode())
        elif python_type_annotation == float:
            type_definition = NumberTypeDefinition(Region.CreateFromCode())
        elif python_type_annotation == str:
            type_definition = StringTypeDefinition(Region.CreateFromCode())
        else:
            raise Exception(
                Errors.create_type_from_annotation_invalid_type.format(
                    value=python_type_annotation.__name__
                )
            )

    return Type.Create(
        TerminalElement[Visibility](type_definition.region, Visibility.Private),
        TerminalElement[str](type_definition.region, type_definition.NAME),
        type_definition,
        Cardinality(
            Region.CreateFromCode(),
            (
                IntegerExpression(Region.CreateFromCode(), cardinality_min)
                if cardinality_min is not None
                else None
            ),
            (
                IntegerExpression(Region.CreateFromCode(), cardinality_max)
                if cardinality_max is not None
                else None
            ),
        ),
        None,
        suppress_region_in_exceptions=True,
    )
