# ----------------------------------------------------------------------
# |
# |  FundamentalTypes.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-22 12:22:16
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains information relative to TypeDefinitions that are considered to be fundamental (e.g. built into the language)."""

from .TypeDefinitions.BooleanTypeDefinition import BooleanTypeDefinition
from .TypeDefinitions.DateTimeTypeDefinition import DateTimeTypeDefinition
from .TypeDefinitions.DateTypeDefinition import DateTypeDefinition
from .TypeDefinitions.DirectoryTypeDefinition import DirectoryTypeDefinition
from .TypeDefinitions.DurationTypeDefinition import DurationTypeDefinition
from .TypeDefinitions.EnumTypeDefinition import EnumTypeDefinition
from .TypeDefinitions.FilenameTypeDefinition import FilenameTypeDefinition
from .TypeDefinitions.GuidTypeDefinition import GuidTypeDefinition
from .TypeDefinitions.IntegerTypeDefinition import IntegerTypeDefinition
from .TypeDefinitions.NumberTypeDefinition import NumberTypeDefinition
from .TypeDefinitions.StringTypeDefinition import StringTypeDefinition
from .TypeDefinitions.TimeTypeDefinition import TimeTypeDefinition
from .TypeDefinitions.TypeDefinition import TypeDefinition
from .TypeDefinitions.UriTypeDefinition import UriTypeDefinition


# ----------------------------------------------------------------------
fundamental_types: tuple[type[TypeDefinition], ...] = (
    BooleanTypeDefinition,
    DateTimeTypeDefinition,
    DateTypeDefinition,
    DirectoryTypeDefinition,
    DurationTypeDefinition,
    EnumTypeDefinition,
    FilenameTypeDefinition,
    GuidTypeDefinition,
    IntegerTypeDefinition,
    NumberTypeDefinition,
    StringTypeDefinition,
    TimeTypeDefinition,
    UriTypeDefinition,
)
