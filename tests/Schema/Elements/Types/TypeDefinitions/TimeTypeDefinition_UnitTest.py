# ----------------------------------------------------------------------
# |
# |  TimeTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-16 10:45:16
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for TimeTypeDefinition.py"""

from datetime import datetime, time
from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.TimeTypeDefinition import *


# ----------------------------------------------------------------------
def test_DisplayType():
    assert TimeTypeDefinition(Mock()).display_type == "Time"


# ----------------------------------------------------------------------
def test_ToPythonInstance():
    now = datetime.now().time()

    assert TimeTypeDefinition(Mock()).ToPythonInstance(now) is now
