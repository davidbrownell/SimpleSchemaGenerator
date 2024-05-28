# ----------------------------------------------------------------------
# |
# |  Resolve.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-05-27 11:13:19
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains functionality for resolving types."""

from pathlib import Path
from typing import Callable, cast, Optional, TypeVar, Union

from dbrownell_Common.Streams.DoneManager import DoneManager  # type: ignore[import-untyped]

from ...Elements.Statements.RootStatement import RootStatement
from ....Common.ExecuteInParallel import ExecuteInParallel as ExecuteInParallelImpl


# ----------------------------------------------------------------------
def Resolve(
    dm: DoneManager,
    roots: dict[Path, RootStatement],
    *,
    single_threaded: bool = False,
    quiet: bool = False,
    raise_if_single_exception: bool = True,
) -> Optional[dict[Path, Exception]]:
    max_num_threads = 1 if single_threaded else None

    # Create namespaces
    with dm.VerboseNested("Creating namespaces...") as verbose_dm:
        # ----------------------------------------------------------------------
        def CreateNamespace(
            root: RootStatement,
        ) -> Namespace:
            pass  # BugBug

        # ----------------------------------------------------------------------

        namespaces = _ExecuteInParallel(
            verbose_dm,
            roots,
            CreateNamespace,
            quiet=quiet,
            max_num_threads=max_num_threads,
            raise_if_single_exception=raise_if_single_exception,
        )

        if verbose_dm.result != 0:
            assert all(isinstance(value, Exception) for value in namespaces.values()), values
            return cast(dict[Path, Exception], namespaces)

        namespaces = cast(dict[Path, Namespace], namespace)

    # BugBug


# ----------------------------------------------------------------------
# |
# |  Private Functions
# |
# ----------------------------------------------------------------------
_ExecuteInParallelInputType = TypeVar("_ExecuteInParallelInputType")
_ExecuteInParallelOutputType = TypeVar("_ExecuteInParallelOutputType")


def _ExecuteInParallel(
    dm: DoneManager,
    items: dict[Path, _ExecuteInParallelInputType],
    func: Callable[[_ExecuteInParallelInputType], _ExecuteInParallelOutputType],
    *,
    quiet: bool,
    max_num_threads: Optional[int],
    raise_if_single_exception: bool,
) -> Union[
    dict[Path, Exception],
    dict[Path, _ExecuteInParallelOutputType],
]:
    return ExecuteInParallelImpl(
        dm,
        "Processing",
        items,
        lambda context, status: func(context),
        quiet=quiet,
        max_num_threads=max_num_threads,
        raise_if_single_exception=raise_if_single_exception,
    )
