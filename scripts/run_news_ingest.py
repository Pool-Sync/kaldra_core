#!/usr/bin/env python3
"""
CLI Wrapper for KALDRA News Ingestion Worker.
Usage: python scripts/run_news_ingest.py --query "AI" --limit 50
"""
import sys
import os
import argparse

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaldra_data.workers.news_ingest_worker import run_news_ingest

def main():
    parser = argparse.ArgumentParser(description="Run KALDRA News Ingestion")
    parser.add_argument("--query", type=str, required=True, help="Topic to search for")
    parser.add_argument("--limit", type=int, default=50, help="Max articles per source")
    parser.add_argument("--sources", type=str, help="Comma-separated sources (e.g. mediastack,gnews)")
    
    args = parser.parse_args()
    
    sources = args.sources.split(",") if args.sources else None
    
    print(f"🚀 Starting KALDRA News Ingestion for query: '{args.query}'")
    
    try:
        result = run_news_ingest(query=args.query, limit=args.limit, sources=sources)
        
        print("\n✅ Ingestion Complete!")
        print(f"   Total Articles: {result['total_fetched']}")
        print(f"   Saved File:     {result['saved_path']}")
        print(f"   Duration:       {result['duration_seconds']}s")
        
        if result['total_fetched'] == 0:
            sys.exit(1) # Exit with error if no data found
            
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
