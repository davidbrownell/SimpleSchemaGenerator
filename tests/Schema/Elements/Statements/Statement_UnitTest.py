# ----------------------------------------------------------------------
# |
# |  Statement_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-13 11:21:32
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Statement.py."""

from unittest.mock import Mock

from SimpleSchemaGenerator.Schema.Elements.Statements.Statement import Statement


# ----------------------------------------------------------------------
def test_Standard():
    region = Mock()

    s = Statement(region)

    assert s.region is region
