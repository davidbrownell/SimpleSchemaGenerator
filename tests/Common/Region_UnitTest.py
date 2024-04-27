# ----------------------------------------------------------------------
# |
# |  Region_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-09 14:11:35
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Region.py"""

from SimpleSchemaGenerator.Common.Region import *  # type: ignore[import-untyped]


# ----------------------------------------------------------------------
def test_Create():
    r = Region.Create(Path("foo"), 1, 2, 3, 4)

    assert r.filename == Path("foo")
    assert r.begin == Location(1, 2)
    assert r.end == Location(3, 4)
    assert str(r) == "foo, Ln 1, Col 2 -> Ln 3, Col 4"


# ----------------------------------------------------------------------
def test_CreateFromCode():
    r = Region.CreateFromCode()

    assert r.filename == Path(__file__)
    assert r.begin.line == 31
    assert r.end.line == 31


# ----------------------------------------------------------------------
def test_Comparison():
    assert Region.Create(Path("foo"), 1, 2, 3, 4) == Region.Create(Path("foo"), 1, 2, 3, 4)

    assert Region.Create(Path("foo"), 1, 2, 3, 4) != Region.Create(Path("bar"), 1, 2, 3, 4)
    assert Region.Create(Path("foo"), 1, 2, 3, 4) != Region.Create(Path("foo"), 1, 2, 3, 40)
    assert Region.Create(Path("foo"), 1, 2, 3, 4) != Region.Create(Path("foo"), 1, 2, 30, 4)
    assert Region.Create(Path("foo"), 1, 2, 3, 4) != Region.Create(Path("foo"), 1, 20, 3, 4)
    assert Region.Create(Path("foo"), 1, 2, 3, 4) != Region.Create(Path("foo"), 10, 2, 30, 40)

    assert Region.Create(Path("aaa"), 1, 2, 3, 4) < Region.Create(Path("zzz"), 1, 2, 3, 4)
    assert Region.Create(Path("foo"), 1, 2, 3, 4) < Region.Create(Path("foo"), 10, 20, 30, 40)

    assert Region.Create(Path("aaa"), 1, 2, 3, 4) <= Region.Create(Path("zzz"), 1, 2, 3, 4)
    assert Region.Create(Path("foo"), 1, 2, 3, 4) <= Region.Create(Path("foo"), 10, 20, 30, 40)
    assert Region.Create(Path("foo"), 1, 2, 3, 4) <= Region.Create(Path("foo"), 1, 2, 3, 4)

    assert Region.Create(Path("zzz"), 1, 2, 3, 4) > Region.Create(Path("aaa"), 1, 2, 3, 4)
    assert Region.Create(Path("foo"), 10, 20, 30, 40) > Region.Create(Path("foo"), 1, 2, 3, 4)

    assert Region.Create(Path("zzz"), 1, 2, 3, 4) >= Region.Create(Path("aaa"), 1, 2, 3, 4)
    assert Region.Create(Path("foo"), 10, 20, 30, 40) >= Region.Create(Path("foo"), 1, 2, 3, 4)
    assert Region.Create(Path("foo"), 1, 2, 3, 4) >= Region.Create(Path("foo"), 1, 2, 3, 4)


# ----------------------------------------------------------------------
def test_Contains():
    r = Region.Create(Path("foo"), 1, 2, 3, 4)

    # Location
    assert Location(1, 2) in r
    assert Location(3, 4) in r
    assert Location(4, 4) not in r

    # Region
    assert Region.Create(Path("foo"), 1, 2, 3, 4) in r
    assert Region.Create(Path("bar"), 1, 2, 3, 4) not in r
    assert Region.Create(Path("foo"), 1, 2, 4, 1) not in r
