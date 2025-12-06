"""
KALDRA API — Signals Router
REST endpoints for signal operations via Supabase.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from src.data.repositories.signal_repository import SignalRepository
from ..dependencies import get_signal_repository


router = APIRouter()


@router.get("")
async def list_signals(
    domain: Optional[str] = Query(None, description="Filter by domain (alpha, geo, product, safeguard)"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results"),
    repo: SignalRepository = Depends(get_signal_repository),
):
    """
    List signals with optional filters.
    
    Query parameters:
    - domain: Filter by domain type
    - limit: Maximum results (default 20, max 100)
    
    Returns:
    - List of signal objects from Supabase
    """
    result = repo.list_signals(domain=domain, limit=limit)
    
    # Check for errors
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {result.get('message', 'Unknown error')}"
        )
    
    return result


@router.get("/{signal_id}")
async def get_signal(
    signal_id: str,
    repo: SignalRepository = Depends(get_signal_repository),
):
    """
    Get a specific signal by ID.
    
    Path parameters:
    - signal_id: UUID of the signal
    
    Returns:
    - Signal object
    
    Raises:
    - 404: Signal not found
    - 503: Database error
    """
    result = repo.get_signal_by_id(signal_id)
    
    # Check for errors
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {result.get('message', 'Unknown error')}"
        )
    
    # Check if signal exists
    if isinstance(result, list):
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Signal not found")
        return result[0]
    
    return result
