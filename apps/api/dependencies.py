"""
KALDRA API Gateway — Dependency Injection
Provides singleton instances of core engines for FastAPI routers.
"""
from functools import lru_cache
from kaldra_engine.core.kaldra_master_engine import KaldraMasterEngineV2
from kaldra_engine.data.repositories.signal_repository import SignalRepository
from kaldra_engine.data.repositories.story_event_repository import StoryEventRepository

@lru_cache()
def get_master_engine() -> KaldraMasterEngineV2:
    """
    Returns a singleton instance of the KALDRA Master Engine V2.
    
    This function is cached to ensure only one engine instance is created
    during the lifetime of the API process.
    """
    return KaldraMasterEngineV2(d_ctx=256, tau=0.65)


def get_signal_repository() -> SignalRepository:
    """
    Returns a SignalRepository instance for signal persistence operations.
    """
    return SignalRepository()


def get_story_event_repository() -> StoryEventRepository:
    """
    Returns a StoryEventRepository instance for story events persistence operations.
    """
    return StoryEventRepository()
