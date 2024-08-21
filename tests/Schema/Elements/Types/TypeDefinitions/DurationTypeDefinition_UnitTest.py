# ----------------------------------------------------------------------
# |
# |  DurationTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-14 15:20:02
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for DurationTypeDefinition.py."""

from datetime import timedelta
from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.DurationTypeDefinition import *


# ----------------------------------------------------------------------
def test_DisplayType():
    assert DurationTypeDefinition(Mock()).display_type == "Duration"


# ----------------------------------------------------------------------
def test_PythonValue():
    duration = timedelta(seconds=123)

    assert DurationTypeDefinition(Mock()).ToPythonInstance(duration) == duration
