# ----------------------------------------------------------------------
# |
# |  Range_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-09 14:10:29
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Range.py"""

import pytest

from SimpleSchemaGenerator.Common.Range import *


# ----------------------------------------------------------------------
def test_Create():
    r = Range(Location(1, 2), Location(3, 4))

    assert r.begin == Location(1, 2)
    assert r.end == Location(3, 4)
    assert str(r) == "Ln 1, Col 2 -> Ln 3, Col 4"


# ----------------------------------------------------------------------
def test_InvalidRange():
    with pytest.raises(ValueError, match="Invalid end"):
        Range(Location(3, 4), Location(1, 2))


# ----------------------------------------------------------------------
def test_Comparison():
    assert Range(Location(1, 2), Location(3, 4)) == Range(Location(1, 2), Location(3, 4))
    assert (Range(Location(1, 2), Location(3, 4)) == Range(Location(3, 4), Location(3, 5))) is False

    assert Range(Location(1, 2), Location(3, 4)) != Range(Location(3, 4), Location(3, 5))
    assert (Range(Location(1, 2), Location(3, 4)) != Range(Location(1, 2), Location(3, 4))) is False

    assert Range(Location(1, 2), Location(1, 10)) < Range(Location(2, 2), Location(2, 10))
    assert Range(Location(1, 2), Location(1, 10)) < Range(Location(1, 2), Location(1, 20))
    assert Range(Location(1, 2), Location(1, 10)) < Range(Location(1, 5), Location(1, 10))

    assert Range(Location(1, 2), Location(1, 10)) <= Range(Location(2, 2), Location(2, 10))
    assert Range(Location(1, 2), Location(1, 10)) <= Range(Location(1, 2), Location(1, 20))
    assert Range(Location(1, 2), Location(1, 10)) <= Range(Location(1, 5), Location(1, 10))
    assert Range(Location(1, 2), Location(3, 4)) <= Range(Location(1, 2), Location(3, 4))

    assert Range(Location(2, 2), Location(2, 10)) > Range(Location(1, 2), Location(1, 10))
    assert Range(Location(1, 2), Location(1, 20)) > Range(Location(1, 2), Location(1, 10))
    assert Range(Location(1, 5), Location(1, 10)) > Range(Location(1, 2), Location(1, 10))

    assert Range(Location(2, 2), Location(2, 10)) >= Range(Location(1, 2), Location(1, 10))
    assert Range(Location(1, 2), Location(1, 20)) >= Range(Location(1, 2), Location(1, 10))
    assert Range(Location(1, 5), Location(1, 10)) >= Range(Location(1, 2), Location(1, 10))
    assert Range(Location(1, 2), Location(3, 4)) >= Range(Location(1, 2), Location(3, 4))


# ----------------------------------------------------------------------
def test_Contains():
    r = Range(Location(1, 2), Location(3, 4))

    # Location
    assert Location(1, 5) in r
    assert Location(2, 1) in r
    assert Location(10, 20) not in r

    # Range
    assert Range(Location(1, 2), Location(3, 4)) in r
    assert Range(Location(1, 2), Location(1, 10)) in r
    assert Range(Location(2, 1), Location(3, 4)) in r
    assert Range(Location(3, 1), Location(3, 10)) not in r
