# ----------------------------------------------------------------------
# |
# |  Cardinality_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 09:05:03
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Cardinality.py"""

import re
import sys

from pathlib import Path
from unittest.mock import Mock

import pytest

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Common.Error import SimpleSchemaGeneratorError
from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator.Errors import SimpleSchemaGeneratorError
from SimpleSchemaGenerator.Schema.Elements.Common.Cardinality import Cardinality
from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.ListExpression import ListExpression

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_Standard():
    region_mock = Mock()

    min_value = IntegerExpression(Mock(), 1)
    max_value = IntegerExpression(Mock(), 2)

    cardinality = Cardinality(region_mock, min_value, max_value)

    assert cardinality.region is region_mock
    assert cardinality.min is min_value
    assert cardinality.max is max_value


# ----------------------------------------------------------------------
def test_Single():
    region_mock = Mock()

    c = Cardinality(region_mock, None, None)

    assert c.min.value == 1
    assert c.min.region is region_mock

    assert c.max is not None
    assert c.max.value == 1
    assert c.max.region is region_mock

    assert c.is_single is True
    assert c.is_optional is False
    assert c.is_container is False

    assert str(c) == ""

    results = TestElementVisitor(c)

    assert len(results) == 3
    assert results[0] is c
    assert results[1][0] == "min"
    assert isinstance(results[1][1], IntegerExpression)
    assert results[2][0] == "max"
    assert isinstance(results[2][1], IntegerExpression)


# ----------------------------------------------------------------------
def test_Optional():
    min = IntegerExpression(Mock(), 0)
    max = IntegerExpression(Mock(), 1)

    c = Cardinality(Mock(), min, max)

    assert c.min is min
    assert c.max is max

    assert c.is_single is False
    assert c.is_optional is True
    assert c.is_container is False

    assert str(c) == "?"

    assert TestElementVisitor(c) == [
        c,
        ("min", min),
        ("max", max),
    ]


# ----------------------------------------------------------------------
def test_OptionalContainer():
    min = IntegerExpression(Mock(), 0)

    c = Cardinality(Mock(), min, None)

    assert c.min is min
    assert c.max is None

    assert c.is_single is False
    assert c.is_optional is False
    assert c.is_container is True

    assert str(c) == "*"

    assert TestElementVisitor(c) == [
        c,
        ("min", min),
    ]


# ----------------------------------------------------------------------
def test_RequiredUnboundedContainer():
    min = IntegerExpression(Mock(), 1)

    c = Cardinality(Mock(), min, None)

    assert c.min is min
    assert c.max is None

    assert c.is_single is False
    assert c.is_optional is False
    assert c.is_container is True

    assert str(c) == "+"

    assert TestElementVisitor(c) == [
        c,
        ("min", min),
    ]


# ----------------------------------------------------------------------
def test_RequiredBoundedContainer():
    min = IntegerExpression(Mock(), 13)

    c = Cardinality(Mock(), min, None)

    assert c.min is min
    assert c.max is None

    assert c.is_single is False
    assert c.is_optional is False
    assert c.is_container is True

    assert str(c) == "[13+]"

    assert TestElementVisitor(c) == [
        c,
        ("min", min),
    ]


# ----------------------------------------------------------------------
def test_FixedContainer():
    integer = IntegerExpression(Mock(), 13)

    c = Cardinality(Mock(), integer, integer)

    assert c.min is integer
    assert c.max is integer

    assert c.is_single is False
    assert c.is_optional is False
    assert c.is_container is True

    assert str(c) == "[13]"

    assert TestElementVisitor(c) == [
        c,
        ("min", integer),
        ("max", integer),
    ]


# ----------------------------------------------------------------------
def test_VariableContainer():
    min = IntegerExpression(Mock(), 13)
    max = IntegerExpression(Mock(), 42)

    c = Cardinality(Mock(), min, max)

    assert c.min is min
    assert c.max is max

    assert c.is_single is False
    assert c.is_optional is False
    assert c.is_container is True

    assert str(c) == "[13..42]"

    assert TestElementVisitor(c) == [
        c,
        ("min", min),
        ("max", max),
    ]


# ----------------------------------------------------------------------
def test_MaxOnly():
    region_mock = Mock()
    max = IntegerExpression(Mock(), 100)

    c = Cardinality(region_mock, None, max)

    assert c.min.value == 0
    assert c.min.region is region_mock
    assert c.max is max

    assert c.is_single is False
    assert c.is_optional is False
    assert c.is_container is True

    assert str(c) == "[0..100]"

    results = TestElementVisitor(c)

    assert len(results) == 3
    assert results[0] is c
    assert results[1][0] == "min"
    assert isinstance(results[1][1], IntegerExpression)
    assert results[2] == ("max", max)


# ----------------------------------------------------------------------
def test_InvalidRange():
    max_region = Region.Create(Path("one"), 1, 2, 3, 4)

    with pytest.raises(
        SimpleSchemaGeneratorError,
        match=re.escape("Invalid cardinality (100 > 4). (one, Ln 1, Col 2 -> Ln 3, Col 4)"),
    ) as exec_info:
        Cardinality(Mock(), IntegerExpression(Mock(), 100), IntegerExpression(max_region, 4))

    assert len(exec_info.value.errors) == 1
    assert len(exec_info.value.errors[0].regions) == 1
    assert exec_info.value.errors[0].regions[0] is max_region


# ----------------------------------------------------------------------
class TestValidate:
    # ----------------------------------------------------------------------
    def test_Single(self):
        c = Cardinality(Mock(), None, None)
        c.Validate("value")

        with pytest.raises(
            Exception,
            match=re.escape("None was not expected."),
        ):
            c.Validate(None)

        with pytest.raises(
            Exception,
            match=re.escape("A list of items was not expected."),
        ):
            c.Validate([1, 2, 3])

    # ----------------------------------------------------------------------
    def test_Optional(self):
        c = Cardinality(Mock(), IntegerExpression(Mock(), 0), IntegerExpression(Mock(), 1))

        c.Validate(None)
        c.Validate(1)

    # ----------------------------------------------------------------------
    def test_List(self):
        c = Cardinality(Mock(), IntegerExpression(Mock(), 2), IntegerExpression(Mock(), 3))

        c.Validate([1, 2])
        c.Validate([1, 2, 3])

        with pytest.raises(
            Exception,
            match=re.escape("A list of items was expected."),
        ):
            c.Validate(1)

        with pytest.raises(
            Exception,
            match=re.escape("At least 2 items were expected (1 item was found)."),
        ):
            c.Validate([1])

        with pytest.raises(
            Exception,
            match=re.escape("No more than 3 items were expected (4 items were found)."),
        ):
            c.Validate([1, 2, 3, 4])

    # ----------------------------------------------------------------------
    def test_Expression(self):
        c = Cardinality(
            Mock(),
            IntegerExpression(Mock(), 2),
            IntegerExpression(Mock(), 3),
        )

        c.Validate(ListExpression(Mock(), [IntegerExpression(Mock(), 1), IntegerExpression(Mock(), 2)]))

        with pytest.raises(
            SimpleSchemaGeneratorError,
            match=re.escape(
                "At least 2 items were expected (1 item was found). (filename2, Ln 1, Col 2 -> Ln 3, Col 4)"
            ),
        ):
            c.Validate(
                ListExpression(Region.Create(Path("filename2"), 1, 2, 3, 4), [IntegerExpression(Mock(), 1)])
            )
