"""
KALDRA Data Lab — News Ingestion Module
External news API clients for data collection
"""

__all__ = [
    "MediaStackClient",
    "GNewsClient",
]

try:
    from .gnews_client import GNewsClient
    from .mediastack_client import MediaStackClient
except ImportError:
    # Graceful degradation if dependencies not installed
    pass
