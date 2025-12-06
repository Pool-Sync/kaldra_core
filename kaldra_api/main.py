"""
KALDRA API Gateway — Main Entry Point
FastAPI application serving KALDRA Engine endpoints.
"""
from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from .routers import (
    router_status,
    router_engine,
    router_alpha,
    router_geo,
    router_product,
    router_safeguard,
    router_news,
    router_v3_1,  # v3.1 API endpoints
    router_signals,  # Supabase signals
    router_story_events,  # Supabase story events
)

# Initialize FastAPI app
app = FastAPI(
    title="KALDRA API Gateway",
    description="REST API for KALDRA symbolic intelligence engine",
    version="2.1.0",
)

# Configure CORS - permissive mode for development & multi-frontend support
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://4iam.ai",
    "https://www.4iam.ai",
    "https://4iam-frontend.vercel.app",
]

# Add custom frontend URL if provided (for production)
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url and frontend_url not in origins:
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="https?://.*",  # <- aceita qualquer origem http/https
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


@app.get("/health/supabase", tags=["status"])
async def health_supabase():
    """
    Supabase connectivity health check.
    
    Attempts to query signals table to verify database connection.
    
    Returns:
    - 200: Connection OK
    - 503: Connection failed
    """
    from .dependencies import get_signal_repository
    
    try:
        repo = get_signal_repository()
        result = repo.list_signals(limit=1)
        
        # Check for errors
        if isinstance(result, dict) and "error" in result:
            return {
                "status": "error",
                "message": result.get("message", "Unknown database error")
            }
        
        count = len(result) if isinstance(result, list) else 0
        return {
            "status": "ok",
            "supabase_connected": True,
            "signals_sample_count": count
        }
    
    except Exception as e:
        return {
            "status": "error",
            "supabase_connected": False,
            "error": str(e)
        }


# Include routers
app.include_router(router_status.router, prefix="/status", tags=["Status"])
app.include_router(router_engine.router, prefix="/engine", tags=["Engine"])
app.include_router(router_alpha.router, prefix="/alpha", tags=["Alpha"])
app.include_router(router_geo.router, prefix="/geo", tags=["GEO"])
app.include_router(router_product.router, prefix="/product", tags=["Product"])
app.include_router(router_safeguard.router, prefix="/safeguard", tags=["Safeguard"])
app.include_router(router_news.router, prefix="/kaldra", tags=["News"])
app.include_router(router_v3_1.router, prefix="/api", tags=["v3.1"])  # v3.1 API

# Supabase integration endpoints
app.include_router(router_signals.router, prefix="/signals", tags=["Signals"])
app.include_router(router_story_events.router, prefix="/story-events", tags=["Story Events"])
