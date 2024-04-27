# ----------------------------------------------------------------------
# |
# |  ParseStructureStatement_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-13 11:30:23
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for ParseStructureStatement.py."""

import sys

from pathlib import Path
from typing import cast
from unittest.mock import Mock

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Schema.Elements.Common.TerminalElement import TerminalElement
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Statements.ParseStructureStatement import (
    ParseStructureStatement,
    Statement,
)
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Types.ParseIdentifierType import (
    ParseIdentifierType,
)

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent.parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_Standard():
    region = Mock()
    name = Mock()
    base1 = Mock()
    base2 = Mock()
    cardinality = Mock()
    metadata = Mock()
    child1 = Mock()
    child2 = Mock()
    child3 = Mock()

    s = ParseStructureStatement(
        region,
        name,
        [base1, base2],
        cardinality,
        metadata,
        [child1, child2, child3],
    )

    assert s.region is region
    assert s.name is name
    assert s.bases == [base1, base2]
    assert s.cardinality is cardinality
    assert s.unresolved_metadata is metadata
    assert s.children == [child1, child2, child3]


# ----------------------------------------------------------------------
def test_VisitorNoOptional():
    child1 = TerminalElement[str](Mock(), "child1")
    child2 = TerminalElement[str](Mock(), "child2")

    s = ParseStructureStatement(
        Mock(),
        Mock(),
        None,
        Mock(),
        None,
        cast(list[Statement], [child1, child2]),
    )

    results = TestElementVisitor(s)

    assert len(results) == 4
    assert results[0] is s
    assert results[1][0] == "name"
    assert results[2][0] == "cardinality"
    assert results[3] == ("<children>: children", [child1, child2])


# ----------------------------------------------------------------------
def test_VisitorAllOptional():
    base1 = TerminalElement[str](Mock(), "base1")
    base2 = TerminalElement[str](Mock(), "base2")

    child1 = TerminalElement[str](Mock(), "child1")
    child2 = TerminalElement[str](Mock(), "child2")

    s = ParseStructureStatement(
        Mock(),
        Mock(),
        cast(list[ParseIdentifierType], [base1, base2]),
        Mock(),
        Mock(),
        cast(list[Statement], [child1, child2]),
    )

    results = TestElementVisitor(s)

    assert len(results) == 6
    assert results[0] is s
    assert results[1][0] == "name"
    assert results[2] == ("bases", [base1, base2])
    assert results[3][0] == "cardinality"
    assert results[4][0] == "unresolved_metadata"
    assert results[5] == ("<children>: children", [child1, child2])
