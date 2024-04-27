# ----------------------------------------------------------------------
# |
# |  UniqueNameTrait_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-12 20:01:29
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for UniqueNameTrait.py."""

from SimpleSchemaGenerator.Schema.Elements.Common.UniqueNameTrait import UniqueNameTrait


# ----------------------------------------------------------------------
def test_Standard():
    t = UniqueNameTrait()

    assert t.is_unique_name_normalized is False

    t.NormalizeUniqueName("name")

    assert t.is_unique_name_normalized is True
    assert t.unique_name == "name"
