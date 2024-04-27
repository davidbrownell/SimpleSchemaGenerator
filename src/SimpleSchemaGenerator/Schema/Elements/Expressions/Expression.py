# ----------------------------------------------------------------------
# |
# |  Expression.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 08:16:15
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Expression object"""

from dataclasses import dataclass
from typing import Any, ClassVar

from ..Common.Element import Element


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Expression(Element):
    """Abstract base class for all expressions"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = ""

    value: Any

    # ----------------------------------------------------------------------
    def __post_init__(self):
        if self.NAME == "":
            raise Exception(f"NAME must be defined for '{self.__class__.__name__}'.")
