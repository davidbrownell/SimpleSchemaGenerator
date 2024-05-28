# ----------------------------------------------------------------------
# |
# |  TypeFactories.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-05-27 15:13:33
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the ReferenceTypeFactory and StructureTypeFactory objects"""

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

from dbrownell_Common.Types import extension  # type: ignore[import-untyped]

from ...ANTLR.Grammar.Elements.Statements.ParseItemStatement import ParseItemStatement  # type: ignore[import-untyped]
from ...ANTLR.Grammar.Elements.Statements.ParseStructureStatement import ParseStructureStatement  # type: ignore[import-untyped]

if TYPE_CHECKING:  # pragma: no cover
    from .Namespace import Namespace


# ----------------------------------------------------------------------
class _TypeFactory(ABC):
    """Abstract base class for all type factories"""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        statement: ParseItemStatement | ParseStructureStatement,
        active_namespace: "Namespace",
    ) -> None:
        pass  # BugBug


# ----------------------------------------------------------------------
class StructureTypeFactory(_TypeFactory):
    """Factory for creating StructureTypes"""

    pass  # BugBug


# ----------------------------------------------------------------------
class ReferenceTypeFactory(_TypeFactory):
    """Factory for creating ReferenceTypes"""

    pass  # BugBug
