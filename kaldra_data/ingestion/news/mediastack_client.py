"""
KALDRA Data Lab — MediaStack News API Client
Fetches news articles from MediaStack API with rate limiting and error handling.
"""
import os
import logging
import time
from typing import List, Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)

class MediaStackClient:
    """
    Client for MediaStack News API
    https://mediastack.com/documentation
    """
    
    BASE_URL = "http://api.mediastack.com/v1/news"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MEDIASTACK_API_KEY")
        if not self.api_key:
            logger.warning("MEDIASTACK_API_KEY not set. Client will not function.")
        
        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Rate limit: 1 request per second
    
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
        languages: str = "en",
        sort: str = "published_desc"
    ) -> List[Dict[str, Any]]:
        """
        Fetch latest news articles matching query
        
        Returns:
            List of normalized articles with keys:
            - source: str
            - timestamp: str (ISO format)
            - text: str
            - author: str
            - url: str
        """
        if not self.api_key:
            logger.error("Cannot fetch: MEDIASTACK_API_KEY not configured")
            return []
        
        self._rate_limit()
        
        params = {
            "access_key": self.api_key,
            "keywords": query,
            "limit": min(limit, 100),  # API max is 100
            "languages": languages,
            "sort": sort,
        }
        
        try:
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if "data" not in data:
                logger.warning(f"Unexpected MediaStack response format: {data}")
                return []
            
            # Normalize to KALDRA format
            articles = []
            for item in data["data"]:
                articles.append({
                    "source": "mediastack",
                    "timestamp": item.get("published_at", ""),
                    "text": item.get("description") or item.get("title", ""),
                    "author": item.get("author", "Unknown"),
                    "url": item.get("url", ""),
                    "title": item.get("title", ""),
                    "category": item.get("category", "general"),
                })
            
            logger.info(f"MediaStack: Fetched {len(articles)} articles for query '{query}'")
            return articles
            
        except requests.exceptions.RequestException as e:
            logger.error(f"MediaStack API error: {e}")
            return []
        except Exception as e:
            logger.exception(f"Unexpected error in MediaStack client: {e}")
            return []
