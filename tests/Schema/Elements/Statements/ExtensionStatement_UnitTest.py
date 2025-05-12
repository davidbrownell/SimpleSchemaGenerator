# ----------------------------------------------------------------------
# |
# |  ExtensionStatement_UnitTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-04-20 17:55:35
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for ExtensionStatement.py."""

import re
import sys

from pathlib import Path
from unittest.mock import Mock

import pytest

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx

from SimpleSchemaGenerator.Common.Region import Region
from SimpleSchemaGenerator.Schema.Elements.Statements.ExtensionStatement import *

sys.path.insert(0, str(PathEx.EnsureDir(Path(__file__).parent.parent.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from TestHelpers import TestElementVisitor


# ----------------------------------------------------------------------
def test_ExtensionStatementKeywordArg():
    region = Mock()
    name = Mock()
    expression = Mock()

    eska = ExtensionStatementKeywordArg(region, name, expression)

    assert eska.region is region
    assert eska.name is name
    assert eska.expression is expression

    assert TestElementVisitor(eska) == [
        eska,
        ("name", name),
        ("expression", expression),
    ]


# ----------------------------------------------------------------------
def test_ExtensionStatement():
    region = Mock()
    name = Mock()
    positional_arg1 = Mock()
    positional_arg2 = Mock()
    keyword_arg1 = ExtensionStatementKeywordArg(Mock(), TerminalElement[str](Mock(), "arg1"), Mock())
    keyword_arg2 = ExtensionStatementKeywordArg(Mock(), TerminalElement[str](Mock(), "arg2"), Mock())

    es = ExtensionStatement(region, name, [positional_arg1, positional_arg2], [keyword_arg1, keyword_arg2])

    assert es.region is region
    assert es.name is name
    assert es.positional_args == [positional_arg1, positional_arg2]
    assert es.keyword_args == {"arg1": keyword_arg1, "arg2": keyword_arg2}

    assert TestElementVisitor(es) == [
        es,
        ("name", name),
        ("positional_args", [positional_arg1, positional_arg2]),
        ("keyword_args", [keyword_arg1, keyword_arg2]),
    ]


# ----------------------------------------------------------------------
def test_ErrorDuplicateKeywordArg():
    with pytest.raises(
        Exception,
        match=re.escape(
            "An argument for the parameter 'dup' was already provided at 'foo, Ln 1, Col 2 -> Ln 3, Col 4'. (bar, Ln 10, Col 20 -> Ln 30, Col 40)"
        ),
    ):
        ExtensionStatement(
            Mock(),
            Mock(),
            [],
            [
                ExtensionStatementKeywordArg(
                    Mock(),
                    TerminalElement[str](Region.Create(Path("foo"), 1, 2, 3, 4), "dup"),
                    Mock(),
                ),
                ExtensionStatementKeywordArg(
                    Mock(),
                    TerminalElement[str](Region.Create(Path("bar"), 10, 20, 30, 40), "dup"),
                    Mock(),
                ),
            ],
        )
