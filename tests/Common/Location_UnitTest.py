# ----------------------------------------------------------------------
# |
# |  Location_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-02-11 14:07:12
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Location.py"""

import pytest

from SimpleSchemaGenerator.Common.Location import *


# ----------------------------------------------------------------------
def test_Create():
    l = Location(1, 2)

    assert l.line == 1
    assert l.column == 2
    assert str(l) == "Ln 1, Col 2"


# ----------------------------------------------------------------------
def test_InvalidLine():
    with pytest.raises(ValueError, match="Invalid line value: 0"):
        Location(0, 2)


# ----------------------------------------------------------------------
def test_InvalidColumn():
    with pytest.raises(ValueError, match="Invalid column value: 0"):
        Location(1, 0)


# ----------------------------------------------------------------------
def test_Comparison():
    assert Location(1, 2) == Location(1, 2)
    assert (Location(1, 2) == Location(3, 4)) is False

    assert Location(1, 2) != Location(3, 4)
    assert (Location(1, 2) != Location(1, 2)) is False

    assert Location(1, 2) < Location(3, 2)
    assert Location(1, 2) < Location(1, 3)

    assert Location(1, 2) <= Location(3, 2)
    assert Location(1, 2) <= Location(1, 3)
    assert Location(1, 2) <= Location(1, 2)

    assert Location(3, 4) > Location(1, 4)
    assert Location(3, 4) > Location(3, 1)

    assert Location(3, 4) >= Location(1, 4)
    assert Location(3, 4) >= Location(3, 1)
    assert Location(1, 2) >= Location(1, 2)
