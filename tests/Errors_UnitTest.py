# ----------------------------------------------------------------------
# |
# |  Errors_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-10 08:53:59
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Errors.py"""

from unittest.mock import Mock

from SimpleSchemaGenerator.Errors import *


# ----------------------------------------------------------------------
def test_Standard():
    # This isn't really much to test here, as the functionality has already been verified when
    # testing SimpleSchemaGenerator.Common.Error. Test one error message just in case.
    region_mock = Mock()

    error = CardinalityInvalidRange.Create(region_mock, 10, 5)

    assert error.regions == [region_mock]
    assert error.message == "Invalid cardinality (10 > 5)."
