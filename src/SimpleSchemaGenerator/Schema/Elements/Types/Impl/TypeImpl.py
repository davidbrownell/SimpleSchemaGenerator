# ----------------------------------------------------------------------
# |
# |  TypeImpl.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-12 20:12:04
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the Type object."""

from abc import abstractmethod
from dataclasses import dataclass
from functools import cached_property

from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element
from SimpleSchemaGenerator.Schema.Elements.Common.UniqueNameTrait import UniqueNameTrait
from SimpleSchemaGenerator.Schema.Elements.Expressions.Expression import Expression


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class TypeImpl(UniqueNameTrait, Element):
    """Abstract base class for IntrinsicType and ComplexType"""

    # ----------------------------------------------------------------------
    @cached_property
    def display_type(self) -> str:
        return self._display_type

    # ----------------------------------------------------------------------
    @abstractmethod
    def ToPythonInstance(
        self,
        expression_or_value: Expression | object,
    ) -> object:
        raise Exception("Abstract method")  # pragma: no cover  # noqa: EM101, TRY003

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @property
    @abstractmethod
    def _display_type(self) -> str:
        raise Exception("Abstract property")  # pragma: no cover  # noqa: EM101, TRY003
