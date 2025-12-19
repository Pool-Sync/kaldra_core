"""
Parallel Execution Engine for KALDRA
Enables concurrent execution of independent pipeline modules.
"""

import logging
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
from dataclasses import dataclass
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Status of a parallel task."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class TaskResult:
    """
    Result from a parallel task execution.

    Attributes:
        task_name: Name of the task
        status: Execution status
        result: Result value if successful
        error: Error message if failed
        duration_ms: Execution time in milliseconds
    """

    task_name: str
    status: TaskStatus
    result: Any | None = None
    error: str | None = None
    duration_ms: float = 0.0


class ParallelExecutor:
    """
    Parallel task executor with timeout and failure isolation.

    Features:
    - Concurrent execution using ThreadPoolExecutor
    - Per-task timeout handling
    - Failure isolation (one task fails, others continue)
    - Result aggregation
    - Graceful degradation to sequential execution

    Example:
        >>> executor = ParallelExecutor(max_workers=4, default_timeout_ms=100)
        >>> tasks = {
        ...     'delta144': lambda ctx: delta144_engine.run(ctx),
        ...     'kindra': lambda ctx: kindra_engine.run(ctx),
        ...     'tw369': lambda ctx: tw369_engine.run(ctx)
        ... }
        >>> results = executor.run_parallel(tasks, context)
        >>> print(results['delta144'].status)
    """

    def __init__(self, max_workers: int = 6, default_timeout_ms: int = 100, enabled: bool = True):
        """
        Initialize parallel executor.

        Args:
            max_workers: Maximum number of concurrent threads
            default_timeout_ms: Default timeout per task in milliseconds
            enabled: Enable/disable parallel execution
        """
        self.max_workers = max_workers
        self.default_timeout_ms = default_timeout_ms
        self.enabled = enabled

        logger.info(
            f"ParallelExecutor initialized: workers={max_workers}, timeout={default_timeout_ms}ms, enabled={enabled}"
        )

    def run_parallel(
        self,
        tasks: dict[str, Callable],
        shared_context: Any | None = None,
        task_timeouts: dict[str, int] | None = None,
    ) -> dict[str, TaskResult]:
        """
        Execute tasks in parallel with timeout and failure isolation.

        Args:
            tasks: Dict mapping task names to callable functions
            shared_context: Optional context passed to all tasks
            task_timeouts: Optional dict of custom timeouts per task (ms)

        Returns:
            Dict mapping task names to TaskResult objects
        """
        if not self.enabled:
            logger.info("Parallel execution disabled, running sequentially")
            return self._run_sequential(tasks, shared_context)

        if not tasks:
            logger.warning("No tasks provided to run_parallel")
            return {}

        logger.info(f"Starting parallel execution of {len(tasks)} tasks")
        start_time = time.time()

        results: dict[str, TaskResult] = {}
        task_timeouts = task_timeouts or {}

        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_task = {}
                for task_name, task_fn in tasks.items():
                    future = executor.submit(self._execute_task, task_name, task_fn, shared_context)
                    future_to_task[future] = task_name

                # Collect results as they complete
                for future in as_completed(
                    future_to_task.keys(),
                    timeout=max(task_timeouts.values(), default=self.default_timeout_ms) / 1000.0,
                ):
                    task_name = future_to_task[future]
                    timeout_ms = task_timeouts.get(task_name, self.default_timeout_ms)

                    try:
                        result = future.result(timeout=timeout_ms / 1000.0)
                        results[task_name] = result

                    except TimeoutError:
                        logger.warning(f"Task '{task_name}' timed out after {timeout_ms}ms")
                        results[task_name] = TaskResult(
                            task_name=task_name,
                            status=TaskStatus.TIMEOUT,
                            error=f"Timeout after {timeout_ms}ms",
                            duration_ms=timeout_ms,
                        )

                    except Exception as e:
                        logger.error(f"Task '{task_name}' failed: {e}")
                        results[task_name] = TaskResult(
                            task_name=task_name,
                            status=TaskStatus.FAILED,
                            error=str(e),
                            duration_ms=0.0,
                        )

        except Exception as e:
            logger.error(f"Parallel executor failed: {e}, falling back to sequential")
            return self._run_sequential(tasks, shared_context)

        elapsed_ms = (time.time() - start_time) * 1000
        successful = sum(1 for r in results.values() if r.status == TaskStatus.COMPLETED)

        logger.info(f"Parallel execution complete: {successful}/{len(tasks)} successful in {elapsed_ms:.1f}ms")

        return results

    def _execute_task(self, task_name: str, task_fn: Callable, shared_context: Any | None) -> TaskResult:
        """
        Execute a single task with timing and error handling.

        Args:
            task_name: Name of the task
            task_fn: Function to execute
            shared_context: Context to pass to function

        Returns:
            TaskResult with execution details
        """
        start_time = time.time()

        try:
            logger.debug(f"Executing task '{task_name}'")

            # Call task function with or without context
            if shared_context is not None:
                result = task_fn(shared_context)
            else:
                result = task_fn()

            duration_ms = (time.time() - start_time) * 1000

            logger.debug(f"Task '{task_name}' completed in {duration_ms:.1f}ms")

            return TaskResult(
                task_name=task_name,
                status=TaskStatus.COMPLETED,
                result=result,
                duration_ms=duration_ms,
            )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000

            logger.error(f"Task '{task_name}' failed after {duration_ms:.1f}ms: {e}")

            return TaskResult(
                task_name=task_name,
                status=TaskStatus.FAILED,
                error=str(e),
                duration_ms=duration_ms,
            )

    def _run_sequential(self, tasks: dict[str, Callable], shared_context: Any | None) -> dict[str, TaskResult]:
        """
        Fallback: Execute tasks sequentially.

        Args:
            tasks: Dict mapping task names to callable functions
            shared_context: Optional context passed to all tasks

        Returns:
            Dict mapping task names to TaskResult objects
        """
        logger.info(f"Running {len(tasks)} tasks sequentially (fallback mode)")

        results: dict[str, TaskResult] = {}

        for task_name, task_fn in tasks.items():
            result = self._execute_task(task_name, task_fn, shared_context)
            results[task_name] = result

        return results

    def merge_results(
        self,
        results: dict[str, TaskResult],
        target_object: Any,
        result_mapping: dict[str, str] | None = None,
    ) -> Any:
        """
        Merge task results into a target object.

        Args:
            results: Dict of TaskResult objects
            target_object: Object to merge results into
            result_mapping: Optional dict mapping task names to attribute names

        Returns:
            Updated target object
        """
        result_mapping = result_mapping or {}

        for task_name, task_result in results.items():
            if task_result.status == TaskStatus.COMPLETED and task_result.result is not None:
                # Get attribute name (use mapping or task name)
                attr_name = result_mapping.get(task_name, task_name)

                # Set attribute on target object
                setattr(target_object, attr_name, task_result.result)

                logger.debug(f"Merged result from '{task_name}' into '{attr_name}'")
            else:
                logger.warning(f"Skipping merge for '{task_name}': status={task_result.status}")

        return target_object
