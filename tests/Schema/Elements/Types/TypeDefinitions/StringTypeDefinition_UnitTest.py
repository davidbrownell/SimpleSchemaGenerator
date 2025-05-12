# ----------------------------------------------------------------------
# |
# |  StringTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-16 10:45:16
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for StringTypeDefinition.py"""

import re

from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.StringTypeDefinition import *


# ----------------------------------------------------------------------
def test_DisplayType():
    assert StringTypeDefinition(Mock()).display_type == "String"
    assert StringTypeDefinition(Mock(), 3).display_type == "String {>= 3 characters}"
    assert StringTypeDefinition(Mock(), max_length=4).display_type == "String {<= 4 characters}"
    assert StringTypeDefinition(Mock(), 10, 20).display_type == "String {>= 10 characters, <= 20 characters}"
    assert StringTypeDefinition(Mock(), validation_expression="abc").display_type == "String {matches 'abc'}"


# ----------------------------------------------------------------------
def test_Construct():
    td = StringTypeDefinition(Mock(), 10, 20, "abc")

    assert td.min_length == 10
    assert td.max_length == 20
    assert td.validation_expression == "abc"


# ----------------------------------------------------------------------
def test_ConstructErrors():
    with pytest.raises(
        ValueError,
        match=re.escape("-2 < 1"),
    ):
        StringTypeDefinition(Mock(), -2)

    with pytest.raises(
        ValueError,
        match=re.escape("1 > 0"),
    ):
        StringTypeDefinition(Mock(), max_length=0)


# ----------------------------------------------------------------------
def test_ToPythonInstance():
    td = StringTypeDefinition(Mock(), 2, 5, "[ab]*")

    assert td.ToPythonInstance("aa") == "aa"
    assert td.ToPythonInstance("aaa") == "aaa"
    assert td.ToPythonInstance("aaaaa") == "aaaaa"
    assert td.ToPythonInstance("abab") == "abab"


# ----------------------------------------------------------------------
def test_ToPythonInstanceTooShort():
    with pytest.raises(
        Exception,
        match=re.escape("At least 50 characters were expected (4 characters were found)."),
    ):
        StringTypeDefinition(Mock(), 50).ToPythonInstance("test")


# ----------------------------------------------------------------------
def test_ToPythonInstanceTooLong():
    with pytest.raises(
        Exception,
        match=re.escape("No more than 4 characters were expected (8 characters were found)."),
    ):
        StringTypeDefinition(Mock(), max_length=4).ToPythonInstance("testtest")


# ----------------------------------------------------------------------
def test_ToPythonInstanceExpressionError():
    with pytest.raises(
        Exception,
        match=re.escape("The value 'this does not match' does not match the regular expression 'test'."),
    ):
        StringTypeDefinition(Mock(), validation_expression="test").ToPythonInstance("this does not match")
