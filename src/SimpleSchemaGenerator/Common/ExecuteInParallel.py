# ----------------------------------------------------------------------
# |
# |  ExecuteInParallel.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-05-27 14:54:42
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Contains the ExecuteInParallel function."""

from pathlib import Path
from typing import Callable, cast, Optional, TypeVar, Union

from dbrownell_Common import ExecuteTasks  # type: ignore[import-untyped]
from dbrownell_Common.Streams.DoneManager import DoneManager  # type: ignore[import-untyped]


# ----------------------------------------------------------------------
# |
# |  Public Types
# |
# ----------------------------------------------------------------------
ExecuteInParallelInputType = TypeVar("ExecuteInParallelInputType")
ExecuteInParallelOutputType = TypeVar("ExecuteInParallelOutputType")


# ----------------------------------------------------------------------
# |
# |  Public Functions
# |
# ----------------------------------------------------------------------
def ExecuteInParallel(
    dm: DoneManager,
    heading: str,
    items: dict[Path, ExecuteInParallelInputType],
    func: Callable[[ExecuteInParallelInputType, ExecuteTasks.Status], ExecuteInParallelOutputType],
    *,
    quiet: bool,
    max_num_threads: Optional[int],
    raise_if_single_exception: bool,
    num_steps: Optional[int] = None,
) -> Union[
    dict[Path, Exception],
    dict[Path, ExecuteInParallelOutputType],
]:
    # ----------------------------------------------------------------------
    def PrepareTask(
        context: ExecuteInParallelInputType,
        on_simple_status_func: Callable[[str], None],  # pylint: disable=unused-argument
    ) -> Union[
        tuple[
            int,  # Number of steps to execute
            ExecuteTasks.TransformTasksExTypes.TransformFuncType,
        ],
        ExecuteTasks.TransformTasksExTypes.TransformFuncType,
    ]:
        # ----------------------------------------------------------------------
        def Execute(
            status: ExecuteTasks.Status,
        ) -> ExecuteInParallelOutputType:
            return func(context, status)

        # ----------------------------------------------------------------------

        if num_steps is not None:
            return num_steps, Execute

        return Execute

    # ----------------------------------------------------------------------

    exceptions: dict[Path, Exception] = {}
    results: dict[Path, ExecuteInParallelOutputType] = {}

    for filename, result in zip(
        items.keys(),
        ExecuteTasks.TransformTasksEx(
            dm,
            heading,
            [ExecuteTasks.TaskData(str(filename), context) for filename, context in items.items()],
            PrepareTask,
            quiet=quiet,
            max_num_threads=max_num_threads,
            return_exceptions=True,
        ),
    ):
        if isinstance(result, Exception):
            exceptions[filename] = result
        else:
            results[filename] = cast(ExecuteInParallelOutputType, result)

    if raise_if_single_exception and exceptions and len(exceptions) == 1:
        raise next(iter(exceptions.values()))

    return exceptions or results
