"""
Timeout Decorator for KALDRA v2.9.
Enforces strict time limits on function execution.
"""
import signal
import functools
import logging
from typing import Any, Callable

logger = logging.getLogger("kaldra_hardening")

class TimeoutError(Exception):
    pass

def with_timeout(seconds: int):
    """
    Decorator to enforce a timeout on a function.
    Uses signal.alarm, so it primarily works on main thread/Unix.
    For threading support, would need a different approach (e.g. threading.Timer or async).
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            def _handle_timeout(signum, frame):
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds}s")

            # Set the signal handler and a 
            old_handler = signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            
            try:
                result = func(*args, **kwargs)
            finally:
                # Disable alarm
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
                
            return result
        return wrapper
    return decorator
