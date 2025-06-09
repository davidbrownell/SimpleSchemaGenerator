# ----------------------------------------------------------------------
# |
# |  TypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-18 09:56:06
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for TypeDefinition.py."""

import re
import textwrap

from enum import auto, Enum
from pathlib import Path
from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Schema.Elements.Common.Metadata import Metadata, MetadataItem
from SimpleSchemaGenerator.Schema.Elements.Common.TerminalElement import TerminalElement
from SimpleSchemaGenerator.Schema.Elements.Expressions.BooleanExpression import BooleanExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.NumberExpression import NumberExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.StringExpression import StringExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.TupleExpression import TupleExpression
from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.TypeDefinition import *


# ----------------------------------------------------------------------
class MyEnum(Enum):
    Value1 = auto()
    Value2 = auto()
    Value3 = auto()


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class MyTypeDefinition(TypeDefinition):
    NAME: ClassVar[str] = "MyTypeDefinition"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (str,)

    boolean_value: bool = field(default=False)
    int_value: int = field(default=0)
    float_value: float = field(default=0.0)
    string_value: str = field(default="")

    optional_value: int | None = field(default=None)
    variant_value: int | str = field(default=0)
    tuple_value: tuple[int, str] = field(default_factory=lambda: (0, ""))
    enum_value: MyEnum = field(default=MyEnum.Value1)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: str,
    ) -> str:
        return value


# ----------------------------------------------------------------------
def test_Construct():
    region = Mock()

    td = MyTypeDefinition(region)

    assert td.region is region
    assert td.NAME == "MyTypeDefinition"
    assert td.SUPPORTED_PYTHON_TYPES == (str,)
    assert {field.name for field in td.FIELDS.values()} == {
        "boolean_value",
        "int_value",
        "float_value",
        "string_value",
        "optional_value",
        "variant_value",
        "tuple_value",
        "enum_value",
    }


# ----------------------------------------------------------------------
def test_ConstructException():
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class TestTypeDefinition(TypeDefinition):
        NAME: ClassVar[str] = "TestTypeDefinition"
        SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (str,)

        def __post_init__(self) -> None:
            raise Exception("This is the exception")

        @override
        def _ToPythonInstanceImpl(self, *args, **kwargs):
            raise Exception("This will never be called")

    # ----------------------------------------------------------------------

    with pytest.raises(
        Exception,
        match=re.escape("This is the exception"),
    ):
        TestTypeDefinition.CreateFromMetadata(Mock(), None)


# ----------------------------------------------------------------------
def test_ConstructSimpleSchemaGeneratorError():
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class TestTypeDefinition(TypeDefinition):
        NAME: ClassVar[str] = "TestTypeDefinition"
        SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (str,)

        def __post_init__(self) -> None:
            raise Errors.SimpleSchemaGeneratorError(
                Error.Create(
                    Exception("This is a test."),
                    region=Region.Create(Path("filename1"), 1, 2, 3, 4),
                ),
            )

        @override
        def _ToPythonInstanceImpl(self, *args, **kwargs):
            raise Exception("This will never be called")

    # ----------------------------------------------------------------------

    with pytest.raises(
        Exception,
        match=re.escape(
            textwrap.dedent(
                """\
                This is a test.

                    - filename1, Ln 1, Col 2 -> Ln 3, Col 4
                    - filename2, Ln 5, Col 6 -> Ln 7, Col 8
                """,
            ),
        ),
    ):
        TestTypeDefinition.CreateFromMetadata(Region.Create(Path("filename2"), 5, 6, 7, 8), None)


# ----------------------------------------------------------------------
def test_ErrorNoName():
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class BadTypeDefinition(TypeDefinition):
        SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (str,)

        @override
        def _ToPythonInstanceImpl(
            self,
            value: str,
        ) -> str:
            return value

    # ----------------------------------------------------------------------

    with pytest.raises(
        Exception,
        match=re.escape("NAME must be defined for 'BadTypeDefinition'."),
    ):
        BadTypeDefinition(Mock())


# ----------------------------------------------------------------------
def test_ErrorNoSupportedTypeTypes():
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class BadTypeDefinition(TypeDefinition):
        NAME: ClassVar[str] = "BadTypeDefinition"

        @override
        def _ToPythonInstanceImpl(
            self,
            value: str,
        ) -> str:
            return value

    # ----------------------------------------------------------------------

    with pytest.raises(
        Exception,
        match=re.escape("SUPPORTED_PYTHON_TYPES must be defined for 'BadTypeDefinition'."),
    ):
        BadTypeDefinition(Mock())


# ----------------------------------------------------------------------
def test_ErrorToPythonInstanceWrongType():
    with pytest.raises(
        Exception,
        match=re.escape("A 'int' value cannot be converted to a 'MyTypeDefinition' instance."),
    ):
        MyTypeDefinition(Mock()).ToPythonInstance(1)


# ----------------------------------------------------------------------
def test_ErrorToPythonInstanceImplSimpleSchemaGeneratorError():
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class BadTypeDefinition(TypeDefinition):
        NAME: ClassVar[str] = "BadTypeDefinition"
        SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (str,)

        @override
        def _ToPythonInstanceImpl(
            self,
            value: str,
        ) -> str:
            raise Errors.SimpleSchemaGeneratorError(Error.Create(Exception("This is a test.")))

    # ----------------------------------------------------------------------

    with pytest.raises(
        Exception,
        match=re.escape("This is a test."),
    ):
        BadTypeDefinition(Mock()).ToPythonInstance("value")


# ----------------------------------------------------------------------
def test_ToPythonInstance():
    td = MyTypeDefinition(Mock())

    assert td.ToPythonInstance("value") == "value"
    assert (
        td.ToPythonInstance(StringExpression(Mock(), "another_value", StringExpression.QuoteType.Single))
        == "another_value"
    )

    with pytest.raises(
        Errors.SimpleSchemaGeneratorError,
        match=re.escape(
            "A 'int' value cannot be converted to a 'MyTypeDefinition' instance. (filename, Ln 1, Col 2 -> Ln 3, Col 4)"
        ),
    ):
        td.ToPythonInstance(IntegerExpression(Region.Create(Path("filename"), 1, 2, 3, 4), 1))


# ----------------------------------------------------------------------
def test_ToPythonInstanceException():
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class TestTypeDefinition(TypeDefinition):
        NAME: ClassVar[str] = "TestTypeDefinition"
        SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (int,)

        @override
        def _ToPythonInstanceImpl(
            self,
            value: str,
        ) -> str:
            raise Exception("This is an exception")

    # ----------------------------------------------------------------------

    td = TestTypeDefinition(Mock())

    with pytest.raises(
        Exception,
        match=re.escape("This is an exception"),
    ):
        td.ToPythonInstance(IntegerExpression(Region.Create(Path("filename"), 1, 2, 3, 4), 123))


# ----------------------------------------------------------------------
def test_ToPythonInstanceSimpleSchemaGeneratorError():
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class TestTypeDefinition(TypeDefinition):
        NAME: ClassVar[str] = "TestTypeDefinition"
        SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (int,)

        @override
        def _ToPythonInstanceImpl(self, *args, **kwargs):
            raise Errors.SimpleSchemaGeneratorError(
                Error.Create(
                    Exception("This is a test."),
                    region=Region.Create(Path("filename1"), 1, 2, 3, 4),
                ),
            )

    # ----------------------------------------------------------------------

    td = TestTypeDefinition(Mock())

    with pytest.raises(
        Exception,
        match=re.escape(
            textwrap.dedent(
                """\
                This is a test.

                    - filename1, Ln 1, Col 2 -> Ln 3, Col 4
                    - filename2, Ln 5, Col 6 -> Ln 7, Col 8
                """,
            ),
        ),
    ):
        td.ToPythonInstance(IntegerExpression(Region.Create(Path("filename2"), 5, 6, 7, 8), 123))


# ----------------------------------------------------------------------
def test_DeriveNewType():
    td = MyTypeDefinition(Mock())

    new_region = Mock()

    new_td = td.DeriveNewType(
        new_region,
        Metadata(
            Mock(),
            [
                MetadataItem(
                    Mock(),
                    TerminalElement[str](Mock(), "string_value"),
                    StringExpression(Mock(), "new_value1", StringExpression.QuoteType.Single),
                )
            ],
        ),
    )

    assert new_td.region is new_region
    assert new_td.region != td.region
    assert new_td.NAME == "MyTypeDefinition"
    assert new_td.SUPPORTED_PYTHON_TYPES == (str,)
    assert {field.name for field in new_td.FIELDS.values()} == {
        "boolean_value",
        "int_value",
        "float_value",
        "string_value",
        "optional_value",
        "variant_value",
        "tuple_value",
        "enum_value",
    }
    assert new_td.string_value == "new_value1"
    assert new_td.int_value == td.int_value
    assert new_td.float_value == td.float_value


# ----------------------------------------------------------------------
def test_CreateFromMetadata():
    td = MyTypeDefinition.CreateFromMetadata(
        Mock(),
        Metadata(
            Mock(),
            [
                MetadataItem(
                    Mock(),
                    TerminalElement[str](Mock(), "boolean_value"),
                    BooleanExpression(Mock(), True, BooleanExpression.Flags.TrueFalse),
                ),
                MetadataItem(
                    Mock(),
                    TerminalElement[str](Mock(), "int_value"),
                    IntegerExpression(Mock(), 1234),
                ),
                MetadataItem(
                    Mock(),
                    TerminalElement[str](Mock(), "float_value"),
                    NumberExpression(Mock(), 3.14),
                ),
                MetadataItem(
                    Mock(),
                    TerminalElement[str](Mock(), "string_value"),
                    StringExpression(Mock(), "hello world!", StringExpression.QuoteType.Single),
                ),
                MetadataItem(
                    Mock(),
                    TerminalElement[str](Mock(), "optional_value"),
                    IntegerExpression(Mock(), 112233),
                ),
                MetadataItem(
                    Mock(),
                    TerminalElement[str](Mock(), "variant_value"),
                    IntegerExpression(Mock(), -1234),
                ),
                MetadataItem(
                    Mock(),
                    TerminalElement[str](Mock(), "tuple_value"),
                    TupleExpression(
                        Mock(),
                        (
                            IntegerExpression(Mock(), 1234),
                            StringExpression(Mock(), "hello", StringExpression.QuoteType.Single),
                        ),
                    ),
                ),
                MetadataItem(
                    Mock(),
                    TerminalElement[str](Mock(), "enum_value"),
                    MyEnum.Value2,
                ),
            ],
        ),
    )

    assert td.boolean_value is True
    assert td.int_value == 1234
    assert td.float_value == 3.14
    assert td.string_value == "hello world!"
    assert td.optional_value == 112233
    assert td.variant_value == -1234
    assert td.tuple_value == (1234, "hello")
    assert td.enum_value is MyEnum.Value2


# ----------------------------------------------------------------------
def test_CreateFromMetadataEmpty():
    td = MyTypeDefinition.CreateFromMetadata(Mock(), None)

    assert td.boolean_value is False
    assert td.int_value == 0
    assert td.float_value == 0.0
    assert td.string_value == ""
    assert td.optional_value is None
    assert td.variant_value == 0
    assert td.tuple_value == (0, "")
    assert td.enum_value is MyEnum.Value1


# ----------------------------------------------------------------------
def test_CreateFromMetadataErrorUnsupportedType():
    # ----------------------------------------------------------------------
    class MyObject:
        pass

    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class BadTypeDefinition(TypeDefinition):
        NAME: ClassVar[str] = "BadTypeDefinition"
        SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (object,)

        bad_value: MyObject

        # ----------------------------------------------------------------------
        @override
        def _ToPythonInstanceImpl(self, *args, **kwargs):
            raise Exception("This should never be called.")

    # ----------------------------------------------------------------------

    with pytest.raises(
        Exception,
        match=re.escape("'MyObject' is not a supported python type."),
    ):
        BadTypeDefinition.CreateFromMetadata(
            Mock(),
            Metadata(
                Mock(),
                [
                    MetadataItem(
                        Mock(),
                        TerminalElement[str](Mock(), "bad_value"),
                        MyObject(),
                    ),
                ],
            ),
        )
