# ----------------------------------------------------------------------
# |
# |  ParseVariantType_UnitTest.py
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
"""Unit tests for ParseVariantType.py."""

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
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Types.ParseVariantType import (
    ParseVariantType,
)

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent.parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_Standard():
    region = Mock()
    cardinality = Cardinality(Mock(), IntegerExpression(Mock(), 3), IntegerExpression(Mock(), 5))
    metadata = Mock()
    identifier_type1 = ParseIdentifierType(
        Mock(),
        Cardinality(Mock(), IntegerExpression(Mock(), 1), None),
        None,
        [ParseIdentifier(Mock(), "Identifier1")],
        None,
    )

    identifier_type2 = ParseIdentifierType(
        Mock(),
        Cardinality(Mock(), None, None),
        None,
        [ParseIdentifier(Mock(), "Identifier2")],
        None,
    )

    v = ParseVariantType(region, cardinality, metadata, [identifier_type1, identifier_type2])

    assert v.region is region
    assert v.cardinality is cardinality
    assert v.unresolved_metadata is metadata
    assert v.types == [identifier_type1, identifier_type2]

    assert v.display_type == "(Identifier1+ | Identifier2)[3..5]"

    assert TestElementVisitor(v) == [
        v,
        ("cardinality", cardinality),
        ("unresolved_metadata", metadata),
        ("types", [identifier_type1, identifier_type2]),
    ]


# ----------------------------------------------------------------------
def test_ErrorSingleType():
    with pytest.raises(
        Exception,
        match=re.escape("Not enough types were provided. (file, Ln 1, Col 3 -> Ln 5, Col 7)"),
    ):
        ParseVariantType(
            Region.Create(Path("file"), 1, 3, 5, 7),
            Mock(),
            None,
            [Mock()],
        )


# ----------------------------------------------------------------------
def test_ErrorNestedVariant():
    with pytest.raises(
        Exception,
        match=re.escape("Nested variant types are not supported. (abc, Ln 11, Col 22 -> Ln 33, Col 44)"),
    ):
        ParseVariantType(
            Mock(),
            Mock(),
            None,
            [
                Mock(),
                ParseVariantType(
                    Region.Create(Path("abc"), 11, 22, 33, 44),
                    Mock(),
                    None,
                    [Mock(), Mock()],
                ),
            ],
        )
