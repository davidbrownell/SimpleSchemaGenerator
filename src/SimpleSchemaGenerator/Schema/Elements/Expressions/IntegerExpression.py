# ----------------------------------------------------------------------
# |
# |  IntegerExpression.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 08:18:57
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the IntegerExpression object"""

from dataclasses import dataclass
from typing import ClassVar

from .Expression import Expression


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class IntegerExpression(Expression):
    """Integer value"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Integer"

    value: int
