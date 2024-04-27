# ----------------------------------------------------------------------
# |
# |  TerminalsElement_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 09:05:54
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for TerminalsElement.py"""

from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Common.TerminalElement import TerminalElement


# ----------------------------------------------------------------------
def test_Int():
    region_mock = Mock()
    e = TerminalElement[int](region_mock, 10)

    assert e.region is region_mock
    assert e.value == 10


# ----------------------------------------------------------------------
def test_String():
    region_mock = Mock()
    e = TerminalElement[str](region_mock, "test")

    assert e.region is region_mock
    assert e.value == "test"
