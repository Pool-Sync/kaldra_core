"""
Caching Decorators for KALDRA
Provides @redis_cache decorator for function-level caching.
"""

import hashlib
import logging
from collections.abc import Callable
from functools import wraps
from typing import Any

from .redis_client import get_redis_client

logger = logging.getLogger(__name__)


def _generate_cache_key(prefix: str, func_name: str, args: tuple, kwargs: dict) -> str:
    """
    Generate cache key from function arguments.

    Args:
        prefix: Key prefix (module name)
        func_name: Function name
        args: Positional arguments
        kwargs: Keyword arguments

    Returns:
        Cache key string
    """
    # Create unique key from args and kwargs
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    key_str = ":".join(key_parts)

    # Hash if too long
    if len(key_str) > 100:
        key_hash = hashlib.md5(key_str.encode()).hexdigest()[:16]
        return f"{prefix}:{func_name}:{key_hash}"

    return f"{prefix}:{func_name}:{key_str}" if key_str else f"{prefix}:{func_name}"


def redis_cache(ttl: int = 3600, key_prefix: str = "kaldra", enabled: bool = True):
    """
    Decorator to cache function results in Redis.

    Args:
        ttl: Time to live in seconds (default 1 hour)
        key_prefix: Prefix for cache keys (default "kaldra")
        enabled: Enable/disable caching (default True)

    Usage:
        @redis_cache(ttl=3600, key_prefix="delta144")
        def expensive_function(arg1, arg2):
            return complex_computation(arg1, arg2)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if not enabled:
                return func(*args, **kwargs)

            # Get Redis client
            client = get_redis_client()
            if not client.enabled:
                # Redis not available, execute function
                return func(*args, **kwargs)

            # Generate cache key
            cache_key = _generate_cache_key(key_prefix, func.__name__, args, kwargs)

            # Try to get from cache
            cached_value = client.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache HIT: {cache_key}")
                return cached_value

            # Cache miss - execute function
            logger.debug(f"Cache MISS: {cache_key}")
            result = func(*args, **kwargs)

            # Store in cache
            client.set(cache_key, result, ttl=ttl)

            return result

        return wrapper

    return decorator


def invalidate_cache(key_prefix: str, pattern: str | None = None):
    """
    Invalidate cache keys by prefix or pattern.

    Args:
        key_prefix: Key prefix to invalidate
        pattern: Optional pattern (supports wildcards)

    Note: This requires Redis SCAN operation.
    For now, implements basic prefix-based invalidation.
    """
    client = get_redis_client()
    if not client.enabled or not client._client:
        return

    try:
        # If pattern specified, use SCAN to find matching keys
        if pattern:
            search_pattern = f"{key_prefix}:{pattern}"
        else:
            search_pattern = f"{key_prefix}:*"

        # Scan and delete matching keys
        cursor = 0
        deleted_count = 0

        while True:
            cursor, keys = client._client.scan(cursor, match=search_pattern, count=100)
            if keys:
                client._client.delete(*keys)
                deleted_count += len(keys)

            if cursor == 0:
                break

        logger.info(f"Invalidated {deleted_count} cache keys matching {search_pattern}")

    except Exception as e:
        logger.warning(f"Cache invalidation failed: {e}")
