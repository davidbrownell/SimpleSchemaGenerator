# ----------------------------------------------------------------------
# |
# |  Visibility_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-12 19:09:59
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Visibility.py."""

import sys

from pathlib import Path
from unittest.mock import Mock

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Schema.Elements.Common.Visibility import Visibility, VisibilityTrait

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_Standard():
    # Nothing much to test here
    assert Visibility.Public != Visibility.Protected != Visibility.Private


# ----------------------------------------------------------------------
def test_VisibilityTrait():
    region = Mock()
    visibility = Mock()

    vt = VisibilityTrait(region, visibility)

    assert vt.region is region
    assert vt.visibility is visibility

    assert TestElementVisitor(vt) == [
        vt,
        ("visibility", visibility),
    ]
