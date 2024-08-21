# ----------------------------------------------------------------------
# |
# |  IntegerTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-16 10:12:20
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for IntegerTypeDefinition.py"""

import re

from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.IntegerTypeDefinition import *


# ----------------------------------------------------------------------
def test_DisplayType():
    assert IntegerTypeDefinition(Mock())._display_type == "Integer"
    assert IntegerTypeDefinition(Mock(), min=0)._display_type == "Integer {>= 0}"
    assert IntegerTypeDefinition(Mock(), max=0)._display_type == "Integer {<= 0}"
    assert IntegerTypeDefinition(Mock(), min=0, max=10)._display_type == "Integer {>= 0, <= 10}"


# ----------------------------------------------------------------------
def test_ErrorInvalidMinMax():
    with pytest.raises(
        ValueError,
        match=re.escape("10 > 0"),
    ):
        IntegerTypeDefinition(Mock(), min=10, max=0)


# ----------------------------------------------------------------------
def test_ToPythonInstance():
    assert IntegerTypeDefinition(Mock()).ToPythonInstance(10) == 10
    assert IntegerTypeDefinition(Mock(), min=0).ToPythonInstance(10) == 10

    with pytest.raises(
        Exception,
        match=re.escape("'-5' is less than '0'"),
    ):
        IntegerTypeDefinition(Mock(), min=0).ToPythonInstance(-5)

    assert IntegerTypeDefinition(Mock(), max=10).ToPythonInstance(5) == 5

    with pytest.raises(
        Exception,
        match=re.escape("'15' is greater than '10'."),
    ):
        IntegerTypeDefinition(Mock(), max=10).ToPythonInstance(15)
