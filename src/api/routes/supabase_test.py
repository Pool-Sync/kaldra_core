"""
Supabase test endpoint.
"""
from fastapi import APIRouter
from src.infra.db.supabase_repository import SupabaseRepository

router = APIRouter()


@router.get("/supabase/test")
def test_supabase():
    """
    Test Supabase connection.
    
    Returns:
        Status dict with row count or error
    """
    repo = SupabaseRepository()
    try:
        result = repo.fetch_table("profiles")  # Empty table for testing
        return {"status": "ok", "rows": len(result)}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
