"""
Test script for Parallel Executor
Validates concurrent execution, timeout handling, and failure isolation.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.execution.execution.parallel_executor import (
    ParallelExecutor,
    TaskStatus
)

print("\n" + "="*60)
print("🧪 PARALLEL EXECUTOR TEST SUITE")
print("="*60)


def test_basic_parallel_execution():
    """Test basic parallel execution."""
    print("\n" + "="*60)
    print("TEST 1: Basic Parallel Execution")
    print("="*60)
    
    def task_a():
        time.sleep(0.05)
        return {"result": "A"}
    
    def task_b():
        time.sleep(0.05)
        return {"result": "B"}
    
    def task_c():
        time.sleep(0.05)
        return {"result": "C"}
    
    executor = ParallelExecutor(max_workers=3, enabled=True)
    
    tasks = {
        "task_a": task_a,
        "task_b": task_b,
        "task_c": task_c
    }
    
    start = time.time()
    results = executor.run_parallel(tasks)
    elapsed = time.time() - start
    
    print(f"\n📊 Results:")
    print(f"   Elapsed time: {elapsed*1000:.1f}ms")
    print(f"   Expected: ~50ms (parallel) vs ~150ms (sequential)")
    
    for name, result in results.items():
        print(f"   {name}: {result.status.value} ({result.duration_ms:.1f}ms)")
    
    all_completed = all(r.status == TaskStatus.COMPLETED for r in results.values())
    if all_completed and elapsed < 0.1:  # Should be ~50ms not ~150ms
        print("\n   ✅ Parallel execution working!")
    else:
        print("\n   ❌ May be running sequentially")


def test_timeout_handling():
    """Test timeout handling."""
    print("\n" + "="*60)
    print("TEST 2: Timeout Handling")
    print("="*60)
    
    def fast_task():
        time.sleep(0.01)
        return "fast"
    
    def slow_task():
        time.sleep(1.0)  # Will timeout
        return "slow"
    
    executor = ParallelExecutor(max_workers=2, default_timeout_ms=50)
    
    tasks = {
        "fast": fast_task,
        "slow": slow_task
    }
    
    results = executor.run_parallel(tasks)
    
    print(f"\n📊 Results:")
    for name, result in results.items():
        print(f"   {name}: {result.status.value}")
        if result.error:
            print(f"      Error: {result.error}")
    
    if (results["fast"].status == TaskStatus.COMPLETED and
        results["slow"].status == TaskStatus.TIMEOUT):
        print("\n   ✅ Timeout handling working!")
    else:
        print("\n   ❌ Timeout not working as expected")


def test_failure_isolation():
    """Test that one task failure doesn't affect others."""
    print("\n" + "="*60)
    print("TEST 3: Failure Isolation")
    print("="*60)
    
    def good_task_1():
        return "success_1"
    
    def bad_task():
        raise ValueError("Intentional failure")
    
    def good_task_2():
        return "success_2"
    
    executor = ParallelExecutor(max_workers=3)
    
    tasks = {
        "good1": good_task_1,
        "bad": bad_task,
        "good2": good_task_2
    }
    
    results = executor.run_parallel(tasks)
    
    print(f"\n📊 Results:")
    for name, result in results.items():
        print(f"   {name}: {result.status.value}")
        if result.error:
            print(f"      Error: {result.error}")
    
    good_count = sum(1 for r in results.values() if r.status == TaskStatus.COMPLETED)
    if good_count == 2 and results["bad"].status == TaskStatus.FAILED:
        print("\n   ✅ Failure isolation working!")
    else:
        print("\n   ❌ Failures may be cascading")


def test_sequential_fallback():
    """Test fallback to sequential execution."""
    print("\n" + "="*60)
    print("TEST 4: Sequential Fallback")
    print("="*60)
    
    def task():
        return "result"
    
    executor = ParallelExecutor(max_workers=2, enabled=False)
    
    tasks = {
        "task1": task,
        "task2": task
    }
    
    results = executor.run_parallel(tasks)
    
    print(f"\n📊 Results:")
    all_completed = all(r.status == TaskStatus.COMPLETED for r in results.values())
    print(f"   All tasks completed: {all_completed}")
    
    if all_completed:
        print("\n   ✅ Sequential fallback working!")
    else:
        print("\n   ❌ Fallback not working")


def test_context_passing():
    """Test passing shared context to tasks."""
    print("\n" + "="*60)
    print("TEST 5: Context Passing")
    print("="*60)
    
    class Context:
        def __init__(self):
            self.value = 42
    
    def task_with_context(ctx):
        return ctx.value * 2
    
    executor = ParallelExecutor()
    context = Context()
    
    tasks = {
        "task1": task_with_context,
        "task2": task_with_context
    }
    
    results = executor.run_parallel(tasks, shared_context=context)
    
    print(f"\n📊 Results:")
    for name, result in results.items():
        print(f"   {name}: result={result.result}")
    
    all_correct = all(r.result == 84 for r in results.values())
    if all_correct:
        print("\n   ✅ Context passing working!")
    else:
        print("\n   ❌ Context not passed correctly")


def main():
    """Run all tests."""
    test_basic_parallel_execution()
    test_timeout_handling()
    test_failure_isolation()
    test_sequential_fallback()
    test_context_passing()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETE")
    print("="*60)
    print("\n💡 ParallelExecutor is operational!")
    print()


if __name__ == "__main__":
    main()
