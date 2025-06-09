# ----------------------------------------------------------------------
# |
# |  TupleExpression_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 15:17:33
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for TupleExpression.py"""

import re
import sys

from pathlib import Path
from unittest.mock import Mock

import pytest

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Common.Error import SimpleSchemaGeneratorError
from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.TupleExpression import TupleExpression

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_ErrorEmpty():
    region = Region.Create(Path("one"), 1, 2, 3, 4)

    with pytest.raises(
        SimpleSchemaGeneratorError,
        match=re.escape("No expressions were provided. (one, Ln 1, Col 2 -> Ln 3, Col 4)"),
    ) as exec_info:
        TupleExpression(region, tuple())

    assert len(exec_info.value.errors) == 1
    assert len(exec_info.value.errors[0].regions) == 1
    assert exec_info.value.errors[0].regions[0] is region


# ----------------------------------------------------------------------
def test_Standard():
    region_mock = Mock()

    value1 = IntegerExpression(Mock(), 1)
    value2 = IntegerExpression(Mock(), 2)

    e = TupleExpression(region_mock, (value1, value2))

    assert e.region is region_mock
    assert e.NAME == "Tuple"
    assert e.value == (value1, value2)

    assert TestElementVisitor(e) == [
        e,
        ("value", [value1, value2]),
    ]
