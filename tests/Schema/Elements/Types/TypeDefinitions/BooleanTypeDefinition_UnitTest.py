# ----------------------------------------------------------------------
# |
# |  BooleanTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-14 13:57:34
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for BooleanTypeDefintion.py."""

from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.BooleanTypeDefinition import *
from SimpleSchemaGenerator.Schema.Elements.Expressions.BooleanExpression import BooleanExpression


# ----------------------------------------------------------------------
def test_DisplayType():
    assert BooleanTypeDefinition(Mock()).display_type == "Boolean"


# ----------------------------------------------------------------------
def test_PythonValue():
    assert BooleanTypeDefinition(Mock()).ToPythonInstance(True) is True
    assert BooleanTypeDefinition(Mock()).ToPythonInstance(False) is False


# ----------------------------------------------------------------------
def test_Expression():
    assert (
        BooleanTypeDefinition(Mock()).ToPythonInstance(
            BooleanExpression(Mock(), True, BooleanExpression.Flags.TrueFalse)
        )
        is True
    )

    assert (
        BooleanTypeDefinition(Mock()).ToPythonInstance(
            BooleanExpression(Mock(), False, BooleanExpression.Flags.TrueFalse)
        )
        is False
    )
