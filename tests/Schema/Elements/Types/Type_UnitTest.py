# ----------------------------------------------------------------------
# |
# |  Type_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-12 20:15:22
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Type.py"""

import re

from dataclasses import dataclass
from typing import ClassVar
from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Schema.Elements.Types.Type import Type


# ----------------------------------------------------------------------
def test_Standard():
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class MyType(Type):
        # ----------------------------------------------------------------------
        NAME: ClassVar[str] = "MyType"

    # ----------------------------------------------------------------------

    region_mock = Mock()

    t = MyType(region_mock)

    assert t.region is region_mock
    assert t.display_type == "MyType"


# ----------------------------------------------------------------------
def test_ErrorNoName():
    with pytest.raises(
        Exception,
        match=re.escape("NAME must be defined for 'Type'."),
    ):
        Type(Mock())
