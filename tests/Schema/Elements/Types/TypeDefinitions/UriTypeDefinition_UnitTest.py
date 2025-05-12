# ----------------------------------------------------------------------
# |
# |  UriTypeDefinition_UnitTest.py
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
"""Unit tests for UriTypeDefinition.py"""

import re

from unittest.mock import Mock

import pytest

from SimpleSchemaGenerator.Schema.Elements.Types.TypeDefinitions.UriTypeDefinition import *


# ----------------------------------------------------------------------
class TestUriAuthority:
    # ----------------------------------------------------------------------
    def test_Standard(self):
        assert str(Uri.Authority("//", None, "foo.bar", None)) == "//foo.bar/"

    # ----------------------------------------------------------------------
    def test_WithUsername(self):
        assert str(Uri.Authority("////", "the_username", "foo.bar", None)) == "////the_username@foo.bar/"

    # ----------------------------------------------------------------------
    def test_WithPort(self):
        assert str(Uri.Authority("__", None, "foo.bar", 1234)) == "__foo.bar:1234/"

    # ----------------------------------------------------------------------
    def test_Complete(self):
        assert str(Uri.Authority("//", "the_username", "foo.bar", 1234)) == "//the_username@foo.bar:1234/"


# ----------------------------------------------------------------------
class TestUri:
    # ----------------------------------------------------------------------
    def test_Standard(self):
        assert str(Uri("file", None, "the_path", None, None)) == "file:the_path"

    # ----------------------------------------------------------------------
    def test_WithAuthority(self):
        assert (
            str(Uri("https", Uri.Authority("//", None, "foo.bar", None), "", None, None))
            == "https://foo.bar/"
        )

    # ----------------------------------------------------------------------
    def test_WithQuery(self):
        assert str(Uri("file", None, "", "the_query", None)) == "file:?the_query"

    # ----------------------------------------------------------------------
    def test_WithFragment(self):
        assert str(Uri("file", None, "", None, "the_fragment")) == "file:#the_fragment"

    # ----------------------------------------------------------------------
    def test_Complete(self):
        assert (
            str(
                Uri(
                    "https",
                    Uri.Authority("//", None, "foo.bar", 1234),
                    "the_path",
                    "the_query",
                    "the_fragment",
                )
            )
            == "https://foo.bar:1234/the_path?the_query#the_fragment"
        )


# ----------------------------------------------------------------------
class TestUriTypeDefinition:
    # ----------------------------------------------------------------------
    def test_DisplayType(self):
        assert UriTypeDefinition(Mock()).display_type == "Uri"

    # ----------------------------------------------------------------------
    @pytest.mark.parametrize("trailing_slash", ["", "/"])
    def test_ToPythonInstance(self, trailing_slash):
        uri_type = UriTypeDefinition(Mock())

        uri = uri_type.ToPythonInstance("https://foo.bar{}".format(trailing_slash))

        assert uri == Uri("https", Uri.Authority("//", None, "foo.bar", None), None, None, None)
        assert uri_type.ToPythonInstance(uri) is uri

        assert uri_type.ToPythonInstance("https://foo.bar/one/two/three") == Uri(
            "https", Uri.Authority("//", None, "foo.bar", None), "one/two/three", None, None
        )
        assert uri_type.ToPythonInstance("https://foo.bar:1234/one/two/three") == Uri(
            "https", Uri.Authority("//", None, "foo.bar", 1234), "one/two/three", None, None
        )

        with pytest.raises(
            Exception,
            match=re.escape("'this is not a valid uri' is not a valid URI."),
        ):
            uri_type.ToPythonInstance("this is not a valid uri")
