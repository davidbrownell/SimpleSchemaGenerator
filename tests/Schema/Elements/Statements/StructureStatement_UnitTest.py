# ----------------------------------------------------------------------
# |
# |  StructureStatement_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-20 18:10:29
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for StructureStatement.py."""

import sys

from pathlib import Path
from unittest.mock import Mock

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Schema.Elements.Statements.StructureStatement import *

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_Standard():
    region = Mock()
    name = Mock()
    base1 = Mock()
    base2 = Mock()
    child1 = TerminalElement[str](Mock(), "child1")
    child2 = TerminalElement[str](Mock(), "child2")

    s = StructureStatement(region, name, [base1, base2], [child1, child2])

    assert s.region is region
    assert s.name is name
    assert s.base_types == [base1, base2]
    assert s.children == [child1, child2]

    assert TestElementVisitor(s) == [
        s,
        ("name", name),
        ("base_types", [base1, base2]),
        ("<children>: children", [child1, child2]),
    ]
