# ----------------------------------------------------------------------
# |
# |  GuidTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-16 09:15:43
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for GuidTypeDefinition.py."""

import uuid

from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.GuidTypeDefinition import *


# ----------------------------------------------------------------------
def test_DisplayType():
    assert GuidTypeDefinition(Mock()).display_type == "Guid"


# ----------------------------------------------------------------------
def test_PythonValue():
    guid = uuid.uuid4()

    assert GuidTypeDefinition(Mock()).ToPythonInstance(guid) == guid
