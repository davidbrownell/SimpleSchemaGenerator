# ----------------------------------------------------------------------
# |
# |  DirectoryTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-14 15:05:33
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the DirectoryTypeDefinition object."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Type as PythonType

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition
from ..... import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class DirectoryTypeDefinition(TypeDefinition):
    """A Directory type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Directory"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (Path,)

    ensure_exists: bool = field(default=True, kw_only=True)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        result = super(DirectoryTypeDefinition, self)._display_type

        if self.ensure_exists:
            result += "!"

        return result

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: Path,
    ) -> Path:
        if self.ensure_exists and not value.is_dir():
            raise Exception(Errors.directory_typedef_invalid_dir.format(value=value))

        return value
