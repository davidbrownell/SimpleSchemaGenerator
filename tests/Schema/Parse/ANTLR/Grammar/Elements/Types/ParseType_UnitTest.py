# ----------------------------------------------------------------------
# |
# |  ParseType_UnitTest.py
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
"""Unit tests for ParseType.py."""

import sys

from dataclasses import dataclass
from pathlib import Path
from unittest.mock import Mock

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Schema.Parse.ANTLR.Grammar.Elements.Types.ParseType import (
    ParseType,
)

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent.parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class MyParseType(ParseType):
    @property
    def _display_type(self) -> str:
        return "MyParseType"


# ----------------------------------------------------------------------
def test_Standard():
    region = Mock()
    cardinality = Mock()
    metadata = Mock()

    t = MyParseType(region, cardinality, metadata)

    assert t.region is region
    assert t.cardinality is cardinality
    assert t.unresolved_metadata is metadata

    assert TestElementVisitor(t) == [
        t,
        ("cardinality", cardinality),
        ("unresolved_metadata", metadata),
    ]
