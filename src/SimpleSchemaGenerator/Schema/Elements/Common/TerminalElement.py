# ----------------------------------------------------------------------
# |
# |  TerminalElement.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 09:04:40
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the TerminalElement object"""

from dataclasses import dataclass
from typing import Generic, TypeVar

from .Element import Element


# ----------------------------------------------------------------------
TerminalElementType = TypeVar("TerminalElementType")  # pylint: disable=invalid-name


@dataclass(frozen=True)
class TerminalElement(Generic[TerminalElementType], Element):
    """Element with a single value member"""

    # ----------------------------------------------------------------------
    value: TerminalElementType
