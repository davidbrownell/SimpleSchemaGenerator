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

import sys

from pathlib import Path
from unittest.mock import Mock

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.ListExpression import ListExpression

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_ListExpressionEmpty():
    region_mock = Mock()

    e = ListExpression(region_mock, [])

    assert e.region is region_mock
    assert e.NAME == "List"
    assert e.value == []

    assert TestElementVisitor(e) == [
        e,
        ("value", []),
    ]


# ----------------------------------------------------------------------
def test_ListExpressionValues():
    region_mock = Mock()

    value1 = IntegerExpression(Mock(), 1)
    value2 = IntegerExpression(Mock(), 2)

    e = ListExpression(region_mock, [value1, value2])

    assert e.region is region_mock
    assert e.NAME == "List"
    assert e.value == [value1, value2]

    assert TestElementVisitor(e) == [
        e,
        ("value", [value1, value2]),
    ]
