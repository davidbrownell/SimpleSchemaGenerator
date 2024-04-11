# ----------------------------------------------------------------------
# |
# |  Build.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 18:54:15
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Generates the ANTLR code"""

from pathlib import Path
from typing import Annotated

import typer

from dbrownell_Common import PathEx
from dbrownell_Common.Streams.DoneManager import DoneManager, Flags as DoneManagerFlags
from dbrownell_Common import SubprocessEx
from typer.core import TyperGroup


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
@app.command("EntryPoint", help=__doc__, no_args_is_help=False)
def EntryPoi(
    verbose: Annotated[
        bool,
        typer.Option("--verbose", help="Write verbose information to the terminal."),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option("--debug", help="Write debug information to the terminal."),
    ] = False,
) -> None:
    with DoneManager.CreateCommandLine(
        flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        with dm.Nested("Generating source...") as generate_dm:
            this_dir = Path(__file__).parent
            output_dir = (this_dir / ".." / "GeneratedCode").resolve()

            # Run the jar
            command_line = 'java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -o "{output_dir}" -no-listener -visitor "{input_file}"'.format(
                output_dir=output_dir,
                input_file=PathEx.EnsureFile(this_dir / "SimpleSchema.g4"),
            )

            generate_dm.WriteVerbose(f"Command Line: {command_line}\n\n")

            with generate_dm.YieldStream() as stream:
                generate_dm.result = SubprocessEx.Stream(command_line, stream)

            if generate_dm.result != 0:
                return

            # Create the init file (if necessary)
            init_filename = output_dir / "__init__.py"

            if not init_filename.is_file():
                with init_filename.open("w") as f:
                    pass


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()
