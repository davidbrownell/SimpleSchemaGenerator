# ----------------------------------------------------------------------
# |
# |  FilenameTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-16 08:37:59
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the FilenameTypeDefinition object."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from dbrownell_Common.Types import override

from .TypeDefinition import TypeDefinition
from SimpleSchemaGenerator import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class FilenameTypeDefinition(TypeDefinition):
    """A Filename type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Filename"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (Path,)

    ensure_exists: bool = field(default=True, kw_only=True)
    match_any: bool = field(default=False, kw_only=True)

    # ----------------------------------------------------------------------
    def __post_init__(self) -> None:
        if self.match_any and not self.ensure_exists:
            raise ValueError(Errors.filename_typedef_invalid_match_any)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        result = super()._display_type

        if self.ensure_exists:
            result += "!"

        if self.match_any:
            result += "^"

        return result

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: Path,
    ) -> Path:
        if self.ensure_exists:
            if self.match_any and not value.exists():
                raise Exception(Errors.filename_typedef_does_not_exist.format(value=value))
            if not self.match_any and not value.is_file():
                raise Exception(Errors.filename_typedef_invalid_file.format(value=value))

        return value
