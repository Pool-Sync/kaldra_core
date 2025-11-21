"""
KALDRA API — Main FastAPI application.
"""
from __future__ import annotations

from fastapi import FastAPI

# Import routers
from .routers import (
    router_status,
    router_engine,
    router_alpha,
    router_geo,
    router_product,
    router_safeguard
)

app = FastAPI(
    title="KALDRA API Gateway",
    version="0.1.0",
)


@app.get("/health", tags=["status"])
def health_check() -> dict:
    """
    Basic health endpoint.
    """
    return {"status": "ok"}


# Include routers
app.include_router(router_status.router, prefix="/status", tags=["Status"])
app.include_router(router_engine.router, prefix="/engine", tags=["Engine"])
app.include_router(router_alpha.router, prefix="/alpha", tags=["Alpha"])
app.include_router(router_geo.router, prefix="/geo", tags=["GEO"])
app.include_router(router_product.router, prefix="/product", tags=["Product"])
app.include_router(router_safeguard.router, prefix="/safeguard", tags=["Safeguard"])
