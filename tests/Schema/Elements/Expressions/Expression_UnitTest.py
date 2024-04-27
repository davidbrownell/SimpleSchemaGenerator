# ----------------------------------------------------------------------
# |
# |  Expression_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 08:48:20
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Expression.py"""

from dataclasses import dataclass
from typing import ClassVar
from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Schema.Elements.Expressions.Expression import Expression


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class MyExpression(Expression):
    NAME: ClassVar[str] = "MyExpression"

    value: str


# ----------------------------------------------------------------------
def test_MyExpression():
    region_mock = Mock()

    e = MyExpression(region_mock, "foo")

    assert e.region is region_mock
    assert e.NAME == "MyExpression"
    assert e.value == "foo"


# ----------------------------------------------------------------------
def test_InvalidExpression():
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class InvalidExpression(Expression):
        pass

    # ----------------------------------------------------------------------

    with pytest.raises(Exception, match="NAME must be defined for 'InvalidExpression'."):
        InvalidExpression(Mock(), 10)
