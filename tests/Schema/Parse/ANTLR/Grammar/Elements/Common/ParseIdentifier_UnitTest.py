# ----------------------------------------------------------------------
# |
# |  ParseIdentifier_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-12 19:17:58
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for ParseIdentifier.py."""

import re

from pathlib import Path
from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Common.Error import SimpleSchemaGeneratorError
from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator.Schema.Elements.Common.Visibility import Visibility
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Common.ParseIdentifier import (
    ParseIdentifier,
    TerminalElement,
)


# ----------------------------------------------------------------------
def test_Standard():
    region_mock = Mock()

    e = ParseIdentifier(region_mock, "Hello")

    assert e.region is region_mock
    assert e.value == "Hello"


# ----------------------------------------------------------------------
@pytest.mark.parametrize("value", ["Name", "🤠"])
class TestVisibility:
    # ----------------------------------------------------------------------
    def test_Private(self, value):
        region = Region.Create(Path("foo"), 1, 2, 3, 4)

        result = ParseIdentifier(region, f"_{value}").visibility

        assert result.value == Visibility.Private
        assert result.region.begin == region.begin
        assert result.region.end.line == result.region.begin.line
        assert result.region.end.column == result.region.begin.column + 1

    # ----------------------------------------------------------------------
    @pytest.mark.parametrize("prefix", ["@", "$", "&"])
    def test_Protected(self, value, prefix):
        region = Region.Create(Path("foo"), 1, 2, 3, 4)

        result = ParseIdentifier(region, f"{prefix}{value}").visibility

        assert result.value == Visibility.Protected
        assert result.region.begin == region.begin
        assert result.region.end.line == result.region.begin.line
        assert result.region.end.column == result.region.begin.column + 1

    # ----------------------------------------------------------------------
    def test_Public(self, value):
        region = Region.Create(Path("foo"), 1, 2, 3, 4)

        result = ParseIdentifier(region, value).visibility

        assert result.value == Visibility.Public
        assert result.region == region


# ----------------------------------------------------------------------
def test_ExpressionOrType():
    for value, is_type in [
        ("Name", True),
        ("🤠", True),
        ("name", False),
        ("_Name", True),
        ("@Name", True),
        ("_name", False),
        ("$name", False),
    ]:
        e = ParseIdentifier(Mock(), value)

        assert e.is_type is is_type
        assert e.is_expression is not is_type


# ----------------------------------------------------------------------
def test_ToTerminalElement():
    e = ParseIdentifier(Mock(), "name")

    result = e.ToTerminalElement()

    assert isinstance(result, TerminalElement)
    assert result.value == e.value
    assert result.region == e.region


# ----------------------------------------------------------------------
def test_ErrorNoChars():
    region = Region.Create(Path("bar"), 1, 2, 3, 4)

    with pytest.raises(
        SimpleSchemaGeneratorError,
        match=re.escape("'__' does not have any identifiable characters. (bar, Ln 1, Col 2 -> Ln 3, Col 4)"),
    ) as exec_info:
        ParseIdentifier(region, "__")

    assert len(exec_info.value.errors) == 1
    assert len(exec_info.value.errors[0].regions) == 1
    assert exec_info.value.errors[0].regions[0] is region


# ----------------------------------------------------------------------
def test_ErrorNotAlpha():
    region = Region.Create(Path("bar"), 1, 2, 3, 4)

    with pytest.raises(
        SimpleSchemaGeneratorError,
        match=re.escape(
            "The first identifiable character in '<<<' must be a letter or emoji. (bar, Ln 1, Col 2 -> Ln 3, Col 4)"
        ),
    ) as exec_info:
        ParseIdentifier(region, "<<<")

    assert len(exec_info.value.errors) == 1
    assert len(exec_info.value.errors[0].regions) == 1
    assert exec_info.value.errors[0].regions[0] is region
