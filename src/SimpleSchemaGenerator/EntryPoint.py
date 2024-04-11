# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 David Brownell
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""This file serves as an example of how to create scripts that can be invoked from the command line once the package is installed."""

import sys

import typer

from typer.core import TyperGroup  # type: ignore [import-untyped]

from SimpleSchemaGenerator import __version__


# ----------------------------------------------------------------------
class NaturalOrderGrouper(TyperGroup):
    # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def list_commands(self, *args, **kwargs):  # pylint: disable=unused-argument
        return self.commands.keys()


# ----------------------------------------------------------------------
app = typer.Typer(
    cls=NaturalOrderGrouper,
    help=__doc__,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False,
)


# ----------------------------------------------------------------------
@app.command("EntryPoint")
def EntryPoint(
    x: int,
    y: int,
) -> None:
    pass  # TODO: Remove this


# ----------------------------------------------------------------------
@app.command("Version")
def Version() -> None:
    """Prints the version of the package."""

    sys.stdout.write(__version__)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()  # pragma: no cover
