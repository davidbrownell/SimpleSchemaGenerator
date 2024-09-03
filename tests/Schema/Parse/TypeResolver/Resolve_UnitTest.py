# ----------------------------------------------------------------------
# |
# |  Resolve_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-23 10:29:43
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for Resolve.py"""

import re
import sys
import textwrap

from pathlib import Path, PurePath
from typing import cast, Optional

import pytest

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx
from dbrownell_Common.TestHelpers.StreamTestHelpers import GenerateDoneManagerAndContent

from SimpleSchemaGenerator.Schema.Parse.ANTLR.Parse import Parse
from SimpleSchemaGenerator.Schema.Parse.TypeResolver.Resolve import *

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TerminalElementVisitor, TestElementVisitor, YamlVisitor


# ----------------------------------------------------------------------
sample_schemas = PathEx.EnsureDir(
    Path(__file__).parent.parent.parent.parent.parent
    / "src"
    / "SimpleSchemaGenerator"
    / "SampleSchemas"
)


# ----------------------------------------------------------------------
class TestResolve:
    # ----------------------------------------------------------------------
    @pytest.mark.parametrize(
        "filename",
        sample_schemas.iterdir(),
        ids=[filename.name for filename in sample_schemas.iterdir()],
    )
    def test_File(self, filename, snapshot):

        if filename.name == "Import.SimpleSchema":
            expected_num_results = 4
        else:
            expected_num_results = 1

        root = _ExecuteSingleFile(filename, expected_num_results=expected_num_results)

        visitor = YamlVisitor()

        root.Accept(visitor)

        # BugBug assert visitor.yaml_string == snapshot


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _Execute(
    workspaces: dict[
        Path,  # workspace root
        dict[
            PurePath,  # relative path
            Callable[[], str],  # get content
        ],
    ],
    *,
    single_threaded: bool = False,
    quiet: bool = False,
    raise_if_single_exception: bool = True,
    expected_result: int = 0,
    expected_content: Optional[str] = None,
) -> dict[Path, RootStatement]:
    # Parse
    dm_and_content = GenerateDoneManagerAndContent()

    dm = cast(DoneManager, next(dm_and_content))

    parse_result = Parse(
        dm,
        workspaces,
        single_threaded=single_threaded,
        quiet=quiet,
        raise_if_single_exception=raise_if_single_exception,
    )

    assert dm.result == 0, dm.result

    assert len(parse_result) == 1, parse_result
    workspace_root, parse_results = next(iter(parse_result.items()))

    assert all(isinstance(value, RootStatement) for value in parse_results.values())

    results: dict[Path, RootStatement] = {
        workspace_root / key: cast(RootStatement, value) for key, value in parse_results.items()
    }

    # Resolve
    dm_and_content = GenerateDoneManagerAndContent()

    dm = cast(DoneManager, next(dm_and_content))

    Resolve(
        dm,
        results,
        single_threaded=single_threaded,
        quiet=quiet,
        raise_if_single_exception=raise_if_single_exception,
    )

    assert dm.result == expected_result, (dm.result, expected_result)

    if expected_content is not None:
        content = cast(str, next(dm_and_content))
        assert content == expected_content

    return results


# ----------------------------------------------------------------------
def _ExecuteSingleFile(
    schema_filename: Path,
    *,
    expected_num_results: int = 1,
) -> RootStatement:
    content = schema_filename.read_text(encoding="utf-8")

    result = _Execute({schema_filename.parent: {PurePath(schema_filename.name): lambda: content}})

    assert len(result) == expected_num_results
    return cast(RootStatement, result[schema_filename])
