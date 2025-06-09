# ----------------------------------------------------------------------
# |
# |  Error_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-09 14:13:42
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Errors.py"""

import textwrap

from enum import auto, Enum

from SimpleSchemaGenerator.Common.Error import *  # type: ignore[import-untyped]


# ----------------------------------------------------------------------
class TestError:
    # ----------------------------------------------------------------------
    def test_SingleLineSingleRegion(self):
        region = Region(
            Path("foo"),
            Location(1, 2),
            Location(3, 4),
        )

        e = Error("Single line, single region", region)

        assert e.message == "Single line, single region"
        assert e.regions == [region]
        assert str(e) == "Single line, single region (foo, Ln 1, Col 2 -> Ln 3, Col 4)"

    # ----------------------------------------------------------------------
    def test_MultipleLinesSingleRegion(self):
        region = Region(
            Path("foo"),
            Location(1, 2),
            Location(3, 4),
        )

        e = Error("Multiple lines\nsingle region\n", region)

        assert e.message == "Multiple lines\nsingle region\n"
        assert e.regions == [region]
        assert str(e) == textwrap.dedent(
            """\
            Multiple lines
            single region

                - foo, Ln 1, Col 2 -> Ln 3, Col 4
            """,
        )

    # ----------------------------------------------------------------------
    def test_SingleLineMultipleRegions(self):
        region1 = Region(
            Path("foo"),
            Location(1, 2),
            Location(3, 4),
        )

        region2 = Region(
            Path("bar"),
            Location(5, 6),
            Location(7, 8),
        )

        e = Error("Single line, multiple regions", [region1, region2])

        assert e.message == "Single line, multiple regions"
        assert e.regions == [region1, region2]
        assert str(e) == textwrap.dedent(
            """\
            Single line, multiple regions

                - foo, Ln 1, Col 2 -> Ln 3, Col 4
                - bar, Ln 5, Col 6 -> Ln 7, Col 8
            """,
        )

    # ----------------------------------------------------------------------
    def test_MutlipleLinesMultipleRegions(self):
        region1 = Region(
            Path("foo"),
            Location(1, 2),
            Location(3, 4),
        )

        region2 = Region(
            Path("bar"),
            Location(5, 6),
            Location(7, 8),
        )

        e = Error("Multiple lines\nmultiple regions", [region1, region2])

        assert e.message == "Multiple lines\nmultiple regions"
        assert e.regions == [region1, region2]
        assert str(e) == textwrap.dedent(
            """\
            Multiple lines
            multiple regions

                - foo, Ln 1, Col 2 -> Ln 3, Col 4
                - bar, Ln 5, Col 6 -> Ln 7, Col 8
            """,
        )


# ----------------------------------------------------------------------
def test_SimpleSchemaGeneratorError():
    region = Region(
        Path("foo"),
        Location(1, 2),
        Location(3, 4),
    )

    ex = SimpleSchemaGeneratorError(Error.Create("Single line, single_region", region))

    assert len(ex.errors) == 1
    assert ex.errors[0].message == "Single line, single_region"
    assert ex.errors[0].regions == [region]


# ----------------------------------------------------------------------
def test_ExceptionError():
    try:
        raise Exception("This is my exception")
    except Exception as ex:
        the_ex = ex

    ee = Error.Create(the_ex)

    assert ee.ex is the_ex
    assert ee.message == "This is my exception"
    assert len(ee.regions) == 1
    assert ee.regions[0].filename == Path(__file__)


# ----------------------------------------------------------------------
def test_ExceptionErrorWithRegion():
    try:
        raise Exception("This is my exception")
    except Exception as ex:
        the_ex = ex

    ee = Error.Create(the_ex, Region.Create(Path("foo"), 1, 2, 3, 4))

    assert ee.ex is the_ex
    assert ee.message == "This is my exception"
    assert len(ee.regions) == 2
    assert ee.regions[0] == Region.Create(Path("foo"), 1, 2, 3, 4)
    assert ee.regions[1].filename == Path(__file__)


# ----------------------------------------------------------------------
def test_CreateErrorType():
    # ----------------------------------------------------------------------
    class MyEnum(Enum):
        a = auto()
        b = auto()

    # ----------------------------------------------------------------------

    region = Region.Create(Path("foo"), 1, 2, 3, 4)
    error_type = CreateErrorType(
        "a: {a}, b: {b}, l: {l}, p: {p}, e: {e}",
        a=int,
        b=str,
        l=list[int],
        p=Path,
        e=MyEnum,
    )

    error = error_type.Create(
        region,
        1,
        "two",
        [1, 2, 3],
        Path("foo"),
        MyEnum.a,
    )

    assert error.a == 1
    assert error.b == "two"
    assert error.l == [1, 2, 3]
    assert error.p == Path("foo")
    assert error.e == MyEnum.a

    assert error.message == "a: 1, b: two, l: ['1', '2', '3'], p: foo, e: a"
    assert error.regions == [region]
