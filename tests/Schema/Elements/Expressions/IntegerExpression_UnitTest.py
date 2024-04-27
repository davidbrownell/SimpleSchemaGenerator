# ----------------------------------------------------------------------
# |
# |  IntegerExpression_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 08:52:06
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for IntegerExpression.py"""

from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression


# ----------------------------------------------------------------------
def test_IntegerExpression():
    region_mock = Mock()

    e = IntegerExpression(region_mock, 10)

    assert e.region is region_mock
    assert e.NAME == "Integer"
    assert e.value == 10
