import os
import json
import argparse
from datetime import datetime
from kaldra_data.ingestion.news.mediastack_client import fetch_mediastack_news
from kaldra_data.ingestion.news.gnews_client import fetch_gnews_news


def run_news_ingest(query: str, limit: int):
    """Runs ingestion from both Mediastack and GNews."""
    mediastack_key = os.getenv("MEDIASTACK_API_KEY")
    gnews_key = os.getenv("GNEWS_API_KEY")

    if not mediastack_key and not gnews_key:
        raise RuntimeError("Missing API keys for news ingestion")

    print(f"[KALDRA NEWS WORKER] Starting ingestion for: {query}")

    all_articles = []

    if mediastack_key:
        try:
            ms_articles = fetch_mediastack_news(query=query, limit=limit)
            all_articles.extend(ms_articles)
            print(f"[KALDRA NEWS WORKER] Mediastack OK: {len(ms_articles)} items")
        except Exception as e:
            print("[ERROR] Mediastack failed:", e)

    if gnews_key:
        try:
            gn_articles = fetch_gnews_news(query=query, limit=limit)
            all_articles.extend(gn_articles)
            print(f"[KALDRA NEWS WORKER] GNews OK: {len(gn_articles)} items")
        except Exception as e:
            print("[ERROR] GNews failed:", e)

    # Save results
    date_str = datetime.utcnow().strftime("%Y%m%d")
    out_dir = f"data/news/raw/{date_str}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/{query.replace(' ','_')}.jsonl"

    with open(out_path, "w") as f:
        for a in all_articles:
            f.write(json.dumps(a) + "\n")

    print(f"[KALDRA NEWS WORKER] Saved {len(all_articles)} articles to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KALDRA News Ingestion Worker")
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    run_news_ingest(args.query, args.limit)
