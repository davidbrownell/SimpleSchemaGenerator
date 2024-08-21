# ----------------------------------------------------------------------
# |
# |  DateTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-14 15:03:44
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for DateTypeDefinition.py."""

from datetime import datetime
from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.DateTypeDefinition import *


# ----------------------------------------------------------------------
def test_DisplayType():
    assert DateTypeDefinition(Mock()).display_type == "Date"


# ----------------------------------------------------------------------
def test_PythonValue():
    date = datetime.now().date()

    assert DateTypeDefinition(Mock()).ToPythonInstance(date) is date
