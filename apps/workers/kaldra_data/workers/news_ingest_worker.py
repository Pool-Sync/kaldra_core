"""
KALDRA Data Lab — News Ingest Worker
Handles ingestion of news articles for narrative intelligence pipelines.
"""

import logging
import time

logging.basicConfig(level=logging.INFO)


def fetch_news() -> list[dict]:
    """
    Placeholder news fetch.
    Replace with real API connectors in future versions.
    """
    return [
        {
            "title": "Example News",
            "content": "This is a placeholder for real ingestion.",
        }
    ]


def run():
    logging.info("Starting News Ingest Worker...")
    while True:
        items = fetch_news()
        logging.info(f"Ingested {len(items)} items.")
        time.sleep(60)
