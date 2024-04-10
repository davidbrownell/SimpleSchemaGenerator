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

from pathlib import Path
from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Common.Error import SimpleSchemaGeneratorException
from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator.Schema.Common.Cardinality import Cardinality
from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression
from SimpleSchemaGenerator.Schema.Visitors.TestHelperVisitor import TestHelperVisitor


# ----------------------------------------------------------------------
def test_Standard():
    region_mock = Mock()

    min_value = IntegerExpression(Mock(), 1)
    max_value = IntegerExpression(Mock(), 2)

    cardinality = Cardinality(region_mock, min_value, max_value)

    assert cardinality.region__ is region_mock
    assert cardinality.min is min_value
    assert cardinality.max is max_value


# ----------------------------------------------------------------------
def test_Single():
    region_mock = Mock()

    c = Cardinality(region_mock, None, None)

    assert c.min.value == 1
    assert c.min.region__ is region_mock

    assert c.max is not None
    assert c.max.value == 1
    assert c.max.region__ is region_mock

    assert c.is_single is True
    assert c.is_optional is False
    assert c.is_container is False

    assert str(c) == ""

    visitor = TestHelperVisitor()

    c.Accept(visitor)

    assert len(visitor.queue) == 5
    assert visitor.queue[0] is c
    assert visitor.queue[1][0] == "min"
    assert isinstance(visitor.queue[2], IntegerExpression)
    assert visitor.queue[3][0] == "max"
    assert isinstance(visitor.queue[4], IntegerExpression)


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

    visitor = TestHelperVisitor()

    c.Accept(visitor)

    assert visitor.queue == [
        c,
        ("min", min),
        min,
        ("max", max),
        max,
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

    visitor = TestHelperVisitor()

    c.Accept(visitor)

    assert visitor.queue == [
        c,
        ("min", min),
        min,
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

    visitor = TestHelperVisitor()

    c.Accept(visitor)

    assert visitor.queue == [
        c,
        ("min", min),
        min,
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

    visitor = TestHelperVisitor()

    c.Accept(visitor)

    assert visitor.queue == [
        c,
        ("min", min),
        min,
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

    visitor = TestHelperVisitor()

    c.Accept(visitor)

    assert visitor.queue == [
        c,
        ("min", integer),
        integer,
        ("max", integer),
        integer,
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

    visitor = TestHelperVisitor()

    c.Accept(visitor)

    assert visitor.queue == [
        c,
        ("min", min),
        min,
        ("max", max),
        max,
    ]


# ----------------------------------------------------------------------
def test_MaxOnly():
    region_mock = Mock()
    max = IntegerExpression(Mock(), 100)

    c = Cardinality(region_mock, None, max)

    assert c.min.value == 0
    assert c.min.region__ is region_mock
    assert c.max is max

    assert c.is_single is False
    assert c.is_optional is False
    assert c.is_container is True

    assert str(c) == "[0..100]"

    visitor = TestHelperVisitor()

    c.Accept(visitor)

    assert len(visitor.queue) == 5

    assert visitor.queue[0] is c
    assert visitor.queue[1][0] == "min"
    assert isinstance(visitor.queue[2], IntegerExpression)
    assert visitor.queue[3] == ("max", max)
    assert visitor.queue[4] is max


# ----------------------------------------------------------------------
def test_InvalidRange():
    max_region = Region.Create(Path("one"), 1, 2, 3, 4)

    with pytest.raises(
        SimpleSchemaGeneratorException,
        match=re.escape("Invalid cardinality (100 > 4). (one, Ln 1, Col 2 -> Ln 3, Col 4)"),
    ) as exec_info:
        Cardinality(Mock(), IntegerExpression(Mock(), 100), IntegerExpression(max_region, 4))

    assert len(exec_info.value.errors) == 1
    assert len(exec_info.value.errors[0].regions) == 1
    assert exec_info.value.errors[0].regions[0] is max_region
