# ----------------------------------------------------------------------
# |
# |  ParseType.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-12 19:58:08
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the ParseType object."""

from dataclasses import dataclass
from typing import Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from ......Elements.Common.Cardinality import Cardinality
from ......Elements.Common.Element import Element
from ......Elements.Common.Metadata import Metadata
from ......Elements.Types.Impl.TypeImpl import TypeImpl


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ParseType(TypeImpl):
    """Temporary type generated during parsing and replaced during subsequent steps"""

    # ----------------------------------------------------------------------
    cardinality: Cardinality
    unresolved_metadata: Optional[Metadata]

    # ----------------------------------------------------------------------
    @override
    def ToPythonInstance(self, *args, **kwargs):
        raise Exception("This should never be invoked on ParseType instances.")  # pragma: no cover

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from super(ParseType, self)._GenerateAcceptDetails()

        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "cardinality", self.cardinality
        )

        if self.unresolved_metadata is not None:
            yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
                "unresolved_metadata", self.unresolved_metadata
            )
