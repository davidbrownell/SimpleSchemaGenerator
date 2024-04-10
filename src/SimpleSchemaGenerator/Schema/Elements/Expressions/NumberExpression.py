# ----------------------------------------------------------------------
# |
# |  NumberExpression.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 15:08:38
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the NumberExpression object."""

from dataclasses import dataclass
from typing import ClassVar

from .Expression import Expression


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class NumberExpression(Expression):
    """Number value"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Number"

    value: float
