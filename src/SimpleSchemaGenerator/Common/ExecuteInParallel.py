# ----------------------------------------------------------------------
# |
# |  ExecuteInParallel.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-22 08:53:14
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the ExecuteInParallel function."""

from pathlib import Path
from typing import Callable, cast, TypeVar

from dbrownell_Common import ExecuteTasks  # type: ignore[import-untyped]
from dbrownell_Common.Streams.DoneManager import DoneManager  # type: ignore[import-untyped]


# ----------------------------------------------------------------------
ExecuteInParallelInputT = TypeVar("ExecuteInParallelInputT")
ExecuteInParallelOutputT = TypeVar("ExecuteInParallelOutputT")


def ExecuteInParallel(
    dm: DoneManager,
    heading: str,
    items: dict[Path, ExecuteInParallelInputT],
    func: Callable[[ExecuteInParallelInputT, ExecuteTasks.Status], ExecuteInParallelOutputT],
    *,
    quiet: bool,
    max_num_threads: int | None,
    raise_if_single_exception: bool,
    num_steps: int | None = None,
) -> dict[Path, Exception] | dict[Path, ExecuteInParallelOutputT]:
    # ----------------------------------------------------------------------
    def Prepare(
        context: ExecuteInParallelInputT,
        on_simple_status_func: Callable[[str], None],  # pylint: disable=unused-argument
    ) -> (
        tuple[int, ExecuteTasks.TransformTasksExTypes.TransformFuncType]
        | ExecuteTasks.TransformTasksExTypes.TransformFuncType
    ):
        # ----------------------------------------------------------------------
        def Execute(
            status: ExecuteTasks.Status,
        ) -> ExecuteInParallelOutputT:
            return func(context, status)

        # ----------------------------------------------------------------------

        if num_steps is None:
            return Execute

        return num_steps, Execute

    # ----------------------------------------------------------------------

    exceptions: dict[Path, Exception] = {}
    results: dict[Path, ExecuteInParallelOutputT] = {}

    for filename, result in zip(
        items.keys(),
        ExecuteTasks.TransformTasksEx(
            dm,
            heading,
            [ExecuteTasks.TaskData(str(filename), context) for filename, context in items.items()],
            Prepare,
            quiet=quiet,
            max_num_threads=max_num_threads,
            return_exceptions=True,
        ),
    ):
        if isinstance(result, Exception):
            exceptions[filename] = result
        else:
            results[filename] = cast(ExecuteInParallelOutputT, result)

    if raise_if_single_exception and len(exceptions) == 1:
        raise next(iter(exceptions.values()))

    return exceptions or results
