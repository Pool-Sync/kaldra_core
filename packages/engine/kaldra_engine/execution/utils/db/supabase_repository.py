"""
Supabase Repository Layer.

Provides data access methods for Supabase tables.
"""

from typing import Any

from kaldra_engine.domain.models.profile import Profile
from kaldra_engine.domain.models.signal_record import SignalRecord
from kaldra_engine.domain.models.story_event_record import StoryEventRecord
from kaldra_engine.execution.utils.supabase_client import get_supabase


class SupabaseRepository:
    """
    Repository for Supabase database operations.

    Example:
        >>> repo = SupabaseRepository()
        >>> signals = repo.list_signals(domain="alpha")
    """

    def __init__(self):
        """Initialize repository with Supabase client."""
        self.client = get_supabase()

    # ========== Generic Methods ==========

    def fetch_table(self, table: str) -> list[dict[str, Any]]:
        """
        Fetch all records from a table.

        Args:
            table: Table name

        Returns:
            List of records
        """
        return self.client.table(table).select("*").execute().data

    def fetch_by_id(self, table: str, record_id: str) -> dict[str, Any] | None:
        """
        Fetch single record by ID.

        Args:
            table: Table name
            record_id: Record ID

        Returns:
            Record dict or None
        """
        result = self.client.table(table).select("*").eq("id", record_id).single().execute()
        return result.data

    # ========== Profiles ==========

    def list_profiles(self) -> list[Profile]:
        """
        List all profiles.

        Returns:
            List of Profile objects
        """
        result = self.client.table("profiles").select("*").execute()
        items = result.data or []
        return [Profile(**item) for item in items]

    # ========== Signals ==========

    def list_signals(self, domain: str | None = None, limit: int = 50) -> list[SignalRecord]:
        """
        List signals with optional filtering.

        Args:
            domain: Filter by domain (alpha, geo, product, safeguard)
            limit: Maximum number of records

        Returns:
            List of SignalRecord objects
        """
        query = self.client.table("signals").select("*").order("created_at", desc=True).limit(limit)
        if domain:
            query = query.eq("domain", domain)
        result = query.execute()
        items = result.data or []
        return [SignalRecord(**item) for item in items]

    def get_signal(self, signal_id: str) -> SignalRecord | None:
        """
        Get single signal by ID.

        Args:
            signal_id: Signal ID

        Returns:
            SignalRecord or None
        """
        result = self.client.table("signals").select("*").eq("id", signal_id).single().execute()
        if not result.data:
            return None
        return SignalRecord(**result.data)

    # ========== Story Events ==========

    def list_story_events_for_signal(self, signal_id: str, limit: int = 100) -> list[StoryEventRecord]:
        """
        List story events for a specific signal.

        Args:
            signal_id: Parent signal ID
            limit: Maximum number of records

        Returns:
            List of StoryEventRecord objects
        """
        result = (
            self.client.table("story_events")
            .select("*")
            .eq("signal_id", signal_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        items = result.data or []
        return [StoryEventRecord(**item) for item in items]
