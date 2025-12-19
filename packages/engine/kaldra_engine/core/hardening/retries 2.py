"""
Retry Decorator for KALDRA v2.9.
Implements exponential backoff for transient failures.
"""
import time
import functools
import logging
import random
from typing import Callable, Any, Type, Tuple

logger = logging.getLogger("kaldra_hardening")

def with_retries(max_attempts: int = 3, backoff: float = 1.0, exceptions: Tuple[Type[Exception], ...] = (Exception,)):
    """
    Decorator to retry a function upon failure.
    
    Args:
        max_attempts: Maximum number of total attempts (1 means no retry).
        backoff: Base backoff time in seconds (exponential).
        exceptions: Tuple of exceptions to catch and retry.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        logger.error(f"Function {func.__name__} failed after {max_attempts} attempts. Error: {e}")
                        raise e
                    
                    sleep_time = backoff * (2 ** (attempt - 1)) + random.uniform(0, 0.1)
                    logger.warning(f"Function {func.__name__} failed (Attempt {attempt}/{max_attempts}). Retrying in {sleep_time:.2f}s. Error: {e}")
                    time.sleep(sleep_time)
                    attempt += 1
        return wrapper
    return decorator
