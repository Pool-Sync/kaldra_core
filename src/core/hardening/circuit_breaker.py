"""
Circuit Breaker for KALDRA v2.9.
Prevents cascading failures by stopping calls to failing services.
"""
import time
import functools
import logging
from typing import Callable, Any, Dict

logger = logging.getLogger("kaldra_hardening")

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreakerState:
    def __init__(self, fail_threshold: int, reset_time: int):
        self.fail_threshold = fail_threshold
        self.reset_time = reset_time
        self.failures = 0
        self.last_failure_time = 0
        self.is_open = False

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.fail_threshold:
            self.is_open = True
            logger.error(f"Circuit Breaker OPENED (Failures: {self.failures})")

    def record_success(self):
        if self.is_open:
            logger.info("Circuit Breaker CLOSED (Success)")
        self.failures = 0
        self.is_open = False

    def check(self):
        if self.is_open:
            if time.time() - self.last_failure_time > self.reset_time:
                # Half-open state (allow one try)
                logger.info("Circuit Breaker HALF-OPEN (Reset timeout passed)")
                return # Allow execution
            raise CircuitBreakerOpenException("Circuit Breaker is OPEN")

# Global registry for circuit breakers
_breakers: Dict[str, CircuitBreakerState] = {}

def circuit_breaker(name: str, fail_threshold: int = 5, reset_time: int = 60):
    """
    Decorator to implement Circuit Breaker pattern.
    """
    if name not in _breakers:
        _breakers[name] = CircuitBreakerState(fail_threshold, reset_time)
    
    breaker = _breakers[name]

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            breaker.check()
            
            try:
                result = func(*args, **kwargs)
                breaker.record_success()
                return result
            except Exception as e:
                breaker.record_failure()
                raise e
        return wrapper
    return decorator
