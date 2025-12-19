"""
Pipeline Profiler for KALDRA v2.9.
Measures end-to-end latency and component-level breakdown.
"""
import time
import logging
import os
import functools
from typing import Callable, Any, Dict

# Configure basic logging for profiler
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kaldra_profiler")

KALDRA_PROFILING_ENABLED = os.getenv("KALDRA_PROFILING_ENABLED", "false").lower() == "true"

def profile_step(func):
    """Decorator to profile a specific step if profiling is enabled."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not KALDRA_PROFILING_ENABLED:
            return func(*args, **kwargs)
        
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000
            logger.info(f"[PROFILE] Step {func.__name__}: {duration_ms:.2f}ms")
    return wrapper

class PipelineProfiler:
    def __init__(self, request_id: str = "unknown"):
        self.request_id = request_id
        self.metrics: Dict[str, float] = {}
        self.start_time = 0.0

    def start(self):
        self.start_time = time.perf_counter()
        if KALDRA_PROFILING_ENABLED:
            logger.info(f"[PROFILE] [{self.request_id}] Pipeline STARTED")

    def stop(self):
        end_time = time.perf_counter()
        total_duration_ms = (end_time - self.start_time) * 1000
        self.metrics["total_duration_ms"] = total_duration_ms
        if KALDRA_PROFILING_ENABLED:
            logger.info(f"[PROFILE] [{self.request_id}] Pipeline FINISHED: {total_duration_ms:.2f}ms")
        return self.metrics

    def profile_full_pipeline(self, pipeline_func: Callable, *args, **kwargs):
        """
        Profiles the full execution of a pipeline function.
        """
        self.start()
        try:
            return pipeline_func(*args, **kwargs)
        finally:
            self.stop()

# Global instance for ad-hoc use
_global_profiler = PipelineProfiler()

def profile_full_pipeline(text: str):
    """
    Standalone helper to profile a text input through the master engine.
    (Requires MasterEngine instance to be passed or instantiated - this is a stub for the interface)
    """
    # In a real scenario, this would import the master engine and run it.
    # For now, it serves as the interface definition requested.
    pass
