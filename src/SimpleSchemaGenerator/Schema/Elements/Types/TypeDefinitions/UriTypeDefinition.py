# ----------------------------------------------------------------------
# |
# |  UriTypeDefinition.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-16 10:44:50
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the UriTypeDefinition object."""

import re

from dataclasses import dataclass
from functools import cached_property
from re import Pattern
from typing import ClassVar

from dbrownell_Common.Types import override

from .TypeDefinition import TypeDefinition
from SimpleSchemaGenerator import Errors


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Uri:
    """Contains the components of a uri."""

    # ----------------------------------------------------------------------
    # |
    # |  Public Types
    # |
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class Authority:
        """The authority portion of a uri."""

        # ----------------------------------------------------------------------
        slashes: str
        username: str | None
        host: str
        port: int | None

        # ----------------------------------------------------------------------
        def __str__(self) -> str:
            return self._string

        # ----------------------------------------------------------------------
        @cached_property
        def _string(self) -> str:
            parts: list[str] = [
                self.slashes,
            ]

            if self.username:
                parts += [self.username, "@"]

            parts.append(self.host)

            if self.port:
                parts += [":", str(self.port)]

            parts.append("/")

            return "".join(parts)

    # ----------------------------------------------------------------------
    # |
    # |  Public Data
    # |
    # ----------------------------------------------------------------------
    scheme: str
    authority: Authority | None
    path: str | None
    query: str | None
    fragment: str | None

    # ----------------------------------------------------------------------
    # |
    # |  Public Methods
    # |
    # ----------------------------------------------------------------------
    def __str__(self) -> str:
        return self._string

    # ----------------------------------------------------------------------
    # |
    # |  Private Properties
    # |
    # ----------------------------------------------------------------------
    @cached_property
    def _string(self) -> str:
        parts: list[str] = [self.scheme, ":"]

        if self.authority:
            parts.append(str(self.authority))

        if self.path:
            parts.append(self.path)

        if self.query:
            parts += ["?", self.query]

        if self.fragment:
            parts += ["#", self.fragment]

        return "".join(parts)


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class UriTypeDefinition(TypeDefinition):
    """A Uri type"""

    # ----------------------------------------------------------------------
    NAME: ClassVar[str] = "Uri"
    SUPPORTED_PYTHON_TYPES: ClassVar[tuple[type, ...]] = (str, Uri)

    _VALIDATION_EXPRESSION: ClassVar[Pattern] = re.compile(
        r"""(?#
            Start of String                 )^(?#
            Scheme                          )(?P<scheme>[a-z]+):(?#
            Authority Begin                 )(?:(?#
                Slashes                     )(?P<slashes>///?)(?#
                User Info Begin             )(?:(?#
                    Username                )(?P<username>[^@/]+?)(?#
                    @                       )@(?#
                User Info End               ))?(?#
                Host                        )(?P<host>[^:/]+?)(?#
                Port Begin                  )(?:(?#
                    :                       ):(?#
                    Port                    )(?P<port>\d+)(?#
                Port End                    ))?(?#
            Authority End                   ))?(?#
            Path Begin                      )(?:(?#
                Slash                       )/(?#
                Path                        )(?P<path>[^:?\#]*?)(?#
            Path End                        ))?(?#
            Query Begin                     )(?:(?#
                ?                           )\?(?#
                Query                       )(?P<query>[^#]+?)(?#
            Query End                       ))?(?#
            Fragment Begin                  )(?:(?#
                #                           )\#(?#
                Fragment                    )(?P<fragment>.+?)(?#
            Fragment End                    ))?(?#
            End of String                   )$(?#
        )""",
    )

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _ToPythonInstanceImpl(
        self,
        value: str | Uri,
    ) -> Uri:
        if isinstance(value, Uri):
            return value

        match = self.__class__._VALIDATION_EXPRESSION.match(  # noqa: SLF001
            value
        )
        if not match:
            raise Exception(Errors.uri_typedef_invalid_value.format(value=value))

        authority: Uri.Authority | None = None

        if match.group("slashes"):
            port = match.group("port")
            port = int(port) if port else None

            authority = Uri.Authority(
                match.group("slashes"),
                match.group("username") or None,
                match.group("host"),
                port,
            )

        return Uri(
            match.group("scheme"),
            authority,
            match.group("path") or None,
            match.group("query") or None,
            match.group("fragment") or None,
        )
