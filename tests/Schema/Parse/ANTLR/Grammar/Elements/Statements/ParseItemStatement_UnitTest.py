# ----------------------------------------------------------------------
# |
# |  ParseItemStatement_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-13 11:27:44
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for ParseItemStatement.py."""

import sys

from pathlib import Path
from unittest.mock import Mock

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Statements.ParseItemStatement import (
    ParseItemStatement,
)

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent.parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_Standard():
    region = Mock()
    name = Mock()
    type = Mock()

    s = ParseItemStatement(region, name, type)

    assert s.region is region
    assert s.name is name
    assert s.type is type

    assert TestElementVisitor(s) == [
        s,
        ("name", name),
        ("type", type),
    ]
