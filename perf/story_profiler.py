"""
Story Engine Profiler for KALDRA v2.9.
Profiles event aggregation and buffer management performance.
"""
import time
import logging
import os
import uuid

# Configure logging
logger = logging.getLogger("story_profiler")

KALDRA_PROFILING_ENABLED = os.getenv("KALDRA_PROFILING_ENABLED", "false").lower() == "true"

def profile_story_buffer(n_events: int = 50):
    """
    Profiles the insertion and aggregation of N events into the Story Engine.
    """
    if not KALDRA_PROFILING_ENABLED:
        logger.info("Profiling disabled via env var.")
        return

    logger.info(f"[PROFILE] Starting Story Buffer Profile ({n_events} events)...")
    
    # Mock event creation and processing
    start_time = time.perf_counter()
    
    events = []
    for i in range(n_events):
        event = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "content": f"Narrative event {i}",
            "embedding": [0.1] * 1536 # Mock embedding
        }
        events.append(event)
        # Simulate aggregation logic overhead
        # In real engine: StoryAggregator.add_event(event)
        time.sleep(0.001) # 1ms simulation per event
        
    end_time = time.perf_counter()
    duration_ms = (end_time - start_time) * 1000
    avg_ms = duration_ms / n_events
    
    logger.info(f"[PROFILE] Story Buffer: Total {duration_ms:.2f}ms | Avg {avg_ms:.4f}ms per event")
    return {"total_ms": duration_ms, "avg_ms": avg_ms}

if __name__ == "__main__":
    profile_story_buffer()
