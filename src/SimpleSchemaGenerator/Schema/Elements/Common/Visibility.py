# ----------------------------------------------------------------------
# |
# |  Visibility.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-12 19:09:22
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Visibility objects"""

from dataclasses import dataclass
from enum import auto, Enum

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TerminalElement import Element, TerminalElement


# ----------------------------------------------------------------------
class Visibility(Enum):
    """Access restriction for an Element"""

    Public = auto()
    Protected = auto()
    Private = auto()


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class VisibilityTrait(Element):
    """Trait for Elements that have a visibility attribute"""

    visibility: TerminalElement[Visibility]

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "visibility",
            self.visibility,
        )
