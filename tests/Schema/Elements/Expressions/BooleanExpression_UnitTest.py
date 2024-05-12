# ----------------------------------------------------------------------
# |
# |  BooleanExpression_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 15:16:28
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for BooleanExpression.py"""

from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Expressions.BooleanExpression import BooleanExpression


# ----------------------------------------------------------------------
def test_BooleanExpression():
    region_mock = Mock()

    e = BooleanExpression(region_mock, True, BooleanExpression.Flags.YesNo)

    assert e.region is region_mock
    assert e.NAME == "Boolean"
    assert e.value is True
    assert e.flags == BooleanExpression.Flags.YesNo
