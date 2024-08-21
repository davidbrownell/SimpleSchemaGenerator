# ----------------------------------------------------------------------
# |
# |  DateTimeTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-14 15:01:00
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for DateTimeTypeDefinition.py."""

from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.DateTimeTypeDefinition import *


# ----------------------------------------------------------------------
def test_DisplayType():
    assert DateTimeTypeDefinition(Mock()).display_type == "DateTime"


# ----------------------------------------------------------------------
def test_PythonType():
    now = datetime.now()

    assert DateTimeTypeDefinition(Mock()).ToPythonInstance(now) is now
