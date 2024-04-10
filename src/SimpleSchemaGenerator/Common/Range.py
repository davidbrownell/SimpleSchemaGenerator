# ----------------------------------------------------------------------
# |
# |  Range.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-09 14:18:26
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Range object"""

from dataclasses import dataclass
from functools import cached_property
from typing import Union

from .Location import Location


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Range:
    """A range of locations within a source file"""

    # ----------------------------------------------------------------------
    begin: Location
    end: Location

    # ----------------------------------------------------------------------
    def __post_init__(self):
        if self.end < self.begin:
            raise ValueError("Invalid end")

    # ----------------------------------------------------------------------
    def __str__(self) -> str:
        return self._string

    # ----------------------------------------------------------------------
    @staticmethod
    def Compare(
        this: "Range",
        that: "Range",
    ) -> int:
        result = Location.Compare(this.begin, that.begin)
        if result != 0:
            return result

        result = Location.Compare(this.end, that.end)
        if result != 0:
            return result

        return 0

    # ----------------------------------------------------------------------
    def __eq__(self, other) -> bool:
        return isinstance(other, Range) and self.__class__.Compare(self, other) == 0

    def __ne__(self, other) -> bool:
        return not isinstance(other, Range) or self.__class__.Compare(self, other) != 0

    def __lt__(self, other) -> bool:
        return isinstance(other, Range) and self.__class__.Compare(self, other) < 0

    def __le__(self, other) -> bool:
        return isinstance(other, Range) and self.__class__.Compare(self, other) <= 0

    def __gt__(self, other) -> bool:
        return isinstance(other, Range) and self.__class__.Compare(self, other) > 0

    def __ge__(self, other) -> bool:
        return isinstance(other, Range) and self.__class__.Compare(self, other) >= 0

    # ----------------------------------------------------------------------
    def __contains__(
        self,
        location_or_range: Union[Location, "Range"],
    ) -> bool:
        if isinstance(location_or_range, Location):
            return self.begin <= location_or_range <= self.end

        if isinstance(location_or_range, Range):
            return self.begin <= location_or_range.begin and location_or_range.end <= self.end

        assert False, location_or_range  # pragma: no cover

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @cached_property
    def _string(self) -> str:
        return "{} -> {}".format(self.begin, self.end)
