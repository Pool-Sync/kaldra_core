"""
KALDRA API — News Aggregation Router
Aggregates news from multiple external APIs (MediaStack, GNews)
"""
from __future__ import annotations

import logging
from typing import List, Dict, Any
from fastapi import APIRouter, Query

logger = logging.getLogger(__name__)
router = APIRouter()

# Import news clients (will fail gracefully if dependencies not installed)
try:
    from kaldra_data.ingestion.news.mediastack_client import MediaStackClient
    from kaldra_data.ingestion.news.gnews_client import GNewsClient
    CLIENTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"News clients not available: {e}")
    CLIENTS_AVAILABLE = False


@router.get(
    "/news",
    summary="Aggregate news from multiple sources",
    description="Fetches and aggregates news articles from MediaStack and GNews APIs"
)
def get_aggregated_news(
    query: str = Query(..., description="Search query for news articles"),
    limit: int = Query(20, ge=1, le=100, description="Max articles per source")
) -> Dict[str, Any]:
    """
    Aggregate news from multiple external APIs
    
    Returns:
        {
            "query": str,
            "total_articles": int,
            "sources": List[str],
            "articles": List[Dict]
        }
    """
    if not CLIENTS_AVAILABLE:
        return {
            "query": query,
            "total_articles": 0,
            "sources": [],
            "articles": [],
            "error": "News API clients not configured. Please install dependencies and set API keys."
        }
    
    all_articles: List[Dict[str, Any]] = []
    sources_used: List[str] = []
    
    # Fetch from MediaStack
    try:
        mediastack = MediaStackClient()
        ms_articles = mediastack.fetch_latest(query, limit=limit)
        if ms_articles:
            all_articles.extend(ms_articles)
            sources_used.append("mediastack")
            logger.info(f"MediaStack contributed {len(ms_articles)} articles")
    except Exception as e:
        logger.error(f"MediaStack fetch failed: {e}")
    
    # Fetch from GNews
    try:
        gnews = GNewsClient()
        gn_articles = gnews.fetch_latest(query, limit=limit)
        if gn_articles:
            all_articles.extend(gn_articles)
            sources_used.append("gnews")
            logger.info(f"GNews contributed {len(gn_articles)} articles")
    except Exception as e:
        logger.error(f"GNews fetch failed: {e}")
    
    # Sort by timestamp (most recent first)
    all_articles.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    return {
        "query": query,
        "total_articles": len(all_articles),
        "sources": sources_used,
        "articles": all_articles,
    }
