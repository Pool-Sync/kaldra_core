"""
Rate Limiter Middleware for KALDRA API.

Provides in-memory rate limiting capabilities.
Designed to be framework-agnostic but integrates with FastAPI if available.
"""

import time
from dataclasses import dataclass
from typing import Dict, Tuple, Callable, Any, Optional

# Conditional FastAPI imports
try:
    from fastapi import Request, HTTPException, Depends
except ImportError:  # pragma: no cover
    Request = object  # type: ignore
    HTTPException = Exception  # type: ignore
    Depends = lambda x: x  # type: ignore


@dataclass
class RateLimiterConfig:
    """Configuration for RateLimiter."""
    requests: int
    per_seconds: int
    key_prefix: str = "kaldra_api"


class InMemoryRateLimiter:
    """
    Simple in-memory rate limiter using a sliding window or fixed window approach.
    For simplicity and performance in this baseline, we use a fixed window counter.
    """

    def __init__(self, config: RateLimiterConfig):
        self.config = config
        # Storage: client_key -> (window_start_timestamp, count)
        self._storage: Dict[str, Tuple[float, int]] = {}

    def is_allowed(self, client_key: str) -> bool:
        """
        Check if the request is allowed for the given client key.
        """
        now = time.time()
        window_start, count = self._storage.get(client_key, (0.0, 0))

        if now - window_start > self.config.per_seconds:
            # New window
            self._storage[client_key] = (now, 1)
            return True
        
        if count < self.config.requests:
            # Within limit
            self._storage[client_key] = (window_start, count + 1)
            return True
            
        # Limit exceeded
        return False


def rate_limit_dependency(config: RateLimiterConfig) -> Callable:
    """
    Creates a FastAPI dependency for rate limiting.
    """
    limiter = InMemoryRateLimiter(config=config)

    async def _dep(request: Request) -> None:
        # If FastAPI is not installed or request is not a real Request object, skip
        if Request is object or not hasattr(request, "client"):
            return

        client_ip = request.client.host if request.client else "unknown"
        key = f"{config.key_prefix}:{client_ip}"
        
        if not limiter.is_allowed(key):
            if HTTPException is not Exception:
                raise HTTPException(
                    status_code=429, 
                    detail="Too Many Requests"
                )
            else:
                raise RuntimeError("Too Many Requests")

    return _dep
