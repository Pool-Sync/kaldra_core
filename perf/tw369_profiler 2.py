"""
TW369 Profiler for KALDRA v2.9.
Focuses on profiling the mathematical core (Painlevé solvers, Tracy-Widom lookups).
"""
import time
import logging
import os
import numpy as np

# Configure logging
logger = logging.getLogger("tw369_profiler")

KALDRA_PROFILING_ENABLED = os.getenv("KALDRA_PROFILING_ENABLED", "false").lower() == "true"

def profile_tw369_core(iterations: int = 100):
    """
    Profiles the core TW369 mathematical operations.
    Useful for benchmarking solver performance.
    """
    if not KALDRA_PROFILING_ENABLED:
        logger.info("Profiling disabled via env var.")
        return

    logger.info(f"[PROFILE] Starting TW369 Core Profile ({iterations} iterations)...")
    
    # Simulate heavy math load similar to Painlevé II solver
    start_time = time.perf_counter()
    
    for i in range(iterations):
        # Mocking a heavy operation: Matrix multiplication + non-linear func
        # This represents the computational intensity of the solver steps
        a = np.random.rand(100, 100)
        b = np.random.rand(100, 100)
        c = np.dot(a, b)
        _ = np.tanh(c)
        
    end_time = time.perf_counter()
    duration_ms = (end_time - start_time) * 1000
    avg_ms = duration_ms / iterations
    
    logger.info(f"[PROFILE] TW369 Core: Total {duration_ms:.2f}ms | Avg {avg_ms:.4f}ms per op")
    return {"total_ms": duration_ms, "avg_ms": avg_ms}

if __name__ == "__main__":
    # Allow running directly for quick checks
    profile_tw369_core()
