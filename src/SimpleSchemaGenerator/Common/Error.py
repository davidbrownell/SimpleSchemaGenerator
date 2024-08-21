# ----------------------------------------------------------------------
# |
# |  Error.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-09 14:13:25
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains functionality associated with errors and Exceptions."""

import re
import textwrap
import traceback

from dataclasses import dataclass, field, InitVar, make_dataclass
from enum import Enum
from functools import singledispatch, singledispatchmethod
from io import StringIO
from pathlib import Path
from typing import Optional, Type as PythonType

from dbrownell_Common import TextwrapEx  # type: ignore[import-untyped]

from .Location import Location
from .Region import Region


# ----------------------------------------------------------------------
# |
# |  Public Types
# |
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Error:
    """Base class for all errors generated within SimpleSchemaGenerator."""

    # ----------------------------------------------------------------------
    message: str

    region_or_regions: InitVar[Region | list[Region]]
    regions: list[Region] = field(init=False)

    # ----------------------------------------------------------------------
    def __post_init__(
        self,
        region_or_regions: Region | list[Region],
    ) -> None:
        regions: list[Region] = []

        if isinstance(region_or_regions, list):
            regions = region_or_regions
        else:
            regions.append(region_or_regions)

        object.__setattr__(self, "regions", regions)

    # ----------------------------------------------------------------------
    @singledispatchmethod
    @classmethod
    def Create(cls, *args, **kwargs) -> "Error":
        return cls(*args, **kwargs)

    # ----------------------------------------------------------------------
    @Create.register
    @classmethod
    def _(
        cls,
        ex: Exception,
        region: Optional[Region] = None,
        *,
        include_callstack: bool = True,
    ):  # -> "Error":
        regions: list[Region] = []

        if include_callstack:
            # I haven't been able to find a reliable way to get the exception's callstack so it is
            # being parsed manually here. There has got to be a better way to do this.
            sink = StringIO()

            traceback.print_exception(ex, file=sink)
            sink_str = sink.getvalue()

            regex = re.compile(
                r"^\s*File \"(?P<filename>.+?)\", line (?P<line>\d+),.+$", re.MULTILINE
            )

            for line in sink_str.splitlines():
                match = regex.match(line)
                if not match:
                    continue

                line_number = int(match.group("line"))

                regions.append(
                    Region(
                        Path(match.group("filename")),
                        Location(line_number, 1),
                        Location(line_number, 1),
                    ),
                )

            regions.reverse()

        if region is not None:
            regions.insert(0, region)

        instance = cls(str(ex), regions)

        object.__setattr__(instance, "ex", ex)

        return instance

    # ----------------------------------------------------------------------
    def __str__(self) -> str:
        if len(self.regions) == 1 and "\n" not in self.message:
            return "{} ({})".format(self.message, self.regions[0])

        return textwrap.dedent(
            """\
            {}

            {}
            """,
        ).format(
            self.message.rstrip(),
            "\n".join("    - {}".format(region) for region in self.regions),
        )


# ----------------------------------------------------------------------
@dataclass
class SimpleSchemaGeneratorException(Exception):
    """Exception raised by functionality in SimpleSchemaGenerator."""

    # ----------------------------------------------------------------------
    error: InitVar[Error]
    errors: list[Error] = field(init=False)  # TODO: Will we ever initialize with multiple errors?

    # ----------------------------------------------------------------------
    def __post_init__(
        self,
        error: Error,
    ) -> None:
        super(SimpleSchemaGeneratorException, self).__init__(str(error))

        object.__setattr__(
            self,
            "errors",
            [
                error,
            ],
        )

    # ----------------------------------------------------------------------
    def __str__(self) -> str:
        return str(self.errors[0])


# ----------------------------------------------------------------------
# |
# |  Public Functions
# |
# ----------------------------------------------------------------------
def CreateErrorType(
    message_template: str,
    **args: PythonType,
) -> PythonType[Error]:
    dynamic_fields_class = make_dataclass(
        "DynamicFields",
        args.items(),
        bases=(Error,),
        frozen=True,
    )

    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class NewError(
        dynamic_fields_class  # type: ignore[valid-type]
    ):  # pylint: disable=missing-class-docstring
        # ----------------------------------------------------------------------
        message: str = field(init=False)

        # ----------------------------------------------------------------------
        def __post_init__(self, *args, **kwargs):
            super(NewError, self).__post_init__(*args, **kwargs)

            object.__setattr__(
                self,
                "message",
                message_template.format(
                    **{k: _ArgToString(v) for k, v in self.__dict__.items()},
                ),
            )

    # ----------------------------------------------------------------------

    return NewError


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
@singledispatch
def _ArgToString(value) -> str:
    return str(value)


# ----------------------------------------------------------------------
@_ArgToString.register
def _(
    value: str,
) -> str:
    return value


# ----------------------------------------------------------------------
@_ArgToString.register
def _(
    value: list,
) -> str:
    return "[{}]".format(", ".join("'{}'".format(_ArgToString(v)) for v in value))


# ----------------------------------------------------------------------
@_ArgToString.register
def _(
    value: Enum,
) -> str:
    return value.name
