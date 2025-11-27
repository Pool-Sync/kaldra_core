"""
Metrics and Monitoring integration for KALDRA API.

Provides integration with Prometheus for tracking request counts and latencies.
Fails gracefully if prometheus_client is not installed.
"""

import time
from typing import Optional, Callable

try:
    from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
except ImportError:  # pragma: no cover
    Counter = Histogram = None  # type: ignore
    CONTENT_TYPE_LATEST = "text/plain"
    
    def generate_latest():  # type: ignore
        return b""


# Global metrics placeholders
REQUEST_COUNT: Optional[Any] = None
REQUEST_LATENCY: Optional[Any] = None


def register_default_metrics():
    """
    Initialize default Prometheus metrics if the client library is available.
    Idempotent: safe to call multiple times.
    """
    global REQUEST_COUNT, REQUEST_LATENCY
    
    if Counter is None or Histogram is None:
        return

    if REQUEST_COUNT is None:
        REQUEST_COUNT = Counter(
            'kaldra_api_requests_total', 
            'Total count of requests', 
            ['method', 'endpoint', 'status']
        )
        
    if REQUEST_LATENCY is None:
        REQUEST_LATENCY = Histogram(
            'kaldra_api_request_duration_seconds', 
            'Request duration in seconds',
            ['method', 'endpoint']
        )


def get_metrics_response() -> bytes:
    """
    Get the current metrics in Prometheus text format.
    Returns empty bytes if prometheus_client is not installed.
    """
    return generate_latest()


def get_metrics_content_type() -> str:
    """
    Return the content type for the metrics response.
    """
    return CONTENT_TYPE_LATEST
