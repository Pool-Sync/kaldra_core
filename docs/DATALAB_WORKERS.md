# KALDRA Data Lab — Workers & Jobs

**Version**: 1.0  
**Last Updated**: 2025-11-23  
**Status**: Operational

---

## 🧠 Overview

The **KALDRA Data Lab** is the subsystem responsible for ingesting, processing, and storing raw data from the external world. While the API Gateway serves real-time requests, **Workers** run in the background (typically as scheduled Cron Jobs) to build up the historical dataset that powers KALDRA's long-term memory and trend analysis.

### Core Responsibilities
- **Ingestion**: Fetching data from external APIs (News, Financials, Social).
- **Normalization**: Converting raw payloads into standard KALDRA schemas.
- **Storage**: Saving data to the Data Lake (currently local/container filesystem, future S3/DB).

---

## 📰 News Ingest Worker (v1)

The first operational worker is responsible for aggregating news from multiple providers.

- **Script**: `kaldra_data/workers/news_ingest_worker.py`
- **CLI Wrapper**: `scripts/run_news_ingest.py`
- **Sources**: MediaStack, GNews
- **Output**: JSONL files in `data/news/raw/`

### Output Format
Files are named: `YYYYMMDD_HHMMSS_<query>.jsonl`

```json
{
  "source": "mediastack",
  "timestamp": "2025-11-23T10:00:00Z",
  "title": "AI Breakthrough in Quantum Computing",
  "text": "Researchers have announced...",
  "author": "Jane Doe",
  "url": "https://example.com/news/123",
  "fetched_at": "2025-11-23T14:30:00.123456",
  "ingest_query": "Quantum AI"
}
```

---

## 🚀 How to Run

### 1. Local Development

**Prerequisites**:
Ensure your `.env.local` has valid API keys:
```bash
MEDIASTACK_API_KEY=your_key
GNEWS_API_KEY=your_key
```

**Run Command**:
```bash
# Run from project root
python scripts/run_news_ingest.py --query "Artificial Intelligence" --limit 50
```

**Verify Output**:
Check the `data/news/raw/` directory for the generated `.jsonl` file.

### 2. Production (Render Cron Job)

To run this as a scheduled job on Render:

1. **Create New Cron Job** in Render Dashboard.
2. **Connect Repository**: `Pool-Sync/kaldra_core`.
3. **Configure**:
   - **Name**: `kaldra-news-ingest`
   - **Region**: Oregon (same as API)
   - **Schedule**: `0 */4 * * *` (Every 4 hours)
   - **Command**: `python scripts/run_news_ingest.py --query "AI" --limit 100`
4. **Environment Variables**:
   - Add `MEDIASTACK_API_KEY` and `GNEWS_API_KEY`.

> **Note**: In the current setup (ephemeral container filesystem), data saved to `data/` will be lost when the container restarts. **Next Step**: Implement S3/Cloud Storage upload in the worker for persistence.

---

## 🔮 Future Workers

The Data Lab architecture is designed to be extensible. Planned future workers:

### Earnings Ingest Worker
- **Goal**: Fetch quarterly earnings call transcripts.
- **Source**: Financial APIs (e.g., FMP, AlphaVantage).
- **File**: `kaldra_data/workers/earnings_ingest_worker.py`

### Geopolitics Worker
- **Goal**: Track conflict zones and diplomatic events.
- **Source**: GDELT or specialized news filters.
- **File**: `kaldra_data/workers/geo_ingest_worker.py`

### Product Reviews Worker
- **Goal**: Analyze sentiment on tech product launches.
- **Source**: Reddit, YouTube comments.
- **File**: `kaldra_data/workers/product_reviews_worker.py`

---

## 🛠 Development Guidelines

When creating a new worker:

1. **Create Client**: Implement API client in `kaldra_data/ingestion/<domain>/`.
2. **Create Worker**: Implement logic in `kaldra_data/workers/<name>_worker.py`.
   - Must use `argparse` for configuration.
   - Must use `logging` for observability.
   - Must handle API errors gracefully.
3. **Create CLI**: Add wrapper in `scripts/`.
4. **Document**: Update this file.

---

**Maintained by**: 4IAM.AI Engineering Team
