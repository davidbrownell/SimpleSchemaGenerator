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
from typing import cast, ClassVar, NoReturn, TYPE_CHECKING

from dbrownell_Common import TextwrapEx
from dbrownell_Common.Types import override

from .TypeDefinition import TypeDefinition
from SimpleSchemaGenerator.Schema.Elements.Common.Element import Element
from SimpleSchemaGenerator.Schema.Elements.Expressions.Expression import Expression
from SimpleSchemaGenerator.Common.Error import Error
from SimpleSchemaGenerator import Errors

if TYPE_CHECKING:
    from SimpleSchemaGenerator.Schema.Elements.Types.Type import Type  # pragma: no cover


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class VariantTypeDefinition(TypeDefinition):
    """A Variant type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Variant"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (object,)

    types: list["Type"]

    has_child_cardinality: bool = field(init=False, compare=False)

    # ----------------------------------------------------------------------
    def __post_init__(self) -> None:
        if len(self.types) < 2:  # noqa: PLR2004
            raise Errors.SimpleSchemaGeneratorError(Errors.VariantTypedefNotEnoughTypes.Create(self.region))

        has_child_cardinality = False

        for the_type in self.types:
            with the_type.Resolve() as resolved_type:
                if isinstance(resolved_type.type, VariantTypeDefinition):
                    raise Errors.SimpleSchemaGeneratorError(
                        Errors.VariantTypedefNested.Create(the_type.type.region)
                    )

            if not the_type.cardinality.is_single:
                has_child_cardinality = True

        object.__setattr__(self, "has_child_cardinality", has_child_cardinality)

    # ----------------------------------------------------------------------
    def ToPythonInstance(
        self,
        expression_or_value: Expression | object,
    ) -> object:
        # ----------------------------------------------------------------------
        def Impl(
            value: object,
        ) -> object:
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
                            for sub_type, ex in zip(self.types, exceptions, strict=True)
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
                raise Errors.SimpleSchemaGeneratorError(
                    Error.Create(
                        ex,
                        expression_or_value.region,
                        include_callstack=False,
                    ),
                ) from ex

        return Impl(expression_or_value)

    # ----------------------------------------------------------------------
    def ToPythonInstanceOverride(
        self,
        the_type: "Type",
        expression_or_value: Expression | object,
    ) -> object:
        if self.has_child_cardinality:
            return self.ToPythonInstance(expression_or_value)

        return the_type.ToPythonInstanceImpl(expression_or_value)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @property
    @override
    def _display_type(self) -> str:
        display_values: list[str] = []

        for child_type in self.types:
            child_display = child_type.display_type

            if "{" in child_display and not (child_display.startswith("<") and child_display.endswith(">")):
                child_display = f"<{child_display}>"

            display_values.append(child_display)

        return "({})".format(" | ".join(display_values))

    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(self, *args, **kwargs) -> NoReturn:  # noqa: ARG002
        raise Exception(  # noqa: TRY003
            "This will never be called for variant types."  # noqa: EM101
        )  # pragma: no cover

    # ----------------------------------------------------------------------
    @override
    def _GenerateAcceptDetails(self) -> Element._GenerateAcceptDetailsResultType:
        yield from super()._GenerateAcceptDetails()

        yield Element._GenerateAcceptDetailsItem(  # noqa: SLF001
            "types",
            cast(list[Element], self.types),
        )
