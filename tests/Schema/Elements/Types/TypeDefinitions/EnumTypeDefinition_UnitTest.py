# ----------------------------------------------------------------------
# |
# |  EnumTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-15 14:13:05
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for EnumTypeDefinition.py."""

import re

from enum import auto, Enum
from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.EnumTypeDefinition import *


# ----------------------------------------------------------------------
def test_DisplayType():
    assert EnumTypeDefinition(Mock(), [1, 2, 3]).display_type == "Enum"


# ----------------------------------------------------------------------
def test_Strs():
    td = EnumTypeDefinition(Mock(), ["one", "two", "three"])

    assert td.ToPythonInstance(td.EnumClass.one) is td.EnumClass.one
    assert td.EnumClass.one.value == 1

    assert td.ToPythonInstance("two") is td.EnumClass.two
    assert td.EnumClass.two.value == 2

    assert td.ToPythonInstance(3) is td.EnumClass.three
    assert td.EnumClass.three.value == 3


# ----------------------------------------------------------------------
def test_StrsCustomValues():
    td = EnumTypeDefinition(Mock(), ["one", "two", "three"], 10)

    assert td.ToPythonInstance(td.EnumClass.one) is td.EnumClass.one
    assert td.EnumClass.one.value == 10

    assert td.ToPythonInstance("two") is td.EnumClass.two
    assert td.EnumClass.two.value == 11

    assert td.ToPythonInstance(12) is td.EnumClass.three
    assert td.EnumClass.three.value == 12


# ----------------------------------------------------------------------
def test_Ints():
    td = EnumTypeDefinition(Mock(), [1, 2, 3])

    assert td.ToPythonInstance(td.EnumClass.Value1) is td.EnumClass.Value1
    assert td.EnumClass.Value1.value == 1

    assert td.ToPythonInstance("Value2") is td.EnumClass.Value2
    assert td.EnumClass.Value2.value == 2

    assert td.ToPythonInstance(3) is td.EnumClass.Value3
    assert td.EnumClass.Value3.value == 3


# ----------------------------------------------------------------------
def test_IntString():
    td = EnumTypeDefinition(
        Mock(),
        [
            (1, "TheValue1"),
            (2, "TheValue2"),
            (3, "TheValue3"),
        ],
    )

    assert td.ToPythonInstance(td.EnumClass.Value1) is td.EnumClass.Value1
    assert td.EnumClass.Value1.value == "TheValue1"

    assert td.ToPythonInstance("Value2") is td.EnumClass.Value2
    assert td.ToPythonInstance("TheValue2") is td.EnumClass.Value2
    assert td.EnumClass.Value2.value == "TheValue2"

    assert td.ToPythonInstance(3) is td.EnumClass.Value3
    assert td.EnumClass.Value3.value == "TheValue3"


# ----------------------------------------------------------------------
def test_IntInt():
    td = EnumTypeDefinition(
        Mock(),
        [
            (1, 11),
            (2, 22),
            (3, 33),
        ],
    )

    assert td.ToPythonInstance(td.EnumClass.Value1) is td.EnumClass.Value1
    assert td.EnumClass.Value1.value == 11

    assert td.ToPythonInstance("Value2") is td.EnumClass.Value2
    assert td.ToPythonInstance(22) is td.EnumClass.Value2
    assert td.EnumClass.Value2.value == 22

    assert td.ToPythonInstance(3) is td.EnumClass.Value3
    assert td.EnumClass.Value3.value == 33


# ----------------------------------------------------------------------
def test_StringInt():
    td = EnumTypeDefinition(
        Mock(),
        [
            ("Key1", 11),
            ("Key2", 22),
            ("Key3", 33),
        ],
    )

    assert td.ToPythonInstance(td.EnumClass.Key1) is td.EnumClass.Key1
    assert td.EnumClass.Key1.value == 11

    assert td.ToPythonInstance("Key2") is td.EnumClass.Key2
    assert td.ToPythonInstance(22) == td.EnumClass.Key2
    assert td.EnumClass.Key2.value == 22

    assert td.EnumClass.Key3.value == 33


# ----------------------------------------------------------------------
def test_StringString():
    td = EnumTypeDefinition(
        Mock(),
        [
            ("Key1", "TheValue1"),
            ("Key2", "TheValue2"),
            ("Key3", "TheValue3"),
        ],
    )

    assert td.ToPythonInstance(td.EnumClass.Key1) is td.EnumClass.Key1
    assert td.EnumClass.Key1.value == "TheValue1"

    assert td.ToPythonInstance("Key2") is td.EnumClass.Key2
    assert td.ToPythonInstance("TheValue2") is td.EnumClass.Key2

    assert td.EnumClass.Key3.value == "TheValue3"


# ----------------------------------------------------------------------
def test_ExistingClass():
    # ----------------------------------------------------------------------
    class MyEnum(Enum):
        Value1 = auto()
        Value2 = auto()
        Value3 = auto()

    # ----------------------------------------------------------------------

    td = EnumTypeDefinition(Mock(), MyEnum)

    assert td.EnumClass is MyEnum
    assert td.ToPythonInstance(MyEnum.Value2) is MyEnum.Value2


# ----------------------------------------------------------------------
def test_ErrorNoValues():
    with pytest.raises(
        ValueError,
        match=re.escape("Values must be provided."),
    ):
        EnumTypeDefinition(Mock(), [])


# ----------------------------------------------------------------------
def test_ErrorNonTupleAfterTuple():
    with pytest.raises(
        TypeError,
        match=re.escape("A tuple was expected (index: 1)."),
    ):
        EnumTypeDefinition(Mock(), [(1, "Value1"), 2])


# ----------------------------------------------------------------------
def test_ErrorEmptyString():
    with pytest.raises(
        ValueError,
        match=re.escape("A string value is required (index: 2)."),
    ):
        EnumTypeDefinition(Mock(), [(1, "Value1"), (2, "Value2"), (3, "")])


# ----------------------------------------------------------------------
def test_ErrorZero():
    with pytest.raises(
        ValueError,
        match=re.escape("A non-zero value is required (index: 1)."),
    ):
        EnumTypeDefinition(Mock(), [(1, 1), (2, 0)])


# ----------------------------------------------------------------------
def test_ErrorInvalidValueTuple():
    with pytest.raises(
        TypeError,
        match=re.escape("An Integer or String value was expected."),
    ):
        EnumTypeDefinition(Mock(), [("One", 3.14)])


# ----------------------------------------------------------------------
def test_ErrorInvalidValueNonTuple():
    with pytest.raises(
        TypeError,
        match=re.escape("An Integer or String value was expected."),
    ):
        EnumTypeDefinition(Mock(), [3.14])


# ----------------------------------------------------------------------
def test_ErrorTupleAfterNonTuple():
    with pytest.raises(
        TypeError,
        match=re.escape("A tuple was not expected (index: 1)."),
    ):
        EnumTypeDefinition(Mock(), [1, (2, "Value2")])


# ----------------------------------------------------------------------
def test_ErrorMixedInt():
    with pytest.raises(
        TypeError,
        match=re.escape("A String was expected (index: 3)."),
    ):
        EnumTypeDefinition(Mock(), ["one", "two", "three", 4])


# ----------------------------------------------------------------------
def test_ErrorMixedString():
    with pytest.raises(
        TypeError,
        match=re.escape("An Integer was expected (index: 3)."),
    ):
        EnumTypeDefinition(Mock(), [1, 2, 3, "four"])


# ----------------------------------------------------------------------
def test_ErrorInvalidValue():
    td = EnumTypeDefinition(Mock(), [1, 2, 3])

    with pytest.raises(
        Exception,
        match="'123' is not a valid enum value.",
    ):
        td.ToPythonInstance("123")
