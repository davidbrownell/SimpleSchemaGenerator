# ----------------------------------------------------------------------
# |
# |  ExecuteInParallel_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-22 11:36:42
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for the ExecuteInParallel.py."""

import re
import textwrap

from pathlib import Path
from typing import cast

import pytest

from dbrownell_Common.Streams.DoneManager import DoneManager
from dbrownell_Common.TestHelpers.StreamTestHelpers import GenerateDoneManagerAndContent

from SimpleSchemaGenerator.Common.ExecuteInParallel import ExecuteInParallel


# ----------------------------------------------------------------------
@pytest.mark.parametrize("num_steps", [None, 1])
def test_Standard(num_steps):
    dm_and_content = GenerateDoneManagerAndContent()

    results = ExecuteInParallel(
        cast(DoneManager, next(dm_and_content)),
        "The heading",
        {
            Path("filename1"): "content1",
            Path("filename2"): "content2",
        },
        lambda context, _: f"__{context}__",
        quiet=False,
        max_num_threads=None,
        raise_if_single_exception=True,
        num_steps=num_steps,
    )

    assert cast(str, next(dm_and_content)) == textwrap.dedent(
        """\
        Heading...
          The heading (2 items)...DONE! (0, <scrubbed duration>, 2 items succeeded, no items with errors, no items with warnings)
        DONE! (0, <scrubbed duration>)
        """,
    )

    assert results == {
        Path("filename1"): "__content1__",
        Path("filename2"): "__content2__",
    }


# ----------------------------------------------------------------------
def test_MultipleExceptions():
    dm_and_content = GenerateDoneManagerAndContent()

    # ----------------------------------------------------------------------
    def Execute(*args, **kwargs):
        raise Exception("This is an exception")

    # ----------------------------------------------------------------------

    results = ExecuteInParallel(
        cast(DoneManager, next(dm_and_content)),
        "The heading",
        {
            Path("filename1"): "content1",
            Path("filename2"): "content2",
        },
        Execute,
        quiet=False,
        max_num_threads=None,
        raise_if_single_exception=True,
    )

    assert len(results) == 2
    assert isinstance(results[Path("filename1")], Exception)
    assert str(results[Path("filename1")]) == "This is an exception"
    assert isinstance(results[Path("filename2")], Exception)
    assert str(results[Path("filename2")]) == "This is an exception"


# ----------------------------------------------------------------------
def test_SingleException():
    dm_and_content = GenerateDoneManagerAndContent()

    with pytest.raises(
        Exception,
        match=re.escape("This is an exception for filename2"),
    ):
        # ----------------------------------------------------------------------
        def Execute(context, _):
            if context == "content2":
                raise Exception("This is an exception for filename2")

            return f"__{context}__"

        # ----------------------------------------------------------------------

        ExecuteInParallel(
            cast(DoneManager, next(dm_and_content)),
            "The heading",
            {
                Path("filename1"): "content1",
                Path("filename2"): "content2",
            },
            Execute,
            quiet=False,
            max_num_threads=None,
            raise_if_single_exception=True,
        )
