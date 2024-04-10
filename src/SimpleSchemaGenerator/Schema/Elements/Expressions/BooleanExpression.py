# ----------------------------------------------------------------------
# |
# |  BooleanExpression.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 15:03:29
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the BooleanExpression object."""

from dataclasses import dataclass
from typing import ClassVar

from .Expression import Expression


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class BooleanExpression(Expression):
    """Boolean value"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Boolean"

    value: bool
