# ----------------------------------------------------------------------
# |
# |  NoneExpression.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 15:07:55
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the NoneExpression object."""

from dataclasses import dataclass
from typing import ClassVar

from .Expression import Expression


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class NoneExpression(Expression):
    """None value"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "None"

    value: None = None
