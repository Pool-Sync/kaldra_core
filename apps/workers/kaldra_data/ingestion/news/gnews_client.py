"""
KALDRA Data Lab — GNews API Client
Fetches news articles from GNews API with rate limiting and error handling.
"""
import os
import logging
import time
from typing import List, Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)

class GNewsClient:
    """
    Client for GNews API
    https://gnews.io/docs/v4
    """
    
    BASE_URL = "https://gnews.io/api/v4/search"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GNEWS_API_KEY")
        if not self.api_key:
            logger.warning("GNEWS_API_KEY not set. Client will not function.")
        
        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Rate limit
    
    def _rate_limit(self):
        """Enforce rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def fetch_latest(
        self,
        query: str,
        limit: int = 20,
        lang: str = "en",
        country: str = "us"
    ) -> List[Dict[str, Any]]:
        """
        Fetch latest news articles matching query
        
        Returns:
            List of normalized articles
        """
        if not self.api_key:
            logger.error("Cannot fetch: GNEWS_API_KEY not configured")
            return []
        
        self._rate_limit()
        
        params = {
            "q": query,
            "token": self.api_key,
            "lang": lang,
            "country": country,
            "max": min(limit, 100),
        }
        
        try:
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if "articles" not in data:
                logger.warning(f"Unexpected GNews response format: {data}")
                return []
            
            # Normalize to KALDRA format
            articles = []
            for item in data["articles"]:
                articles.append({
                    "source": "gnews",
                    "timestamp": item.get("publishedAt", ""),
                    "text": item.get("description") or item.get("title", ""),
                    "author": item.get("source", {}).get("name", "Unknown"),
                    "url": item.get("url", ""),
                    "title": item.get("title", ""),
                })
            
            logger.info(f"GNews: Fetched {len(articles)} articles for query '{query}'")
            return articles
            
        except requests.exceptions.RequestException as e:
            logger.error(f"GNews API error: {e}")
            return []
        except Exception as e:
            logger.exception(f"Unexpected error in GNews client: {e}")
            return []
