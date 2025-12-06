"""
Story Event Repository for KALDRA.

Handles persistence of narrative events to Supabase.
"""
from typing import Any, Dict, List, Optional
from src.infrastructure.supabase_client import SupabaseClient


class StoryEventRepository:
    """
    Repository for story_events table operations.
    
    Manages narrative events associated with signals.
    """
    
    def __init__(self, client: Optional[SupabaseClient] = None) -> None:
        """
        Initialize repository.
        
        Args:
            client: Optional SupabaseClient instance (for testing)
        """
        self.client = client or SupabaseClient()
        self.table = "story_events"
    
    # ========== Read Operations ==========
    
    def list_events(
        self,
        signal_id: Optional[str] = None,
        stream_id: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """
        List story events with optional filtering.
        
        Args:
            signal_id: Filter by parent signal ID
            stream_id: Filter by stream ID
            limit: Maximum number of results
        
        Returns:
            List of events or error dict
        """
        params = f"select=*&limit={limit}&order=created_at.desc"
        
        if signal_id:
            params += f"&signal_id=eq.{signal_id}"
        if stream_id:
            params += f"&stream_id=eq.{stream_id}"
        
        return self.client.fetch(self.table, params)
    
    # ========== Write Operations ==========
    
    def create_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a single story event.
        
        Expected fields:
        - signal_id (uuid, optional)
        - stream_id (str, optional)
        - text (str, optional)
        - delta144_state (str, optional)
        - polarities (jsonb, optional)
        - meta (jsonb, optional)
        
        Args:
            data: Event data
        
        Returns:
            Created event or error dict
        """
        return self.client.insert(self.table, data)
    
    def bulk_create_events(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple story events in batch.
        
        Args:
            events: List of event data dicts
        
        Returns:
            Created events or error dict
        """
        if not events:
            return []
        
        # Note: Supabase REST API supports array inserts
        # The client's insert method should handle this
        return self.client.insert(self.table, events)
    
    # ========== Delete Operations ==========
    
    def delete_event(self, event_id: str) -> Dict[str, Any]:
        """
        Delete a single event by ID.
        
        Args:
            event_id: Event UUID
        
        Returns:
            Success response or error dict
        """
        return self.client.delete(self.table, {"id": event_id})
    
    def delete_by_signal(self, signal_id: str) -> Dict[str, Any]:
        """
        Delete all events for a given signal.
        
        Args:
            signal_id: Signal UUID
        
        Returns:
            Success response or error dict
        """
        return self.client.delete(self.table, {"signal_id": signal_id})
