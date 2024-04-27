# ----------------------------------------------------------------------
# |
# |  Statement.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-13 11:20:15
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
# """Contains the Statement object."""

from dataclasses import dataclass

from ..Common.Element import Element


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Statement(Element):
    """Abstract base class for all statements"""
