# ----------------------------------------------------------------------
# |
# |  NoneExpression_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 15:17:01
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for NoneExpression.py"""

from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Expressions.NoneExpression import NoneExpression


# ----------------------------------------------------------------------
def test_NoneExpression():
    region_mock = Mock()

    e = NoneExpression(region_mock)

    assert e.region is region_mock
    assert e.NAME == "None"
    assert e.value is None
