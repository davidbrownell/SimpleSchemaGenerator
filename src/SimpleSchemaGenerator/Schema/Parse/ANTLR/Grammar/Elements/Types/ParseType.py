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

from dbrownell_Common.Types import override

from SimpleSchemaGenerator.Schema.Elements.Common.Cardinality import Cardinality
from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element
from SimpleSchemaGenerator.Schema.Elements.Common.Metadata import Metadata
from SimpleSchemaGenerator.Schema.Elements.Types.Impl.TypeImpl import TypeImpl


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ParseType(TypeImpl):
    """Temporary type generated during parsing and replaced during subsequent steps"""

    # ----------------------------------------------------------------------
    cardinality: Cardinality
    unresolved_metadata: Metadata | None

    # ----------------------------------------------------------------------
    @override
    def ToPythonInstance(self, *args, **kwargs) -> object:  # noqa: ARG002
        raise Exception(  # noqa: TRY003
            "This should never be invoked on ParseType instances."  # noqa: EM101
        )  # pragma: no cover

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from super()._GenerateAcceptDetails()

        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "cardinality", self.cardinality
        )

        if self.unresolved_metadata is not None:
            yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
                "unresolved_metadata", self.unresolved_metadata
            )
