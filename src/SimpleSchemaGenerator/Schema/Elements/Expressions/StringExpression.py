# ----------------------------------------------------------------------
# |
# |  StringExpression.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 15:09:56
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the StringExpression object."""

from dataclasses import dataclass
from typing import ClassVar

from .Expression import Expression


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class StringExpression(Expression):
    """String value"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "String"

    value: str
