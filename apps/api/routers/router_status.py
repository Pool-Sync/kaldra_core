"""
Module: router_status
Part of: KALDRA API Gateway
Status: Structural placeholder (no logic implemented)

Description:
    Status and health check endpoints.

Notes:
    - Do not implement real logic.
    - Keep architecture clean.
    - Routes and methods should be empty.
"""

from fastapi import APIRouter, Depends, Response
from ..middleware.rate_limiter import rate_limit_dependency, RateLimiterConfig
from ..monitoring.metrics import get_metrics_response, get_metrics_content_type, register_default_metrics

# Initialize metrics
register_default_metrics()

router = APIRouter()

# Configure rate limiter for status endpoints
status_rate_limiter = rate_limit_dependency(
    RateLimiterConfig(requests=10, per_seconds=60, key_prefix="status")
)

@router.get(
    "/",
    dependencies=[Depends(status_rate_limiter)]
)
def status():
    """
    Health check endpoint.
    
    Returns:
        dict: Status information
    """
    return {"status": "KALDRA API Gateway online", "version": "0.1.0"}


@router.get("/metrics")
def metrics():
    """
    Expose Prometheus metrics.
    """
    data = get_metrics_response()
    if not data:
        return Response(status_code=503, content=b"Prometheus client not installed")
    return Response(content=data, media_type=get_metrics_content_type())
