# ----------------------------------------------------------------------
# |
# |  DirectoryTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-14 15:09:41
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for DirectoryTypeDefinition.py."""

import re

from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.DirectoryTypeDefinition import *


# ----------------------------------------------------------------------
def test_PythonTypeEnsureExists():
    this_dir = Path(__file__).parent

    assert DirectoryTypeDefinition(Mock(), ensure_exists=True).ToPythonInstance(this_dir) is this_dir

    bad_dir = this_dir / "does_not_exist"

    with pytest.raises(
        Exception,
        match=re.escape(f"'{bad_dir}' is not a valid directory."),
    ):
        DirectoryTypeDefinition(Mock(), ensure_exists=True).ToPythonInstance(bad_dir)

    bad_file = Path(__file__)

    with pytest.raises(
        Exception,
        match=re.escape(f"'{bad_file}' is not a valid directory."),
    ):
        DirectoryTypeDefinition(Mock(), ensure_exists=True).ToPythonInstance(bad_file)


# ----------------------------------------------------------------------
def test_PythonTypeNoEnsureExists():
    this_dir = Path(__file__).parent
    bad_dir = this_dir / "does_not_exist"
    bad_file = Path(__file__)

    assert DirectoryTypeDefinition(Mock(), ensure_exists=False).ToPythonInstance(this_dir) is this_dir
    assert DirectoryTypeDefinition(Mock(), ensure_exists=False).ToPythonInstance(bad_dir) is bad_dir
    assert DirectoryTypeDefinition(Mock(), ensure_exists=False).ToPythonInstance(bad_file) is bad_file


# ----------------------------------------------------------------------
def test_DisplayType():
    assert DirectoryTypeDefinition(Mock(), ensure_exists=True).display_type == "Directory!"
    assert DirectoryTypeDefinition(Mock(), ensure_exists=False).display_type == "Directory"
