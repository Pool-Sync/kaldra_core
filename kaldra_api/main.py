"""
KALDRA API Gateway — Main Entry Point
FastAPI application serving KALDRA Engine endpoints.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from .routers import (
    router_status,
    router_engine,
    router_alpha,
    router_geo,
    router_product,
    router_safeguard
)

# Initialize FastAPI app
app = FastAPI(
    title="KALDRA API Gateway",
    description="REST API for KALDRA symbolic intelligence engine",
    version="0.1.0",
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://4iam-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
