"""
KALDRA Data Lab — News Ingestion Worker
Worker script to fetch, normalize, and save news data from external APIs.
Designed to be run as a scheduled job (cron) on Render.
"""
import os
import json
import time
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Import clients
from kaldra_data.ingestion.news.mediastack_client import MediaStackClient
from kaldra_data.ingestion.news.gnews_client import GNewsClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("NewsIngestWorker")

def save_articles(articles: List[Dict[str, Any]], query: str, output_dir: str = "data/news/raw") -> str:
    """
    Save articles to a JSONL file.
    
    Args:
        articles: List of normalized article dictionaries
        query: Search query used (for filename)
        output_dir: Directory to save the file
        
    Returns:
        Path to the saved file
    """
    if not articles:
        logger.warning("No articles to save.")
        return ""
        
    # Create directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate filename: YYYYMMDD_HHMMSS_<query>.jsonl
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
    filename = f"{timestamp}_{safe_query}.jsonl"
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for article in articles:
                # Add fetched_at timestamp
                article["fetched_at"] = datetime.utcnow().isoformat()
                article["ingest_query"] = query
                f.write(json.dumps(article, ensure_ascii=False) + "\n")
        
        logger.info(f"Saved {len(articles)} articles to {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Failed to save articles to {filepath}: {e}")
        return ""

def run_news_ingest(query: str, limit: int = 50, sources: List[str] = None) -> Dict[str, Any]:
    """
    Main execution logic for news ingestion.
    
    Args:
        query: Search term
        limit: Max articles per source
        sources: List of sources to use (['mediastack', 'gnews']). If None, uses all.
        
    Returns:
        Summary dictionary
    """
    start_time = time.time()
    logger.info(f"Starting news ingestion for query='{query}', limit={limit}, sources={sources}")
    
    if sources is None:
        sources = ["mediastack", "gnews"]
    
    all_articles = []
    
    # 1. Fetch from MediaStack
    if "mediastack" in sources:
        try:
            ms_client = MediaStackClient()
            if ms_client.api_key:
                logger.info("Fetching from MediaStack...")
                ms_articles = ms_client.fetch_latest(query=query, limit=limit)
                all_articles.extend(ms_articles)
            else:
                logger.warning("Skipping MediaStack: API key not found")
        except Exception as e:
            logger.error(f"Error fetching from MediaStack: {e}")

    # 2. Fetch from GNews
    if "gnews" in sources:
        try:
            gn_client = GNewsClient()
            if gn_client.api_key:
                logger.info("Fetching from GNews...")
                gn_articles = gn_client.fetch_latest(query=query, limit=limit)
                all_articles.extend(gn_articles)
            else:
                logger.warning("Skipping GNews: API key not found")
        except Exception as e:
            logger.error(f"Error fetching from GNews: {e}")
            
    # 3. Save results
    saved_path = ""
    if all_articles:
        saved_path = save_articles(all_articles, query)
    else:
        logger.warning("No articles fetched from any source.")
        
    duration = time.time() - start_time
    summary = {
        "status": "success" if all_articles else "warning",
        "total_fetched": len(all_articles),
        "saved_path": saved_path,
        "duration_seconds": round(duration, 2)
    }
    
    logger.info(f"Ingestion complete. Summary: {summary}")
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KALDRA News Ingestion Worker")
    parser.add_argument("--query", type=str, required=True, help="Search query for news")
    parser.add_argument("--limit", type=int, default=50, help="Max articles per source")
    parser.add_argument("--sources", type=str, help="Comma-separated list of sources (mediastack,gnews)")
    
    args = parser.parse_args()
    
    source_list = args.sources.split(",") if args.sources else None
    
    run_news_ingest(query=args.query, limit=args.limit, sources=source_list)
