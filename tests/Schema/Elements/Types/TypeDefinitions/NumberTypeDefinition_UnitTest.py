# ----------------------------------------------------------------------
# |
# |  NumberTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-16 10:41:59
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for NumberTypeDefinition.py"""

import re

from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.NumberTypeDefinition import *


# ----------------------------------------------------------------------
def test_DisplayType():
    assert NumberTypeDefinition(Mock())._display_type == "Number"
    assert NumberTypeDefinition(Mock(), min=0.0)._display_type == "Number {>= 0.0}"
    assert NumberTypeDefinition(Mock(), max=0.0)._display_type == "Number {<= 0.0}"
    assert NumberTypeDefinition(Mock(), min=0.0, max=10.0)._display_type == "Number {>= 0.0, <= 10.0}"


# ----------------------------------------------------------------------
def test_ErrorInvalidMinMax():
    with pytest.raises(
        ValueError,
        match=re.escape("10 > 0"),
    ):
        NumberTypeDefinition(Mock(), min=10, max=0)


# ----------------------------------------------------------------------
def test_ToPythonInstance():
    assert NumberTypeDefinition(Mock()).ToPythonInstance(10) == 10
    assert NumberTypeDefinition(Mock(), min=0).ToPythonInstance(10) == 10

    with pytest.raises(
        Exception,
        match=re.escape("'-5' is less than '0'"),
    ):
        NumberTypeDefinition(Mock(), min=0).ToPythonInstance(-5)

    assert NumberTypeDefinition(Mock(), max=10).ToPythonInstance(5) == 5

    with pytest.raises(
        Exception,
        match=re.escape("'15' is greater than '10'."),
    ):
        NumberTypeDefinition(Mock(), max=10).ToPythonInstance(15)
