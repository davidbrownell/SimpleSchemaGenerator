# ----------------------------------------------------------------------
# |
# |  ParseIncludeStatement_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-25 19:15:39
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for ParseIncludeStatement.py."""

import re
import sys

from pathlib import Path
from unittest.mock import Mock

import pytest

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator.Schema.Elements.Common.TerminalElement import TerminalElement
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Common.ParseIdentifier import (
    ParseIdentifier,
)
from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Statements.ParseIncludeStatement import (
    ParseIncludeStatement,
    ParseIncludeStatementItem,
    ParseIncludeStatementType,
)

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent.parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_ParseIncludeStatementItem():
    region = Mock()
    element_name = Mock()
    reference_name = Mock()

    s = ParseIncludeStatementItem(region, element_name, reference_name)

    assert s.region is region
    assert s.element_name is element_name
    assert s.reference_name is reference_name

    assert TestElementVisitor(s) == [
        s,
        ("element_name", element_name),
        ("reference_name", reference_name),
    ]


# ----------------------------------------------------------------------
def test_ErrorInvalidElementName():
    with pytest.raises(
        Exception,
        match=re.escape("The imported element 'not_a_type' is not a type. (foo, Ln 1, Col 2 -> Ln 3, Col 4)"),
    ):
        ParseIncludeStatementItem(
            Mock(),
            ParseIdentifier(Region.Create(Path("foo"), 1, 2, 3, 4), "not_a_type"),
            Mock(),
        )


# ----------------------------------------------------------------------
def test_ErrorInvalidReferenceName():
    with pytest.raises(
        Exception,
        match=re.escape("'not_a_type' is not a type name. (foo, Ln 1, Col 2 -> Ln 3, Col 4)"),
    ):
        ParseIncludeStatementItem(
            Mock(),
            Mock(),
            ParseIdentifier(Region.Create(Path("foo"), 1, 2, 3, 4), "not_a_type"),
        )


# ----------------------------------------------------------------------
def test_ParseIncludeStatement():
    region = Mock()
    include_type = ParseIncludeStatementType.Package
    filename = Mock()
    item1 = Mock()
    item2 = Mock()

    s = ParseIncludeStatement(region, include_type, filename, [item1, item2])

    assert s.region is region
    assert s.include_type is include_type
    assert s.filename is filename
    assert s.items == [item1, item2]

    assert TestElementVisitor(s) == [
        s,
        ("filename", filename),
        ("items", [item1, item2]),
    ]


# ----------------------------------------------------------------------
def test_ErrorInvalidFile():
    with pytest.raises(
        Exception,
        match=re.escape("'__does not exist__' is not a valid file. (file, Ln 2, Col 4 -> Ln 6, Col 8)"),
    ):
        ParseIncludeStatement(
            Mock(),
            Mock(),
            TerminalElement[Path](Region.Create(Path("file"), 2, 4, 6, 8), Path("__does not exist__")),
            [],
        )


# ----------------------------------------------------------------------
@pytest.mark.parametrize("include_type", [ParseIncludeStatementType.Module, ParseIncludeStatementType.Star])
def test_ErrorNoItemsExpected(include_type):
    with pytest.raises(
        Exception,
        match=re.escape("No items were expected. (foo, Ln 1, Col 2 -> Ln 3, Col 4)"),
    ):
        ParseIncludeStatement(
            Region.Create(Path("foo"), 1, 2, 3, 4),
            include_type,
            Mock(),
            [Mock(), Mock()],
        )


# ----------------------------------------------------------------------
def test_ErrorItemsExpected():
    with pytest.raises(
        Exception,
        match=re.escape("Items were expected. (bar, Ln 10, Col 20 -> Ln 30, Col 40)"),
    ):
        ParseIncludeStatement(
            Region.Create(Path("bar"), 10, 20, 30, 40),
            ParseIncludeStatementType.Package,
            Mock(),
            [],
        )
