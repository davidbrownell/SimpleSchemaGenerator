# ----------------------------------------------------------------------
# |
# |  StructureTypeDefinition_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-19 09:42:03
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit test for StructureTypeDefinition.py"""

import sys

from pathlib import Path
from unittest.mock import Mock

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.StructureTypeDefinition import *

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_Standard():
    region = Mock()
    structure = Mock()
    structure.name.value = "MyStructure"

    td = StructureTypeDefinition(region, structure)

    assert td.NAME == "Structure"
    assert td.SUPPORTED_PYTHON_TYPES == (object,)
    assert td.display_type == "MyStructure"
    assert td.structure is structure

    assert TestElementVisitor(td) == [
        td,
        ("structure", structure),
    ]
