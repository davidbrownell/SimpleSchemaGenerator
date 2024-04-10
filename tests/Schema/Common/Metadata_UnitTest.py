# ----------------------------------------------------------------------
# |
# |  Metadata_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 09:11:47
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Metadata.py"""

import re

from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Errors import SimpleSchemaGeneratorException
from SimpleSchemaGenerator.Common.Region import *
from SimpleSchemaGenerator.Schema.Common.Metadata import *
from SimpleSchemaGenerator.Schema.Visitors.TestHelperVisitor import TestHelperVisitor


# ----------------------------------------------------------------------
def test_MetadataItem():
    region_mock = Mock()
    name_mock = Mock()
    expression_mock = Mock()

    e = MetadataItem(region_mock, name_mock, expression_mock)

    assert e.region__ is region_mock
    assert e.name is name_mock
    assert e.expression is expression_mock

    # Visitor
    visitor = TestHelperVisitor()

    e.Accept(visitor)

    assert visitor.queue == [
        e,
        ("name", name_mock),
        ("expression", expression_mock),
    ]


# ----------------------------------------------------------------------
def test_Metadata():
    region_mock = Mock()

    foo_name = TerminalElement[str](Mock(), "foo")
    bar_name = TerminalElement[str](Mock(), "bar")
    baz_name = TerminalElement[str](Mock(), "baz")

    foo_expression = Mock()
    bar_expression = Mock()
    baz_expression = Mock()

    foo_metadata_item = MetadataItem(Mock(), foo_name, foo_expression)
    bar_metadata_item = MetadataItem(Mock(), bar_name, bar_expression)
    baz_metadata_item = MetadataItem(Mock(), baz_name, baz_expression)

    e = Metadata(
        region_mock,
        [
            foo_metadata_item,
            bar_metadata_item,
            baz_metadata_item,
        ],
    )

    assert e.region__ is region_mock
    assert len(e.items) == 3
    assert e.items["foo"].expression is foo_expression
    assert e.items["bar"].expression is bar_expression
    assert e.items["baz"].expression is baz_expression

    # Visitor
    visitor = TestHelperVisitor()

    e.Accept(visitor)

    assert visitor.queue == [
        e,
        "Push 'items'",
        foo_metadata_item,
        ("name", foo_name),
        foo_name,
        ("expression", foo_expression),
        bar_metadata_item,
        ("name", bar_name),
        bar_name,
        ("expression", bar_expression),
        baz_metadata_item,
        ("name", baz_name),
        baz_name,
        ("expression", baz_expression),
        "Pop 'items'",
    ]


# ----------------------------------------------------------------------
def test_ErrorDuplicateKey():
    first_region = Region.Create(Path("one"), 1, 2, 3, 4)
    second_region = Region.Create(Path("two"), 2, 4, 6, 8)

    with pytest.raises(
        SimpleSchemaGeneratorException,
        match=re.escape(
            "The metadata item 'foo' was already provided at one, Ln 1, Col 2 -> Ln 3, Col 4. (two, Ln 2, Col 4 -> Ln 6, Col 8)"
        ),
    ) as exc_info:
        Metadata(
            Mock(),
            [
                MetadataItem(Mock(), TerminalElement[str](first_region, "foo"), Mock()),
                MetadataItem(Mock(), TerminalElement[str](second_region, "foo"), Mock()),
            ],
        )

    assert len(exc_info.value.errors) == 1
    assert exc_info.value.errors[0].regions[0] is second_region
