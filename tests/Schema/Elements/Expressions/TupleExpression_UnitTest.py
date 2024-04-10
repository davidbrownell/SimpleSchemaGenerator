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

from pathlib import Path
from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Common.Error import SimpleSchemaGeneratorException
from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.TupleExpression import TupleExpression
from SimpleSchemaGenerator.Schema.Visitors.TestHelperVisitor import TestHelperVisitor


# ----------------------------------------------------------------------
def test_Empty():
    region = Region.Create(Path("one"), 1, 2, 3, 4)

    with pytest.raises(
        SimpleSchemaGeneratorException,
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

    assert e.region__ is region_mock
    assert e.NAME == "Tuple"
    assert e.value == (value1, value2)

    visitor = TestHelperVisitor()

    e.Accept(visitor)

    assert visitor.queue == [
        e,
        ("value", [value1, value2]),
        value1,
        value2,
    ]
