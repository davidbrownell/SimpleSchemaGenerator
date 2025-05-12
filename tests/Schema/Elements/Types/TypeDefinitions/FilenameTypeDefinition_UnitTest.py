# ----------------------------------------------------------------------
# |
# |  FilenameTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-16 09:04:40
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit test for FilenameTypeDefinition.py."""

import re

from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.FilenameTypeDefinition import *


# ----------------------------------------------------------------------
def test_DisplayType():
    assert FilenameTypeDefinition(Mock(), ensure_exists=False, match_any=False).display_type == "Filename"
    assert FilenameTypeDefinition(Mock(), ensure_exists=True, match_any=False).display_type == "Filename!"
    assert FilenameTypeDefinition(Mock(), ensure_exists=True, match_any=True).display_type == "Filename!^"

    with pytest.raises(
        ValueError,
        match=re.escape("'match_any' should only be set when 'ensure_exists' is set as well."),
    ):
        FilenameTypeDefinition(Mock(), ensure_exists=False, match_any=True)


# ----------------------------------------------------------------------
def test_ToPythonInstance():
    filename = Path(__file__)
    directory = filename.parent
    does_not_exist = directory / "does_not_exist"

    td = FilenameTypeDefinition(Mock(), ensure_exists=False, match_any=False)
    assert td.ToPythonInstance(filename) is filename
    assert td.ToPythonInstance(directory) is directory
    assert td.ToPythonInstance(does_not_exist) is does_not_exist

    td = FilenameTypeDefinition(Mock(), ensure_exists=True, match_any=False)
    assert td.ToPythonInstance(filename) is filename

    with pytest.raises(
        Exception,
        match=re.escape(f"'{directory}' is not a valid filename."),
    ):
        td.ToPythonInstance(directory)

    with pytest.raises(
        Exception,
        match=re.escape(f"'{does_not_exist}' is not a valid filename."),
    ):
        td.ToPythonInstance(does_not_exist)

    td = FilenameTypeDefinition(Mock(), ensure_exists=True, match_any=True)

    assert td.ToPythonInstance(filename) is filename
    assert td.ToPythonInstance(directory) is directory

    with pytest.raises(
        Exception,
        match=re.escape(f"'{does_not_exist}' is not a valid filename or directory."),
    ):
        td.ToPythonInstance(does_not_exist)
