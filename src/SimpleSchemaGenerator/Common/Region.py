# ----------------------------------------------------------------------
# |
# |  Region.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-09 14:11:01
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Region object"""

import inspect

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Union

from .Location import Location
from .Range import Range


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Region(Range):
    """Range that includes source file information."""

    # ----------------------------------------------------------------------
    filename: Path

    # ----------------------------------------------------------------------
    @classmethod
    def Create(
        cls,
        filename: Path,
        begin_line: int,
        begin_column: int,
        end_line: int,
        end_column: int,
    ) -> "Region":
        return cls.CreateFromLocation(
            filename,
            Location(begin_line, begin_column),
            Location(end_line, end_column),
        )

    # ----------------------------------------------------------------------
    @classmethod
    def CreateFromCode(
        cls,
        *,
        callstack_offset: int = 0,
    ) -> "Region":
        frame = inspect.stack()[callstack_offset + 1][0]
        line = frame.f_lineno

        return cls.CreateFromLocation(
            Path(frame.f_code.co_filename),
            Location(line, line),
            Location(line, line),
        )

    # ----------------------------------------------------------------------
    @classmethod
    def CreateFromLocation(
        cls,
        filename: Path,
        begin: Location,
        end: Location,
    ) -> "Region":
        return cls(begin, end, filename)

    # ----------------------------------------------------------------------
    def __str__(self) -> str:
        return self._string

    # ----------------------------------------------------------------------
    @staticmethod
    def Compare(
        this: "Region",  # type: ignore
        that: "Region",  # type: ignore
    ) -> int:
        if this.filename != that.filename:
            return -1 if this.filename < that.filename else 1

        return Range.Compare(this, that)

    # ----------------------------------------------------------------------
    def __eq__(self, other) -> bool:
        return isinstance(other, Region) and self.__class__.Compare(self, other) == 0

    def __ne__(self, other) -> bool:
        return not isinstance(other, Region) or self.__class__.Compare(self, other) != 0

    def __lt__(self, other) -> bool:
        return isinstance(other, Region) and self.__class__.Compare(self, other) < 0

    def __le__(self, other) -> bool:
        return isinstance(other, Region) and self.__class__.Compare(self, other) <= 0

    def __gt__(self, other) -> bool:
        return isinstance(other, Region) and self.__class__.Compare(self, other) > 0

    def __ge__(self, other) -> bool:
        return isinstance(other, Region) and self.__class__.Compare(self, other) >= 0

    # ----------------------------------------------------------------------
    def __contains__(
        self,
        location_range_or_region: Union[Location, Range, "Region"],
    ) -> bool:
        if (
            isinstance(location_range_or_region, Region)
            and self.filename != location_range_or_region.filename
        ):
            return False

        return super(Region, self).__contains__(location_range_or_region)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @cached_property
    def _string(self) -> str:
        return "{}, {}".format(self.filename.as_posix(), super(Region, self)._string)
