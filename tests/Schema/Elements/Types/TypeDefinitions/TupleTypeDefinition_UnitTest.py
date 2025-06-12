# ----------------------------------------------------------------------
# |
# |  TupleTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-19 12:58:09
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for TupleTypeDefinition.py."""

import re
import sys

from pathlib import Path
from unittest.mock import Mock

import pytest

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator.Schema.Elements.Common.Cardinality import Cardinality
from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression
from SimpleSchemaGenerator.Schema.Elements.Types.Type import Type
from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.TupleTypeDefinition import *
from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.IntegerTypeDefinition import (
    IntegerTypeDefinition,
)
from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.StringTypeDefinition import (
    StringTypeDefinition,
)

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_Create():
    types = [Mock(), Mock()]

    td = TupleTypeDefinition(Mock(), types)

    assert td.NAME == "Tuple"
    assert td.SUPPORTED_PYTHON_TYPES == (tuple,)
    assert td.types is types

    assert TestElementVisitor(td) == [
        td,
        ("types", types),
    ]


# ----------------------------------------------------------------------
def test_ErrorCreateWithoutTypes():
    with pytest.raises(
        Errors.SimpleSchemaGeneratorError,
        match=re.escape("No types were provided. (filename, Ln 1, Col 2 -> Ln 3, Col 4)"),
    ):
        TupleTypeDefinition(Region.Create(Path("filename"), 1, 2, 3, 4), [])


# ----------------------------------------------------------------------
def test_DisplayType():
    assert (
        TupleTypeDefinition(
            Mock(),
            [
                Type.Create(
                    Mock(),
                    Mock(),
                    IntegerTypeDefinition(Mock(), max=10),
                    Cardinality(Mock(), None, None),
                    None,
                ),
                Type.Create(
                    Mock(),
                    Mock(),
                    StringTypeDefinition(Mock()),
                    Cardinality(Mock(), None, None),
                    None,
                ),
                Type.Create(
                    Mock(),
                    Mock(),
                    IntegerTypeDefinition(Mock()),
                    Cardinality(Mock(), IntegerExpression(Mock(), 0), IntegerExpression(Mock(), 1)),
                    None,
                ),
                Type.Create(
                    Mock(),
                    Mock(),
                    StringTypeDefinition(Mock()),
                    Cardinality(Mock(), IntegerExpression(Mock(), 1), None),
                    None,
                ),
            ],
        ).display_type
        == "(<Integer {<= 10}>, String, Integer?, String+, )"
    )


# ----------------------------------------------------------------------
def test_ToPythonInstance():
    td = TupleTypeDefinition(
        Mock(),
        [
            Type.Create(
                Mock(),
                Mock(),
                IntegerTypeDefinition(Mock()),
                Cardinality(Mock(), IntegerExpression(Mock(), 2), IntegerExpression(Mock(), 2)),
                None,
            ),
            Type.Create(
                Mock(),
                Mock(),
                StringTypeDefinition(Mock()),
                Cardinality(Mock(), None, None),
                None,
            ),
        ],
    )

    assert td.ToPythonInstance(([1, 2], "test")) == ([1, 2], "test")


# ----------------------------------------------------------------------
def test_ToPythonInstanceErrors():
    td = TupleTypeDefinition(
        Region.Create(Path("filename1"), 1, 2, 3, 4),
        [
            Type.Create(
                Mock(),
                Mock(),
                IntegerTypeDefinition(Region.Create(Path("filename2"), 10, 20, 30, 40)),
                Cardinality(Mock(), None, None),
                None,
            ),
            Type.Create(
                Mock(),
                Mock(),
                StringTypeDefinition(Region.Create(Path("filename3"), 11, 22, 33, 44)),
                Cardinality(Mock(), None, None),
                None,
            ),
        ],
    )

    # Wrong types
    with pytest.raises(
        Exception,
        match=re.escape(
            "A 'str' value cannot be converted to a 'Integer' instance. (filename2, Ln 10, Col 20 -> Ln 30, Col 40)"
        ),
    ):
        td.ToPythonInstance(("wrong_type", "test"))

    with pytest.raises(
        Exception,
        match=re.escape(
            "A 'int' value cannot be converted to a 'String' instance. (filename3, Ln 11, Col 22 -> Ln 33, Col 44)"
        ),
    ):
        td.ToPythonInstance((10, 20))

    # Too few elements
    with pytest.raises(
        Exception,
        match=re.escape("2 tuple items were expected (1 tuple item was found)."),
    ):
        td.ToPythonInstance((1,))

    # Too many elements
    with pytest.raises(
        Exception,
        match=re.escape(
            "A 'int' value cannot be converted to a 'String' instance. (filename3, Ln 11, Col 22 -> Ln 33, Col 44)"
        ),
    ):
        td.ToPythonInstance((1, 2, 3))
