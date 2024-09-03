"""Build tasks for this python project."""

import sys

from pathlib import Path
from typing import Annotated

import typer

from dbrownell_Common import PathEx
from dbrownell_Common.Streams.DoneManager import DoneManager, Flags as DoneManagerFlags
from dbrownell_Common import SubprocessEx
from dbrownell_DevTools.RepoBuildTools import Python as RepoBuildTools
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
this_dir = PathEx.EnsureDir(Path(__file__).parent)
src_dir = PathEx.EnsureDir(this_dir / "src")
package_dir = PathEx.EnsureDir(src_dir / "SimpleSchemaGenerator")


# ----------------------------------------------------------------------
Black = RepoBuildTools.BlackFuncFactory(this_dir, app)

Pylint = RepoBuildTools.PylintFuncFactory(
    package_dir,
    app,
    default_min_score=9.5,
)

Pytest = RepoBuildTools.PytestFuncFactory(
    this_dir,
    package_dir.name,
    app,
    default_min_coverage=90.0,
)

UpdateVersion = RepoBuildTools.UpdateVersionFuncFactory(
    src_dir,
    PathEx.EnsureFile(package_dir / "__init__.py"),
    app,
)

Package = RepoBuildTools.PackageFuncFactory(this_dir, app)
Publish = RepoBuildTools.PublishFuncFactory(this_dir, app)

BuildBinary = RepoBuildTools.BuildBinaryFuncFactory(
    this_dir,
    PathEx.EnsureFile(src_dir / "BuildBinary.py"),
    app,
)

CreateDockerImage = RepoBuildTools.CreateDockerImageFuncFactory(
    this_dir,
    app,
)


# ----------------------------------------------------------------------
@app.command("build_antlr_grammar", no_args_is_help=False)
def BuildAntlrGrammar(
    verbose: Annotated[
        bool,
        typer.Option("--verbose", help="Write verbose information to the terminal."),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option("--debug", help="Write debug information to the terminal."),
    ] = False,
):
    with DoneManager.CreateCommandLine(
        flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        with dm.Nested("Generating sources...") as generate_dm:
            working_dir = PathEx.EnsureDir(
                Path(__file__).parent
                / "src"
                / "SimpleSchemaGenerator"
                / "Schema"
                / "Parse"
                / "ANTLR"
                / "Grammar"
            )
            output_dir = (working_dir / ".." / "GeneratedCode").resolve()

            # Run the jar
            command_line = 'java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -o "{output_dir}" -no-listener -visitor "{input_file}"'.format(
                output_dir=output_dir,
                input_file=PathEx.EnsureFile(working_dir / "SimpleSchema.g4"),
            )

            generate_dm.WriteVerbose(f"Command Line: {command_line}\n\n")

            with generate_dm.YieldStream() as stream:
                generate_dm.result = SubprocessEx.Stream(command_line, stream, cwd=working_dir)

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
    sys.exit(app())
