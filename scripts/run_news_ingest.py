import subprocess
import sys

if __name__ == "__main__":
    query = "AI"
    limit = "50"

    if "--query" in sys.argv:
        i = sys.argv.index("--query")
        query = sys.argv[i+1]

    if "--limit" in sys.argv:
        i = sys.argv.index("--limit")
        limit = sys.argv[i+1]

    cmd = [
        "python",
        "kaldra_data/workers/news_ingest_worker.py",
        "--query", query,
        "--limit", limit
    ]

    print("[KALDRA CLI] Running:", " ".join(cmd))
    subprocess.run(cmd)
