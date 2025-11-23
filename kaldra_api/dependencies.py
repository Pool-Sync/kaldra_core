"""
KALDRA API Gateway — Dependency Injection
Provides singleton instances of core engines for FastAPI routers.
"""
from functools import lru_cache
from src.core.kaldra_master_engine import KaldraMasterEngineV2

@lru_cache()
def get_master_engine() -> KaldraMasterEngineV2:
    """
    Returns a singleton instance of the KALDRA Master Engine V2.
    
    This function is cached to ensure only one engine instance is created
    during the lifetime of the API process.
    """
    return KaldraMasterEngineV2(d_ctx=256, tau=0.65)
