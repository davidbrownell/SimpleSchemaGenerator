# ----------------------------------------------------------------------
# |
# |  TypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-10 11:53:38
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for TypeDefinition.py."""

import re

from pathlib import Path

import pytest

from SimpleSchemaGenerator.Schema.Elements.Common.TerminalElement import TerminalElement
from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression
from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.TypeDefinition import *


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class OddNumberTypeDefinition(TypeDefinition):
    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "OddNumber"

    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (int,)

    min: Optional[int] = field(default=None)
    max: Optional[int] = field(default=None)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: Any,
    ) -> int:
        if not value & 1:
            raise Exception(f"'{value}' is not an odd number.")

        if self.min is not None and value < self.min:
            raise Exception(f"'{value}' is less than the minimum value of '{self.min}'.")

        if self.max is not None and value > self.max:
            raise Exception(f"'{value}' is greater than the maximum value of '{self.max}'.")

        return value


# ----------------------------------------------------------------------
def test_ToPythonInstanceWithValue():
    td = OddNumberTypeDefinition(Region.CreateFromCode())

    assert td.ToPythonInstance(123) == 123

    with pytest.raises(
        Exception,
        match="A 'str' value cannot be converted to a 'OddNumber' type.",
    ):
        td.ToPythonInstance("this is not a number")


# ----------------------------------------------------------------------
def test_ToPythonInstanceWithExpression():
    td = OddNumberTypeDefinition(Region.CreateFromCode())

    assert td.ToPythonInstance(IntegerExpression(Region.CreateFromCode(), 123)) == 123

    with pytest.raises(
        Exception,
        match=re.escape(
            "A 'str' value cannot be converted to a 'OddNumber' type. (filename, Ln 1, Col 2 -> Ln 3, Col 4)"
        ),
    ):
        td.ToPythonInstance(
            IntegerExpression(
                Region.Create(Path("filename"), 1, 2, 3, 4),
                "this is not a number",
            ),
        )


# ----------------------------------------------------------------------
def test_ToPythonInstanceWithMetadata():
    td = OddNumberTypeDefinition(Region.CreateFromCode(), 11, 99)

    assert td.ToPythonInstance(23) == 23

    with pytest.raises(
        Exception,
        match=re.escape("'7' is less than the minimum value of '11'."),
    ):
        td.ToPythonInstance(7)

    with pytest.raises(
        Exception,
        match=re.escape("'123' is greater than the maximum value of '99'."),
    ):
        td.ToPythonInstance(123)

    with pytest.raises(
        Exception,
        match=re.escape("'50' is not an odd number."),
    ):
        td.ToPythonInstance(50)


# ----------------------------------------------------------------------
# BugBug: Can't do this until Type is defined
def BugBugtest_DeriveNewTypeDefinition():
    td1 = OddNumberTypeDefinition(Region.CreateFromCode(), 11, 99)
    td2 = td1.DeriveNewTypeDefinition(
        Region.CreateFromCode(),
        Metadata(
            Region.CreateFromCode(),
            [
                MetadataItem(
                    Region.CreateFromCode(),
                    TerminalElement[str](Region.CreateFromCode(), "min"),
                    IntegerExpression(Region.CreateFromCode(), 7),
                ),
            ],
        ),
    )

    assert td1.region != td2.region
    assert td1.min == 11
    assert td2.min == 7
    assert td1.max == td2.max
