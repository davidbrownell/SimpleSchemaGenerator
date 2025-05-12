# ----------------------------------------------------------------------
# |
# |  ParseIdentifierType_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-12 19:56:28
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for ParseIdentifierType.py."""

import re
import sys

from pathlib import Path
from unittest.mock import Mock

import pytest

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator.Schema.Elements.Common.Cardinality import Cardinality
from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Common.ParseIdentifier import (
    ParseIdentifier,
)
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Types.ParseIdentifierType import (
    ParseIdentifierType,
)

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent.parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_SingleIdentifier():
    region = Mock()
    cardinality = Cardinality(Mock(), IntegerExpression(Mock(), 0), IntegerExpression(Mock(), 1))
    metadata = Mock()
    identifier1 = ParseIdentifier(Mock(), "Identifier1")
    is_global_reference = Mock()

    t = ParseIdentifierType(region, cardinality, metadata, [identifier1], is_global_reference)

    assert t.region is region
    assert t.cardinality is cardinality
    assert t.unresolved_metadata is metadata
    assert t.identifiers == [identifier1]
    assert t.is_global_reference is is_global_reference

    assert t.display_type == "::Identifier1?"

    assert TestElementVisitor(t) == [
        t,
        ("cardinality", cardinality),
        ("unresolved_metadata", metadata),
        ("identifiers", [identifier1]),
    ]


# ----------------------------------------------------------------------
def test_MultipleIdentifiers():
    region = Mock()
    cardinality = Cardinality(Mock(), IntegerExpression(Mock(), 0), None)
    metadata = Mock()
    identifier1 = ParseIdentifier(Mock(), "Identifier1")
    identifier2 = ParseIdentifier(Mock(), "Identifier2")
    is_global_reference = None

    t = ParseIdentifierType(region, cardinality, metadata, [identifier1, identifier2], is_global_reference)

    assert t.region is region
    assert t.cardinality is cardinality
    assert t.unresolved_metadata is metadata
    assert t.identifiers == [identifier1, identifier2]
    assert t.is_global_reference is is_global_reference

    assert t.display_type == "Identifier1.Identifier2*"

    assert TestElementVisitor(t) == [
        t,
        ("cardinality", cardinality),
        ("unresolved_metadata", metadata),
        ("identifiers", [identifier1, identifier2]),
    ]


# ----------------------------------------------------------------------
def test_ErrorNoIdentifiers():
    with pytest.raises(
        Exception,
        match=re.escape(
            "Identifier types must have at least one identifier. (foo, Ln 1, Col 2 -> Ln 3, Col 4)"
        ),
    ):
        ParseIdentifierType(Region.Create(Path("foo"), 1, 2, 3, 4), Mock(), None, [], None)


# ----------------------------------------------------------------------
def test_ErrorIdentifierNotAType():
    with pytest.raises(
        Exception,
        match=re.escape("'not_a_type' is not a valid type name. (foo, Ln 2, Col 4 -> Ln 6, Col 8)"),
    ):
        ParseIdentifierType(
            Mock(),
            Mock(),
            None,
            [ParseIdentifier(Region.Create(Path("foo"), 2, 4, 6, 8), "not_a_type")],
            None,
        )
