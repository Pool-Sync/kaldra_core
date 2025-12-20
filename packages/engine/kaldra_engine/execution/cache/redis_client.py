"""
Redis Client for KALDRA Caching Layer
Provides optimized caching for expensive computations.
"""

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class RedisClient:
    """
    Redis client for KALDRA caching operations.

    Features:
    - Automatic JSON serialization/deserialization
    - Configurable TTL per key
    - Graceful degradation if Redis unavailable
    - Environment-based configuration
    """

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        password: str | None = None,
        enabled: bool | None = None,
    ):
        """
        Initialize Redis client.

        Args:
            host: Redis host (default from REDIS_HOST env)
            port: Redis port (default from REDIS_PORT env)
            password: Redis password (default from REDIS_PASSWORD env)
            enabled: Enable/disable Redis (default from REDIS_ENABLED env)
        """
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = int(port or os.getenv("REDIS_PORT", "6379"))
        self.password = password or os.getenv("REDIS_PASSWORD")
        self.enabled = enabled if enabled is not None else os.getenv("REDIS_ENABLED", "false").lower() == "true"

        self._client = None
        self._connect()

    def _connect(self):
        """Attempt to connect to Redis."""
        if not self.enabled:
            logger.info("Redis caching disabled (REDIS_ENABLED=false)")
            return

        try:
            import redis

            self._client = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                decode_responses=True,
                socket_connect_timeout=1,
                socket_timeout=1,
            )
            # Test connection
            self._client.ping()
            logger.info(f"Redis connected: {self.host}:{self.port}")
        except ImportError:
            logger.warning("redis package not installed. Install with: pip install redis")
            self.enabled = False
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Caching disabled.")
            self._client = None
            self.enabled = False

    def get(self, key: str) -> Any | None:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        if not self.enabled or not self._client:
            return None

        try:
            data = self._client.get(key)
            if data is None:
                return None
            return self._deserialize(data)
        except Exception as e:
            logger.warning(f"Redis GET failed for key {key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """
        Set value in cache with TTL.

        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time to live in seconds (default 1 hour)

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self._client:
            return False

        try:
            serialized = self._serialize(value)
            self._client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            logger.warning(f"Redis SET failed for key {key}: {e}")
            return False

    def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.

        Args:
            key: Cache key

        Returns:
            True if key exists, False otherwise
        """
        if not self.enabled or not self._client:
            return False

        try:
            return bool(self._client.exists(key))
        except Exception as e:
            logger.warning(f"Redis EXISTS failed for key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Delete key from cache.

        Args:
            key: Cache key

        Returns:
            True if deleted, False otherwise
        """
        if not self.enabled or not self._client:
            return False

        try:
            self._client.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Redis DELETE failed for key {key}: {e}")
            return False

    def _serialize(self, value: Any) -> str:
        """Serialize value to JSON string."""
        return json.dumps(value)

    def _deserialize(self, data: str) -> Any:
        """Deserialize JSON string to value."""
        return json.loads(data)

    def flush_all(self) -> bool:
        """
        Flush all keys from cache (use with caution).

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self._client:
            return False

        try:
            self._client.flushall()
            logger.info("Redis cache flushed")
            return True
        except Exception as e:
            logger.warning(f"Redis FLUSHALL failed: {e}")
            return False


# Global singleton instance
_redis_client: RedisClient | None = None


def get_redis_client() -> RedisClient:
    """
    Get global Redis client instance (singleton).

    Returns:
        RedisClient instance
    """
    global _redis_client
    if _redis_client is None:
        _redis_client = RedisClient()
    return _redis_client
