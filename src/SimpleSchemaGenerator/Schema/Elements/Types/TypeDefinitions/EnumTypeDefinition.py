# ----------------------------------------------------------------------
# |
# |  EnumTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-15 09:51:38
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the EnumTypeDefinition object."""

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum, EnumMeta
from typing import cast, ClassVar

from dbrownell_Common.Types import override

from .TypeDefinition import TypeDefinition
from SimpleSchemaGenerator import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class EnumTypeDefinition(TypeDefinition):
    """An Enum type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Enum"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (Enum, str, int)

    values: (
        list[str]
        | list[int]
        | list[tuple[int, int]]
        | list[tuple[int, str]]
        | list[tuple[str, int]]
        | list[tuple[str, str]]
        | EnumMeta
    )

    starting_value: int = field(default=1)

    EnumClass: EnumMeta = field(init=False)

    # ----------------------------------------------------------------------
    def __post_init__(self) -> None:  # noqa: C901, PLR0915
        if isinstance(self.values, EnumMeta):
            enum_class = self.values
        else:
            if not self.values:
                raise ValueError(Errors.enum_typedef_values_required)

            if isinstance(self.values[0], tuple):
                # ----------------------------------------------------------------------
                def GetTupleValue(index: int) -> int | str:
                    assert isinstance(self.values, list), self.values
                    v = self.values[index]

                    if not isinstance(v, tuple):
                        raise TypeError(Errors.enum_typedef_tuple_expected.format(index=index))

                    if not v[1]:
                        if isinstance(v[1], str):
                            raise ValueError(Errors.enum_typedef_string_value_required.format(index=index))
                        if isinstance(v[1], int):
                            raise ValueError(Errors.enum_typedef_non_zero_required.format(index=index))

                        raise AssertionError(v[1])  # pragma: no cover

                    return v[0]

                # ----------------------------------------------------------------------

                get_value_func = GetTupleValue

                if isinstance(self.values[0][1], str):
                    # ----------------------------------------------------------------------
                    def CreateTupleStrEnumType(
                        value_to_enum_func: Callable[[int | str], str],
                    ) -> Enum:
                        return Enum(
                            "EnumClass",
                            {
                                value_to_enum_func(value[0]): value[1]
                                for value in cast(list[tuple[int | str, str]], self.values)
                            },
                            type=str,
                        )

                    # ----------------------------------------------------------------------

                    create_enum_class_func = CreateTupleStrEnumType

                elif isinstance(self.values[0][1], int):
                    # ----------------------------------------------------------------------
                    def CreateTupleIntEnumType(
                        value_to_enum_func: Callable[[int | str], int],
                    ) -> Enum:
                        return Enum(
                            "EnumClass",
                            {
                                value_to_enum_func(value[0]): value[1]
                                for value in cast(list[tuple[int | str, int]], self.values)
                            },
                        )

                    # ----------------------------------------------------------------------

                    create_enum_class_func = CreateTupleIntEnumType

                else:
                    raise TypeError(Errors.enum_typedef_int_or_string_expected)

            else:
                # ----------------------------------------------------------------------
                def GetNonTupleValue(index: int) -> int | str:
                    assert isinstance(self.values, list), self.values
                    v = self.values[index]

                    if isinstance(v, tuple):
                        raise TypeError(Errors.enum_typedef_tuple_not_expected.format(index=index))

                    return v

                # ----------------------------------------------------------------------
                def CreateNonTupleEnumType(
                    value_to_enum_name_func: Callable[[int | str], str],
                ) -> Enum:
                    return Enum(
                        "EnumClass",
                        {
                            value_to_enum_name_func(value): int_value + self.starting_value
                            for int_value, value in enumerate(cast(list[int | str], self.values))
                        },
                    )

                # ----------------------------------------------------------------------

                get_value_func = GetNonTupleValue
                create_enum_class_func = CreateNonTupleEnumType

            expected_type: type | None = None

            if isinstance(get_value_func(0), int):
                # ----------------------------------------------------------------------
                def ValueFormat(value: str) -> str:
                    return f"Value{value}"

                # ----------------------------------------------------------------------

                value_to_enum_name_func = ValueFormat

                expected_type = int
                expected_desc = "An Integer"

            elif isinstance(get_value_func(0), str):
                # ----------------------------------------------------------------------
                def ValueIdentity(value: str) -> str:
                    return value

                # ----------------------------------------------------------------------

                value_to_enum_name_func = ValueIdentity

                expected_type = str
                expected_desc = "A String"

            else:
                raise TypeError(Errors.enum_typedef_int_or_string_expected)

            assert expected_type is not None

            for value in range(1, len(self.values)):
                if not isinstance(get_value_func(value), expected_type):
                    raise TypeError(f"{expected_desc} was expected (index: {value}).")  # noqa: EM102, TRY003

            enum_class = create_enum_class_func(value_to_enum_name_func)

        # Commit
        object.__setattr__(self, "EnumClass", enum_class)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: Enum | int | str,
    ) -> Enum:
        if isinstance(value, Enum) and value in self.EnumClass:
            return value

        if isinstance(value, int):
            for e in self.EnumClass:
                if e.value == value:
                    return e

            value = f"Value{value}"

        if isinstance(value, str):
            # Check by name
            for e in self.EnumClass:
                if e.name == value:
                    return e

            # Check by value
            for e in self.EnumClass:
                if e.value == value:
                    return e

        raise Exception(Errors.enum_typedef_invalid_value.format(value=value))
