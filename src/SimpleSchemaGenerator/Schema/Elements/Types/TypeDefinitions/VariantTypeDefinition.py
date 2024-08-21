# ----------------------------------------------------------------------
# |
# |  VariantTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-19 11:40:38
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the VariantTypeDefinition object."""

import textwrap

from dataclasses import dataclass, field
from typing import Any, cast, ClassVar, Type as PythonType, TYPE_CHECKING

from dbrownell_Common import TextwrapEx  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from .TypeDefinition import TypeDefinition
from ...Common.Element import Element
from ...Expressions.Expression import Expression
from .....Common.Error import Error
from ..... import Errors

if TYPE_CHECKING:
    from ..Type import Type  # pragma: no cover


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class VariantTypeDefinition(TypeDefinition):
    """A Variant type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Variant"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[PythonType, ...]] = (object,)

    types: list["Type"]

    has_child_cardinality: bool = field(init=False, compare=False)

    # ----------------------------------------------------------------------
    def __post_init__(self):
        if len(self.types) < 2:
            raise Errors.SimpleSchemaGeneratorException(
                Errors.VariantTypedefNotEnoughTypes.Create(self.region)
            )

        has_child_cardinality = False

        for the_type in self.types:
            with the_type.Resolve() as resolved_type:
                if isinstance(resolved_type.type, VariantTypeDefinition):
                    raise Errors.SimpleSchemaGeneratorException(
                        Errors.VariantTypedefNested.Create(the_type.type.region)
                    )

            if not the_type.cardinality.is_single:
                has_child_cardinality = True

        object.__setattr__(self, "has_child_cardinality", has_child_cardinality)

    # ----------------------------------------------------------------------
    def ToPythonInstance(
        self,
        expression_or_value: Expression | Any,
    ) -> Any:
        # ----------------------------------------------------------------------
        def Impl(
            value: Any,
        ) -> Any:
            exceptions: list[Exception] = []

            for sub_type in self.types:
                try:
                    return sub_type.ToPythonInstance(value)
                except Exception as ex:
                    exceptions.append(ex)

            raise Exception(
                Errors.variant_typedef_invalid_value.format(
                    python_type=type(value).__name__,
                    type=self.display_type,
                    additional_info=TextwrapEx.Indent(
                        "".join(
                            textwrap.dedent(
                                """\
                                {}
                                    {}
                                """,
                            ).format(
                                sub_type.display_type,
                                TextwrapEx.Indent(
                                    str(ex),
                                    4,
                                    skip_first_line=True,
                                ).rstrip(),
                            )
                            for sub_type, ex in zip(self.types, exceptions)
                        ).rstrip(),
                        8,
                        skip_first_line=True,
                    ),
                ),
            )

        # ----------------------------------------------------------------------

        if isinstance(expression_or_value, Expression):
            try:
                return Impl(expression_or_value.value)
            except Exception as ex:
                raise Errors.SimpleSchemaGeneratorException(
                    Error.Create(
                        ex,
                        expression_or_value.region,
                        include_callstack=False,
                    ),
                )

        return Impl(expression_or_value)

    # ----------------------------------------------------------------------
    def ToPythonInstanceOverride(
        self,
        type: "Type",
        expression_or_value: Expression | Any,
    ) -> Any:
        if self.has_child_cardinality:
            return self.ToPythonInstance(expression_or_value)

        return type.ToPythonInstanceImpl(expression_or_value)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        display_values: list[str] = []

        for child_type in self.types:
            child_display = child_type.display_type

            if "{" in child_display and not (
                child_display.startswith("<") and child_display.endswith(">")
            ):
                child_display = f"<{child_display}>"

            display_values.append(child_display)

        return "({})".format(" | ".join(display_values))

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(self, *args, **kwargs):
        raise Exception("This will never be called for variant types.")  # pragma: no cover

    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from super(VariantTypeDefinition, self)._GenerateAcceptDetails()

        yield Element._GenerateAcceptDetailsItem(  # pylint: disable=protected-access
            "types",
            cast(list[Element], self.types),
        )
