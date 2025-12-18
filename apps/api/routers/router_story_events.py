"""
KALDRA API — Story Events Router
REST endpoints for story events operations via Supabase.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from src.data.repositories.story_event_repository import StoryEventRepository
from ..dependencies import get_story_event_repository


router = APIRouter()


@router.get("/by-signal/{signal_id}")
async def list_events_by_signal(
    signal_id: str,
    limit: int = Query(50, ge=1, le=200, description="Maximum number of results"),
    repo: StoryEventRepository = Depends(get_story_event_repository),
):
    """
    List story events for a specific signal.
    
    Path parameters:
    - signal_id: UUID of the parent signal
    
    Query parameters:
    - limit: Maximum results (default 50, max 200)
    
    Returns:
    - List of story event objects
    """
    result = repo.list_events(signal_id=signal_id, limit=limit)
    
    # Check for errors
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {result.get('message', 'Unknown error')}"
        )
    
    return result


@router.get("")
async def list_events(
    stream_id: Optional[str] = Query(None, description="Filter by stream ID"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of results"),
    repo: StoryEventRepository = Depends(get_story_event_repository),
):
    """
    List story events with optional filters.
    
    Query parameters:
    - stream_id: Filter by stream identifier
    - limit: Maximum results (default 50, max 200)
    
    Returns:
    - List of story event objects
    """
    result = repo.list_events(stream_id=stream_id, limit=limit)
    
    # Check for errors
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {result.get('message', 'Unknown error')}"
        )
    
    return result
