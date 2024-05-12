# ----------------------------------------------------------------------
# |
# |  StringExpression_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 15:17:25
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for StringExpression.py"""

from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Expressions.StringExpression import StringExpression


# ----------------------------------------------------------------------
def test_StringExpression():
    region_mock = Mock()

    e = StringExpression(region_mock, "Hello", StringExpression.QuoteType.Single)

    assert e.region is region_mock
    assert e.NAME == "String"
    assert e.value == "Hello"
    assert e.quote_type == StringExpression.QuoteType.Single
