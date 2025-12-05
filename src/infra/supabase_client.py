"""
Supabase client for KALDRA backend.

Uses SERVICE_ROLE_KEY for backend operations.
"""
import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


def get_supabase() -> Client:
    """
    Get Supabase client with service role key.
    
    Returns:
        Supabase Client instance
    
    Raises:
        RuntimeError: If environment variables are missing
    """
    if not SUPABASE_URL or not SERVICE_ROLE_KEY:
        raise RuntimeError("Supabase environment variables missing.")
    
    return create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
