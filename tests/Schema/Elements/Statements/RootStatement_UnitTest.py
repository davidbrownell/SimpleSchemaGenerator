# ----------------------------------------------------------------------
# |
# |  RootStatement_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-20 17:54:36
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for RootStatement.py."""

import re
import sys

from pathlib import Path
from unittest.mock import Mock

import pytest

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator.Schema.Elements.Common.TerminalElement import TerminalElement
from SimpleSchemaGenerator.Schema.Elements.Statements.RootStatement import *

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_Standard():
    region = Mock()
    statement1 = TerminalElement[str](Mock(), "one")
    statement2 = TerminalElement[str](Mock(), "two")

    root = RootStatement(region, [statement1, statement2])

    assert root.region is region
    assert root.statements == [statement1, statement2]

    assert TestElementVisitor(root) == [
        root,
        ("<children>: statements", [statement1, statement2]),
    ]


# ----------------------------------------------------------------------
def test_ErrorNestedRoot():
    with pytest.raises(
        Exception,
        match=re.escape("Root statements cannot be nested. (foo, Ln 1, Col 2 -> Ln 3, Col 4)"),
    ):
        RootStatement(Mock(), [Mock(), RootStatement(Region.Create(Path("foo"), 1, 2, 3, 4), [])])
