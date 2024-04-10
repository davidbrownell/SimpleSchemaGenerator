# ----------------------------------------------------------------------
# |
# |  ListExpression_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 15:16:47
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for ListExpression.py"""

from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.ListExpression import ListExpression
from SimpleSchemaGenerator.Schema.Visitors.TestHelperVisitor import TestHelperVisitor


# ----------------------------------------------------------------------
def test_ListExpressionEmpty():
    region_mock = Mock()

    e = ListExpression(region_mock, [])

    assert e.region__ is region_mock
    assert e.NAME == "List"
    assert e.value == []

    visitor = TestHelperVisitor()

    e.Accept(visitor)

    assert visitor.queue == [e, ("value", [])]


# ----------------------------------------------------------------------
def test_ListExpressionValues():
    region_mock = Mock()

    value1 = IntegerExpression(Mock(), 1)
    value2 = IntegerExpression(Mock(), 2)

    e = ListExpression(region_mock, [value1, value2])

    assert e.region__ is region_mock
    assert e.NAME == "List"
    assert e.value == [value1, value2]

    visitor = TestHelperVisitor()

    e.Accept(visitor)

    assert visitor.queue == [
        e,
        ("value", [value1, value2]),
        value1,
        value2,
    ]
