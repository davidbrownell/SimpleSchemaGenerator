# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 David Brownell
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for EntryPoint.py"""

from typer.testing import CliRunner

from SimpleSchemaGenerator import __version__
from SimpleSchemaGenerator.EntryPoint import app


# ----------------------------------------------------------------------
def test_Version():
    result = CliRunner().invoke(app, ["Version"])
    assert result.exit_code == 0
    assert result.stdout == __version__
