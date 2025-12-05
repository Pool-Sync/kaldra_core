"""
Signals endpoint for Supabase integration.
"""
from fastapi import APIRouter, Query
from typing import Optional, List
from src.infra.db.supabase_repository import SupabaseRepository
from src.domain.models.signal_record import SignalRecord

router = APIRouter()
repo = SupabaseRepository()


@router.get("/signals", response_model=List[dict])
def list_signals(domain: Optional[str] = Query(None), limit: int = 50):
    """
    List signals from Supabase.
    
    Args:
        domain: Filter by domain (alpha, geo, product, safeguard)
        limit: Maximum number of records (default: 50)
    
    Returns:
        List of signal dictionaries
    """
    signals = repo.list_signals(domain=domain, limit=limit)
    # Return as dict for JSON serialization
    return [s.__dict__ for s in signals]


@router.get("/signals/{signal_id}", response_model=dict)
def get_signal(signal_id: str):
    """
    Get single signal by ID.
    
    Args:
        signal_id: Signal UUID
    
    Returns:
        Signal dictionary or 404
    """
    signal = repo.get_signal(signal_id)
    if not signal:
        return {"error": "Signal not found"}
    return signal.__dict__


@router.get("/signals/{signal_id}/events", response_model=List[dict])
def list_story_events(signal_id: str, limit: int = 100):
    """
    List story events for a signal.
    
    Args:
        signal_id: Signal UUID
        limit: Maximum number of events
    
    Returns:
        List of story event dictionaries
    """
    events = repo.list_story_events_for_signal(signal_id, limit=limit)
    return [e.__dict__ for e in events]
