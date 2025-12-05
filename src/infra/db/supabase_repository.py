"""
Supabase Repository Layer.

Provides data access methods for Supabase tables.
"""
from typing import Any, Dict, List, Optional
from src.infra.supabase_client import get_supabase


class SupabaseRepository:
    """
    Repository for Supabase database operations.
    
    Example:
        >>> repo = SupabaseRepository()
        >>> profiles = repo.fetch_table("profiles")
    """
    
    def __init__(self):
        """Initialize repository with Supabase client."""
        self.client = get_supabase()
    
    def fetch_table(self, table: str) -> List[Dict[str, Any]]:
        """
        Fetch all records from a table.
        
        Args:
            table: Table name
        
        Returns:
            List of records
        """
        return self.client.table(table).select("*").execute().data
    
    def fetch_by_id(self, table: str, record_id: str) -> Optional[Dict[str, Any]]:
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
