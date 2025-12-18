"""
Fallback Decorator for KALDRA v2.9.
Provides a safe default value when a function fails.
"""
import functools
import logging
from typing import Callable, Any

logger = logging.getLogger("kaldra_hardening")

def safe_fallback(default_value: Any):
    """
    Decorator to return a default value if the function raises an exception.
    Logs the exception but suppresses it.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Function {func.__name__} failed. Using fallback. Error: {e}")
                return default_value
        return wrapper
    return decorator
