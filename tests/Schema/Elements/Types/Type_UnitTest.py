# ----------------------------------------------------------------------
# |
# |  Type_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-21 08:08:11
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Type.py."""

import re
import sys
import textwrap

from dataclasses import MISSING, _MISSING_TYPE
from pathlib import Path
from unittest.mock import MagicMock as Mock

import pytest

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Schema.Elements.Expressions.IntegerExpression import IntegerExpression
from SimpleSchemaGenerator.Schema.Elements.Expressions.StringExpression import StringExpression
from SimpleSchemaGenerator.Schema.Elements.Types.Type import *
from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.IntegerTypeDefinition import (
    IntegerTypeDefinition,
)
from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.StringTypeDefinition import (
    StringTypeDefinition,
)

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def _CreateCardinality(
    min_value: int | None = None,
    max_value: int | None = None,
    region: Region | None = None,
) -> Cardinality:
    return Cardinality(
        region or Mock(),
        None if min_value is None else IntegerExpression(Mock(), min_value),
        None if max_value is None else IntegerExpression(Mock(), max_value),
    )


# ----------------------------------------------------------------------
@pytest.mark.parametrize("is_source", [False, True])
@pytest.mark.parametrize("suppress_region_in_exceptions", [False, True])
@pytest.mark.parametrize(
    "cardinality",
    [
        _CreateCardinality(),
        _CreateCardinality(0, 1),
        _CreateCardinality(0),
    ],
)
def test_Standard(
    cardinality: Cardinality,
    is_source: bool,
    suppress_region_in_exceptions: bool,
) -> None:
    region_mock = Mock()
    type_mock = Mock(spec=TypeDefinition)
    visibility_mock = Mock()
    name_mock = Mock()
    metadata_mock = Mock()

    t = Type(
        region_mock,
        visibility_mock,
        type_mock,
        name_mock,
        cardinality,
        metadata_mock,
        is_source=is_source,
        suppress_region_in_exceptions=suppress_region_in_exceptions,
    )

    assert t.region is region_mock
    assert t.type is type_mock
    assert t.visibility is visibility_mock
    assert t.name is name_mock
    assert t.cardinality is cardinality
    assert t.unresolved_metadata is metadata_mock
    assert t.suppress_region_in_exceptions == suppress_region_in_exceptions

    if is_source:
        assert t.category == Type.Category.Source
    elif cardinality.is_single:
        assert t.category == Type.Category.Alias
    else:
        assert t.category == Type.Category.Reference


# ----------------------------------------------------------------------
def test_AcceptDetails():
    the_type = Mock(spec=TypeDefinition)
    cardinality = _CreateCardinality()
    visibility = Mock()
    name = Mock()

    t = _CreateType(
        the_type,
        cardinality,
        visibility=visibility,
        name=name,
    )

    assert TestElementVisitor(t) == [
        t,
        ("visibility", visibility),
        ("name", name),
        ("cardinality", cardinality),
        ("type", the_type),
    ]


# ----------------------------------------------------------------------
def test_AcceptDetailsWithMetadata():
    the_type = Mock(spec=TypeDefinition)
    cardinality = _CreateCardinality()
    visibility = Mock()
    name = Mock()
    metadata = Metadata(Mock(), [Mock()])

    t = _CreateType(
        the_type,
        cardinality,
        visibility=visibility,
        name=name,
        metadata=metadata,
    )

    assert TestElementVisitor(t) == [
        t,
        ("visibility", visibility),
        ("name", name),
        ("cardinality", cardinality),
        ("metadata", metadata),
        ("type", the_type),
    ]


# ----------------------------------------------------------------------
class TestCreate:
    # ----------------------------------------------------------------------
    @pytest.mark.parametrize(
        "cardinality",
        [
            _CreateCardinality(),
            _CreateCardinality(0),
        ],
    )
    def test_TypeDefinition(
        self,
        cardinality: Cardinality,
    ):
        region_mock = Mock()
        visibility_mock = Mock()
        name_mock = Mock()

        type_mock = Mock(spec=TypeDefinition)
        type_mock.region = region_mock

        metadata_mock = Mock()

        t = Type.Create(
            visibility_mock,
            name_mock,
            type_mock,
            cardinality,
            metadata_mock,
        )

        assert t.region is region_mock
        assert t.visibility is visibility_mock
        assert t.name is name_mock
        assert t.cardinality is cardinality
        assert t.unresolved_metadata is metadata_mock
        assert t.category == Type.Category.Source

        if cardinality.is_single:
            assert t.type is type_mock
        else:
            assert isinstance(t.type, Type), t.type
            assert t.type.category == Type.Category.Source
            assert t.type.type is type_mock

    # ----------------------------------------------------------------------
    @pytest.mark.parametrize(
        "cardinality",
        [
            _CreateCardinality(),
            _CreateCardinality(0),
        ],
    )
    def test_Reference(
        self,
        cardinality: Cardinality,
    ):
        region_mock = Mock()
        visibility_mock = Mock()
        name_mock = Mock()

        type_mock = Mock(spec=Type)
        type_mock.region = region_mock
        type_mock.cardinality = Mock()
        type_mock.category = Type.Category.Reference

        metadata_mock = Mock()

        t = Type.Create(
            visibility_mock,
            name_mock,
            type_mock,
            cardinality,
            metadata_mock,
        )

        assert t.region is region_mock
        assert t.visibility is visibility_mock
        assert t.name is name_mock
        assert t.unresolved_metadata is metadata_mock

        assert isinstance(t.type, Type)
        assert t.type.category == Type.Category.Reference
        assert t.type is type_mock

        if cardinality.is_single:
            assert t.cardinality is type_mock.cardinality
            assert t.category == Type.Category.Alias
        else:
            assert t.cardinality is cardinality

    # ----------------------------------------------------------------------
    def test_MetadataSimplification(self):
        t = Type.Create(
            Mock(),  # visibility
            Mock(),  # name
            Mock(),  # the_type
            Mock(),  # cardinality
            Metadata(Mock(), []),
        )

        assert t.unresolved_metadata is None


# ----------------------------------------------------------------------
def test_ErrorOptionalToOptional():
    referenced_type = Mock(spec=TypeDefinition)
    referenced_type.region = Mock()

    optional_type = _CreateType(
        referenced_type,
        _CreateCardinality(0, 1),
        region=Region.Create(Path("filename1"), 1, 2, 3, 4),
    )

    with pytest.raises(
        Errors.SimpleSchemaGeneratorError,
        match=re.escape(
            textwrap.dedent(
                """\
                Optional types may not reference optional types.

                    - filename2, Ln 5, Col 6 -> Ln 7, Col 8
                    - filename1, Ln 1, Col 2 -> Ln 3, Col 4
                """,
            ),
        ),
    ):
        _CreateType(optional_type, _CreateCardinality(0, 1, Region.Create(Path("filename2"), 5, 6, 7, 8)))


# ----------------------------------------------------------------------
def test_ResolveMetadata():
    t = _CreateType(Mock(spec=TypeDefinition), _CreateCardinality(), metadata=None)

    assert t.is_metadata_resolved is False
    assert t.unresolved_metadata is None

    with pytest.raises(
        RuntimeError,
        match=re.escape("Metadata has not been resolved."),
    ):
        t.resolved_metadata

    t.ResolveMetadata({})

    assert t.is_metadata_resolved is True
    assert t.resolved_metadata == {}

    with pytest.raises(
        TypeError,
        match=re.escape("Metadata has been resolved."),
    ):
        t.unresolved_metadata

    with pytest.raises(
        RuntimeError,
        match=re.escape("Metadata has already been resolved."),
    ):
        t.ResolveMetadata({})


# ----------------------------------------------------------------------
def test_ResolveIsShared():
    t = _CreateType(Mock(spec=TypeDefinition), _CreateCardinality(), metadata=None)

    assert t.is_shared_resolved is False

    with pytest.raises(
        RuntimeError,
        match=re.escape("Shared status has not been resolved."),
    ):
        t.is_shared

    t.ResolveIsShared(True)

    assert t.is_shared_resolved is True
    assert t.is_shared is True

    with pytest.raises(
        RuntimeError,
        match=re.escape("Shared status has already been resolved."),
    ):
        t.ResolveIsShared(True)


# ----------------------------------------------------------------------
class TestResolve:
    # ----------------------------------------------------------------------
    @pytest.mark.parametrize(
        "cardinality",
        [
            _CreateCardinality(),
            _CreateCardinality(0, 1),
            _CreateCardinality(0),
        ],
    )
    def test_Standard(
        self,
        cardinality: Cardinality,
    ):
        type_definition = Mock(spec=TypeDefinition)
        type_definition.region = Mock()

        t = _CreateType(type_definition, cardinality)

        with t.Resolve() as resolved_type:
            assert resolved_type is t

    # ----------------------------------------------------------------------
    def test_SingleReference(self):
        referenced_type = _CreateType(Mock(spec=TypeDefinition), _CreateCardinality())

        t = _CreateType(referenced_type, _CreateCardinality())

        with t.Resolve() as resolved_type:
            assert resolved_type is referenced_type

    # ----------------------------------------------------------------------
    @pytest.mark.parametrize(
        "cardinality",
        [
            _CreateCardinality(0, 1),
            _CreateCardinality(0),
        ],
    )
    def test_MultipleReference(
        self,
        cardinality: Cardinality,
    ):
        referenced_type = _CreateType(Mock(spec=TypeDefinition), _CreateCardinality())

        t = _CreateType(referenced_type, cardinality)

        with t.Resolve() as resolved_type:
            assert resolved_type is t

    # ----------------------------------------------------------------------
    def test_ErrorSingle(self):
        t = _CreateType(
            Mock(spec=TypeDefinition),
            _CreateCardinality(),
            region=Region.Create(Path("the--filename"), 2, 4, 6, 8),
        )

        with pytest.raises(
            Errors.SimpleSchemaGeneratorError,
            match=re.escape("An error (the--filename, Ln 2, Col 4 -> Ln 6, Col 8)"),
        ):
            with t.Resolve():
                raise Exception("An error")

        with pytest.raises(
            Errors.SimpleSchemaGeneratorError,
            match=re.escape(
                textwrap.dedent(
                    """\
                    An error

                        - This unique file, Ln 1, Col 2 -> Ln 3, Col 4
                        - the--filename, Ln 2, Col 4 -> Ln 6, Col 8
                    """,
                ),
            ),
        ):
            with t.Resolve():
                raise Errors.SimpleSchemaGeneratorError(
                    Error.Create(
                        Exception("An error"),
                        Region.Create(Path("This unique file"), 1, 2, 3, 4),
                    ),
                )

    # ----------------------------------------------------------------------
    def test_ErrorReference(self):
        t = _CreateType(
            _CreateType(
                Mock(spec=TypeDefinition),
                _CreateCardinality(),
                region=Region.Create(Path("filename1"), 2, 4, 6, 8),
            ),
            _CreateCardinality(),
            region=Region.Create(Path("filename2"), 6, 8, 10, 12),
        )

        with pytest.raises(
            Errors.SimpleSchemaGeneratorError,
            match=re.escape(
                textwrap.dedent(
                    """\
                    An error

                        - filename1, Ln 2, Col 4 -> Ln 6, Col 8
                        - filename2, Ln 6, Col 8 -> Ln 10, Col 12
                    """,
                ),
            ),
        ):
            with t.Resolve():
                raise Exception("An error")

        with pytest.raises(
            Errors.SimpleSchemaGeneratorError,
            match=re.escape(
                textwrap.dedent(
                    """\
                    An error

                        - filename3, Ln 14, Col 16 -> Ln 18, Col 20
                        - filename1, Ln 2, Col 4 -> Ln 6, Col 8
                        - filename2, Ln 6, Col 8 -> Ln 10, Col 12
                    """,
                ),
            ),
        ):
            with t.Resolve():
                raise Errors.SimpleSchemaGeneratorError(
                    Error.Create(
                        Exception("An error"),
                        region=Region.Create(Path("filename3"), 14, 16, 18, 20),
                    ),
                )


# ----------------------------------------------------------------------
class TestToPythonInstance:
    # ----------------------------------------------------------------------
    def test_Standard(self):
        t = _CreateType(
            StringTypeDefinition(Mock()),
            _CreateCardinality(),
        )

        assert t.ToPythonInstance("foo") == "foo"
        assert t.ToPythonInstance(StringExpression(Mock(), "bar", StringExpression.QuoteType.Single)) == "bar"

    # ----------------------------------------------------------------------
    def test_Multiple(self):
        t = _CreateType(
            StringTypeDefinition(Mock()),
            _CreateCardinality(2, 2),
        )

        assert t.ToPythonInstance(["foo", "bar"]) == ["foo", "bar"]

        assert t.ToPythonInstance(
            [
                StringExpression(Mock(), "biz", StringExpression.QuoteType.Single),
                StringExpression(Mock(), "baz", StringExpression.QuoteType.Single),
            ],
        ) == ["biz", "baz"]

    # ----------------------------------------------------------------------
    def test_Optional(self):
        t = _CreateType(
            StringTypeDefinition(Mock()),
            _CreateCardinality(0, 1),
        )

        assert t.ToPythonInstance(None) is None
        assert t.ToPythonInstance("foo") == "foo"

        assert t.ToPythonInstance(NoneExpression(Mock())) is None
        assert t.ToPythonInstance(StringExpression(Mock(), "bar", StringExpression.QuoteType.Single)) == "bar"

    # ----------------------------------------------------------------------
    def test_Alias(self):
        t = _CreateType(
            _CreateType(
                StringTypeDefinition(Mock()),
                _CreateCardinality(),
            ),
            _CreateCardinality(),
        )

        assert t.ToPythonInstance("foo") == "foo"

    # ----------------------------------------------------------------------
    def test_SingleVariant(self):
        t = _CreateType(
            VariantTypeDefinition(
                Mock(),
                [
                    _CreateType(StringTypeDefinition(Mock()), _CreateCardinality()),
                    _CreateType(IntegerTypeDefinition(Mock()), _CreateCardinality()),
                ],
            ),
            _CreateCardinality(),
        )

        assert t.ToPythonInstance("foo") == "foo"
        assert t.ToPythonInstance(123) == 123
        assert t.ToPythonInstance(StringExpression(Mock(), "bar", StringExpression.QuoteType.Single)) == "bar"
        assert t.ToPythonInstance(IntegerExpression(Mock(), 456)) == 456

    # ----------------------------------------------------------------------
    def test_SingleVariantWithDifferentCardinality(self):
        t = _CreateType(
            VariantTypeDefinition(
                Mock(),
                [
                    _CreateType(
                        StringTypeDefinition(Mock()),
                        _CreateCardinality(2, 2),
                    ),
                    _CreateType(
                        IntegerTypeDefinition(Mock()),
                        _CreateCardinality(3, 3),
                    ),
                ],
            ),
            _CreateCardinality(),
        )

        assert t.ToPythonInstance(["foo", "bar"]) == ["foo", "bar"]
        assert t.ToPythonInstance([1, 2, 3]) == [1, 2, 3]

        assert t.ToPythonInstance(
            ListExpression(
                Mock(),
                [
                    StringExpression(Mock(), "baz", StringExpression.QuoteType.Single),
                    StringExpression(Mock(), "biz", StringExpression.QuoteType.Single),
                ],
            ),
        ) == ["baz", "biz"]

    # ----------------------------------------------------------------------
    def test_MultipleVariant(self):
        t = _CreateType(
            VariantTypeDefinition(
                Mock(),
                [
                    _CreateType(StringTypeDefinition(Mock()), _CreateCardinality(2, 2)),
                    _CreateType(IntegerTypeDefinition(Mock()), _CreateCardinality(3, 3)),
                ],
            ),
            _CreateCardinality(3, 3),
        )

        assert t.ToPythonInstance(
            [
                ["foo", "bar"],
                [1, 2, 3],
                [4, 5, 6],
            ],
        ) == [
            ["foo", "bar"],
            [1, 2, 3],
            [4, 5, 6],
        ]

        assert t.ToPythonInstance(
            ListExpression(
                Mock(),
                [
                    ListExpression(
                        Mock(),
                        [
                            StringExpression(Mock(), "foo", StringExpression.QuoteType.Single),
                            StringExpression(Mock(), "bar", StringExpression.QuoteType.Single),
                        ],
                    ),
                    ListExpression(
                        Mock(),
                        [
                            IntegerExpression(Mock(), 1),
                            IntegerExpression(Mock(), 2),
                            IntegerExpression(Mock(), 3),
                        ],
                    ),
                    ListExpression(
                        Mock(),
                        [
                            IntegerExpression(Mock(), 4),
                            IntegerExpression(Mock(), 5),
                            IntegerExpression(Mock(), 6),
                        ],
                    ),
                ],
            ),
        ) == [
            ["foo", "bar"],
            [1, 2, 3],
            [4, 5, 6],
        ]


# ----------------------------------------------------------------------
class TestDisplayType:
    # ----------------------------------------------------------------------
    def test_Single(self):
        t = _CreateType(IntegerTypeDefinition(Mock()), _CreateCardinality())

        assert t.display_type == "Integer"

    # ----------------------------------------------------------------------
    def test_Multiple(self):
        t = _CreateType(IntegerTypeDefinition(Mock()), _CreateCardinality(2, 2))

        assert t.display_type == "Integer[2]"

    # ----------------------------------------------------------------------
    def test_SingleWithConstraints(self):
        t = _CreateType(IntegerTypeDefinition(Mock(), min=5), _CreateCardinality())

        assert t.display_type == "Integer {>= 5}"

    # ----------------------------------------------------------------------
    def test_MultipleWithConstraints(self):
        t = _CreateType(IntegerTypeDefinition(Mock(), min=5), _CreateCardinality(2, 2))

        assert t.display_type == "<Integer {>= 5}>[2]"


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _CreateType(
    the_type: TypeDefinition | Type,
    cardinality: Cardinality,
    *,
    region: Region | None = None,
    visibility: TerminalElement[Visibility] | None = None,
    name: TerminalElement[str] | None = None,
    metadata: _MISSING_TYPE | None | Metadata = MISSING,
    suppress_region_in_exceptions: bool = False,
) -> Type:
    return Type.Create(
        visibility or Mock(),
        name or Mock(),
        the_type,
        cardinality,
        Mock() if metadata is MISSING else metadata,
        region=region or Mock(),
        suppress_region_in_exceptions=suppress_region_in_exceptions,
    )
