# ----------------------------------------------------------------------
# |
# |  VariantTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-19 13:28:27
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for VariantTypeDefinition.py."""

import re
import sys

from pathlib import Path
from unittest.mock import MagicMock as Mock

import pytest

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator.Schema.Elements.Common.Cardinality import Cardinality
from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.ListExpression import ListExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.StringExpression import StringExpression
from SimpleSchemaGenerator.Schema.Elements.Types.Type import Type
from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.VariantTypeDefinition import *
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

    td = VariantTypeDefinition(Mock(), types)

    assert td.NAME == "Variant"
    assert td.SUPPORTED_PYTHON_TYPES == (object,)
    assert td.types is types

    assert TestElementVisitor(td) == [
        td,
        ("types", types),
    ]


# ----------------------------------------------------------------------
def test_ErrorCreateWithoutEnoughTypes():
    with pytest.raises(
        Errors.SimpleSchemaGeneratorError,
        match=re.escape("At least two types must be provided. (filename, Ln 1, Col 2 -> Ln 3, Col 4)"),
    ):
        VariantTypeDefinition(Region.Create(Path("filename"), 1, 2, 3, 4), [Mock()])


# ----------------------------------------------------------------------
def test_ErrorNestedVariant():
    with pytest.raises(
        Errors.SimpleSchemaGeneratorError,
        match=re.escape(
            "Variant types may not be nested within variant types. (filename, Ln 11, Col 22 -> Ln 33, Col 44)"
        ),
    ):
        VariantTypeDefinition(
            Mock(),
            [
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
                    VariantTypeDefinition(
                        Region.Create(Path("filename"), 11, 22, 33, 44),
                        [Mock(), Mock()],
                    ),
                    Cardinality(Mock(), None, None),
                    None,
                ),
            ],
        )


# ----------------------------------------------------------------------
def test_DisplayType():
    assert (
        VariantTypeDefinition(
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
        == "(<Integer {<= 10}> | String | Integer? | String+)"
    )


# ----------------------------------------------------------------------
def test_ToPythonInstanceSingle():
    td = VariantTypeDefinition(
        Mock(),
        [
            Type.Create(
                Mock(),
                Mock(),
                IntegerTypeDefinition(Mock(), max=10),
                Cardinality(Mock(), None, None),
                None,
                region=Region.Create(Path("filename1"), 1, 2, 3, 4),
            ),
            Type.Create(
                Mock(),
                Mock(),
                StringTypeDefinition(Mock()),
                Cardinality(Mock(), None, None),
                None,
                region=Region.Create(Path("filename2"), 11, 22, 33, 44),
            ),
        ],
    )

    assert td.ToPythonInstance(5) == 5
    assert td.ToPythonInstance(IntegerExpression(Mock(), 5)) == 5

    assert td.ToPythonInstance("test") == "test"
    assert td.ToPythonInstance(StringExpression(Mock(), "test", StringExpression.QuoteType.Single)) == "test"

    with pytest.raises(
        Exception,
        match=re.escape(
            textwrap.dedent(
                """\
                A 'int' value does not correspond to any types within '(<Integer {<= 10}> | String)'.

                    Additional Information:
                        Integer {<= 10}
                            '123' is greater than '10'. (filename1, Ln 1, Col 2 -> Ln 3, Col 4)
                        String
                            A 'int' value cannot be converted to a 'String' instance. (filename2, Ln 11, Col 22 -> Ln 33, Col 44)
                """,
            ),
        ),
    ):
        td.ToPythonInstance(123)

    with pytest.raises(
        Exception,
        match=re.escape(
            textwrap.dedent(
                """\
                A 'int' value does not correspond to any types within '(<Integer {<= 10}> | String)'.

                    Additional Information:
                        Integer {<= 10}
                            '123' is greater than '10'. (filename1, Ln 1, Col 2 -> Ln 3, Col 4)
                        String
                            A 'int' value cannot be converted to a 'String' instance. (filename2, Ln 11, Col 22 -> Ln 33, Col 44)

                    - filename3, Ln 10, Col 20 -> Ln 30, Col 40
                """,
            ),
        ),
    ):
        td.ToPythonInstance(IntegerExpression(Region.Create(Path("filename3"), 10, 20, 30, 40), 123))


# ----------------------------------------------------------------------
def test_ToPythonInstanceChildCardinality():
    td = VariantTypeDefinition(
        Mock(),
        [
            Type.Create(
                Mock(),
                Mock(),
                IntegerTypeDefinition(Mock()),
                Cardinality(Mock(), IntegerExpression(Mock(), 2), None),
                None,
                region=Region.Create(Path("filename1"), 1, 2, 3, 4),
            ),
            Type.Create(
                Mock(),
                Mock(),
                StringTypeDefinition(Mock()),
                Cardinality(Mock(), None, None),
                None,
                region=Region.Create(Path("filename2"), 11, 22, 33, 44),
            ),
        ],
    )

    assert td.ToPythonInstance([1, 2]) == [1, 2]
    assert td.ToPythonInstance(
        ListExpression(
            Mock(),
            [
                IntegerExpression(Mock(), 1),
                IntegerExpression(Mock(), 2),
            ],
        ),
    ) == [1, 2]

    assert td.ToPythonInstance("test") == "test"
    assert td.ToPythonInstance(StringExpression(Mock(), "test", StringExpression.QuoteType.Single)) == "test"

    with pytest.raises(
        Exception,
        match=re.escape(
            textwrap.dedent(
                """\
                A 'int' value does not correspond to any types within '(Integer[2+] | String)'.

                    Additional Information:
                        Integer[2+]
                            A list of items was expected. (filename1, Ln 1, Col 2 -> Ln 3, Col 4)
                        String
                            A 'int' value cannot be converted to a 'String' instance. (filename2, Ln 11, Col 22 -> Ln 33, Col 44)
                """,
            ),
        ),
    ):
        td.ToPythonInstance(123)

    with pytest.raises(
        Exception,
        match=re.escape(
            textwrap.dedent(
                """\
                A 'int' value does not correspond to any types within '(Integer[2+] | String)'.

                    Additional Information:
                        Integer[2+]
                            A list of items was expected. (filename1, Ln 1, Col 2 -> Ln 3, Col 4)
                        String
                            A 'int' value cannot be converted to a 'String' instance. (filename2, Ln 11, Col 22 -> Ln 33, Col 44)

                    - filename3, Ln 10, Col 20 -> Ln 30, Col 40
                """,
            ),
        ),
    ):
        td.ToPythonInstance(IntegerExpression(Region.Create(Path("filename3"), 10, 20, 30, 40), 123))
