# ----------------------------------------------------------------------
# |
# |  StringTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-16 10:44:10
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the StringTypeDefinition object."""

import re

from dataclasses import dataclass, field
from typing import ClassVar, Optional, Pattern, Type as PythonType

from dbrownell_Common.InflectEx import inflect  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition
from ..... import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class StringTypeDefinition(TypeDefinition):
    """A String type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "String"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (str,)

    min_length: int = field(default=1)
    max_length: Optional[int] = field(default=None)

    validation_expression: Optional[str] = field(default=None)
    _validation_regex: Optional[Pattern] = field(init=False, repr=False, hash=False, compare=False)

    # ----------------------------------------------------------------------
    def __post_init__(self) -> None:
        if self.min_length < 1:
            raise ValueError(
                Errors.string_typedef_invalid_min_length.format(min_length=self.min_length)
            )

        if self.max_length is not None and self.min_length > self.max_length:
            raise ValueError(
                Errors.string_typedef_invalid_max_length.format(
                    min_length=self.min_length, max_length=self.max_length
                )
            )

        if self.validation_expression is None:
            validation_regex = None
        else:
            validation_regex = re.compile(self.validation_expression)

        object.__setattr__(self, "_validation_regex", validation_regex)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        constraints: list[str] = []

        if self.min_length != 1:
            constraints.append(">= {}".format(inflect.no("character", self.min_length)))
        if self.max_length is not None:
            constraints.append("<= {}".format(inflect.no("character", self.max_length)))
        if self.validation_expression is not None:
            constraints.append(f"matches '{self.validation_expression}'")

        result = super(StringTypeDefinition, self)._display_type

        if constraints:
            result += " {{{}}}".format(", ".join(constraints))

        return result

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: str,
    ) -> str:
        num_chars = len(value)

        if num_chars < self.min_length:
            raise Exception(
                Errors.string_typedef_too_small.format(
                    value=inflect.no("character", self.min_length),
                    value_verb=inflect.plural_verb("was", self.min_length),
                    found=inflect.no("character", num_chars),
                    found_verb=inflect.plural_verb("was", num_chars),
                ),
            )

        if self.max_length is not None and num_chars > self.max_length:
            raise Exception(
                Errors.string_typedef_too_large.format(
                    value=inflect.no("character", self.max_length),
                    value_verb=inflect.plural_verb("was", self.max_length),
                    found=inflect.no("character", num_chars),
                    found_verb=inflect.plural_verb("was", num_chars),
                ),
            )

        if self._validation_regex is not None and not self._validation_regex.match(value):
            raise Exception(
                Errors.string_typedef_regex_failure.format(
                    value=value,
                    expression=self._validation_regex.pattern,
                ),
            )

        return value
