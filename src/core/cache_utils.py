"""
Generic caching utilities for non-engine code paths (API, Data Lab, etc.).

This module provides lightweight, in-memory caching decorators and utilities
to improve performance of repeated operations in the API and auxiliary layers.
It is NOT intended for use within the core mathematical engines (TW369, Delta144)
which have their own state management.
"""

import time
import functools
from typing import Dict, Any, Tuple, Optional

_CACHE_STORE: Dict[str, Tuple[float, Any]] = {}
_CACHE_STATS = {"entries": 0, "hits": 0, "misses": 0}


def ttl_cache_simple(ttl_seconds: int):
    """
    Simple in-memory memoization decorator with TTL (Time To Live).
    
    Args:
        ttl_seconds: Number of seconds to keep the result in cache.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a simple cache key based on function name and arguments
            # Note: This relies on repr() which might not be unique or stable for all objects
            key_parts = (func.__module__, func.__name__, args, tuple(sorted(kwargs.items())))
            key = str(key_parts)
            
            now = time.time()
            
            # Check cache
            if key in _CACHE_STORE:
                timestamp, value = _CACHE_STORE[key]
                if now - timestamp < ttl_seconds:
                    _CACHE_STATS["hits"] += 1
                    return value
                else:
                    # Expired
                    del _CACHE_STORE[key]
                    _CACHE_STATS["entries"] -= 1
            
            _CACHE_STATS["misses"] += 1
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store result
            _CACHE_STORE[key] = (now, result)
            _CACHE_STATS["entries"] += 1
            
            return result
        return wrapper
    return decorator


def cache_stats() -> Dict[str, int]:
    """
    Return a snapshot of cache statistics.
    """
    return _CACHE_STATS.copy()


def clear_cache() -> None:
    """
    Clear the entire in-memory cache.
    """
    _CACHE_STORE.clear()
    _CACHE_STATS["entries"] = 0
