# ----------------------------------------------------------------------
# |
# |  ItemStatement_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-20 18:10:00
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for ItemStatement.py."""

import sys

from pathlib import Path
from unittest.mock import Mock

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Schema.Elements.Statements.ItemStatement import *

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_Standard():
    region = Mock()
    visibility = Mock()
    name = Mock()
    type = Mock()

    item = ItemStatement(region, visibility, name, type)

    assert item.region is region
    assert item.visibility is visibility
    assert item.name is name
    assert item.type is type

    assert TestElementVisitor(item) == [
        item,
        ("visibility", visibility),
        ("name", name),
        ("type", type),
    ]
