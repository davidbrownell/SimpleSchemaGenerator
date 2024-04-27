# ----------------------------------------------------------------------
# |
# |  ParseTupleType_UnitTest.py
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
"""Unit tests for ParseTupleType.py."""

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
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Types.ParseIdentifierType import (
    ParseIdentifier,
    ParseIdentifierType,
)
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Types.ParseTupleType import (
    ParseTupleType,
)

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent.parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_SingleElement():
    region = Mock()
    cardinality = Cardinality(Mock(), IntegerExpression(Mock(), 0), IntegerExpression(Mock(), 1))
    metadata = Mock()
    identifier_type = ParseIdentifierType(
        Mock(),
        Cardinality(Mock(), IntegerExpression(Mock(), 1), None),
        None,
        [ParseIdentifier(Mock(), "Identifier1")],
        None,
    )

    t = ParseTupleType(region, cardinality, metadata, [identifier_type])

    assert t.region is region
    assert t.cardinality is cardinality
    assert t.unresolved_metadata is metadata
    assert t.types == [identifier_type]

    assert t.display_type == "(Identifier1+, )?"

    assert TestElementVisitor(t) == [
        t,
        ("cardinality", cardinality),
        ("unresolved_metadata", metadata),
        ("types", [identifier_type]),
    ]


# ----------------------------------------------------------------------
def test_MultipleElements():
    region = Mock()
    cardinality = Cardinality(Mock(), IntegerExpression(Mock(), 0), None)
    metadata = Mock()
    identifier_type1 = ParseIdentifierType(
        Mock(),
        Cardinality(Mock(), IntegerExpression(Mock(), 0), IntegerExpression(Mock(), 1)),
        None,
        [ParseIdentifier(Mock(), "Identifier1")],
        None,
    )

    identifier_type2 = ParseIdentifierType(
        Mock(),
        Cardinality(Mock(), IntegerExpression(Mock(), 1), None),
        None,
        [
            ParseIdentifier(Mock(), "Identifier2A"),
            ParseIdentifier(Mock(), "Identifier2B"),
        ],
        None,
    )

    t = ParseTupleType(region, cardinality, metadata, [identifier_type1, identifier_type2])

    assert t.region is region
    assert t.cardinality is cardinality
    assert t.unresolved_metadata is metadata
    assert t.types == [identifier_type1, identifier_type2]

    assert t.display_type == "(Identifier1?, Identifier2A.Identifier2B+, )*"

    assert TestElementVisitor(t) == [
        t,
        ("cardinality", cardinality),
        ("unresolved_metadata", metadata),
        ("types", [identifier_type1, identifier_type2]),
    ]


# ----------------------------------------------------------------------
def test_ErrorMissingTypes():
    with pytest.raises(
        Exception,
        match=re.escape("No tuple types were provided. (file, Ln 10, Col 20 -> Ln 30, Col 40)"),
    ):
        ParseTupleType(Region.Create(Path("file"), 10, 20, 30, 40), Mock(), None, [])
