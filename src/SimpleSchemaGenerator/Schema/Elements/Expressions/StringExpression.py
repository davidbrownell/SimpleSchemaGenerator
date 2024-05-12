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
from enum import auto, Enum
from typing import ClassVar

from .Expression import Expression


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class StringExpression(Expression):
    """String value"""

    # ----------------------------------------------------------------------
    class QuoteType(Enum):
        """Type of quote used to define a string"""

        Single = auto()
        Double = auto()
        TripleSingle = auto()
        TripleDouble = auto()

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "String"

    value: str
    quote_type: "StringExpression.QuoteType"
