# ----------------------------------------------------------------------
# |
# |  NumberExpression_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 15:17:13
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for NumberExpression.py"""

from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Expressions.NumberExpression import NumberExpression


# ----------------------------------------------------------------------
def test_NumberExpression():
    region_mock = Mock()

    e = NumberExpression(region_mock, 3.14)

    assert e.region is region_mock
    assert e.NAME == "Number"
    assert e.value == 3.14
