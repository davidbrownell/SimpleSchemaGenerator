# ----------------------------------------------------------------------
# |
# |  ParseIdentifier.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-12 19:00:34
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the ParseIdentifier object."""

from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional

import emoji

from ......Elements.Common.Element import Element
from ......Elements.Common.Visibility import Visibility
from ......Elements.Common.TerminalElement import TerminalElement

from ....... import Errors
from .......Common.Region import Location, Region


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ParseIdentifier(Element):
    """Identifier generated during parsing and replaced in subsequent steps."""

    # ----------------------------------------------------------------------
    value: str

    _first_char: str = field(init=False)

    # ----------------------------------------------------------------------
    def __post_init__(self):
        first_char = self.__class__._GetFirstChar(self.value)  # pylint: disable=protected-access

        if first_char is None:
            raise Errors.SimpleSchemaGeneratorException(
                Errors.ParseIdentifierNoChars.Create(self.region, self.value)
            )

        if not (
            ("a" <= first_char <= "z") or ("A" <= first_char <= "Z") or emoji.is_emoji(first_char)
        ):
            raise Errors.SimpleSchemaGeneratorException(
                Errors.ParseIdentifierNotAlpha.Create(self.region, self.value)
            )

        # Commit
        object.__setattr__(self, "_first_char", first_char)

    # ----------------------------------------------------------------------
    @cached_property
    def is_expression(self) -> bool:
        return self._first_char.islower()

    @cached_property
    def is_type(self) -> bool:
        return self._first_char.isupper() or emoji.is_emoji(self._first_char)

    @cached_property
    def visibility(self) -> TerminalElement[Visibility]:
        region_value: Optional[Region] = None

        if self.value[0] == "_":
            visibility = Visibility.Private
        elif self.value[0] in ["@", "$", "&"]:
            visibility = Visibility.Protected
        else:
            visibility = Visibility.Public
            region_value = self.region

        if region_value is None:
            region_value = Region(
                self.region.filename,
                self.region.begin,
                Location(self.region.begin.line, self.region.begin.column + 1),
            )

        assert region_value is not None
        return TerminalElement[Visibility](region_value, visibility)

    # ----------------------------------------------------------------------
    def ToTerminalElement(self) -> TerminalElement[str]:
        return TerminalElement[str](self.region, self.value)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @staticmethod
    def _GetFirstChar(
        value: str,
    ) -> Optional[str]:
        for char in value:
            if char not in ["_", "@", "$", "&"]:
                return char

        return None
