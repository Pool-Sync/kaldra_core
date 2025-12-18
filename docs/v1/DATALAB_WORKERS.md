# KALDRA Data Lab — Workers

## Overview
Workers are background services that ingest, preprocess and enrich external data sources for the KALDRA Engine.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    External Data Sources                    │
│  (News APIs, Social Media, Financial Data, Product Reviews) │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   KALDRA Data Lab Workers                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  News Ingest Worker                                  │   │
│  │  - Fetches news articles                            │   │
│  │  - Logs ingestion events                            │   │
│  │  - Runs continuously                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Future Workers (GEO, Product, Safeguard)           │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Storage Layer                       │
│              (JSONL files, future: Database)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  KALDRA Master Engine                       │
│            (Processes ingested data into signals)           │
└─────────────────────────────────────────────────────────────┘
```

---

## Worker Lifecycle

1. **Initialization**: Worker starts and initializes logging
2. **Fetch Loop**: Continuously fetches data from external sources
3. **Processing**: Validates and structures incoming data
4. **Storage**: Saves data to designated storage location
5. **Logging**: Records ingestion metrics and errors
6. **Sleep**: Waits for configured interval before next fetch
7. **Repeat**: Returns to step 2

---

## Current Worker: News Ingest Worker

**Path**: `kaldra_data/workers/news_ingest_worker.py`

### Purpose
Responsible for:
- Fetching news articles (currently placeholder API)
- Logging ingestion events
- Running in continuous mode for real-time data ingestion
- Error handling and graceful degradation

### Implementation
```python
def fetch_news() -> List[Dict]:
    """
    Placeholder news fetch.
    Replace with real API connectors in future versions.
    """
    return [
        {"title": "Example News", "content": "This is a placeholder for real ingestion."}
    ]

def run():
    logging.info("Starting News Ingest Worker...")
    while True:
        items = fetch_news()
        logging.info(f"Ingested {len(items)} items.")
        time.sleep(60)  # Fetch every 60 seconds
```

### Configuration
- **Fetch Interval**: 60 seconds
- **Data Format**: JSON dictionaries
- **Logging Level**: INFO
- **Error Handling**: Try-catch with logging (future enhancement)

---

## Running Locally

### Prerequisites
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Start Worker
```bash
python scripts/run_news_ingest.py
```

### Expected Output
```
INFO:root:Starting News Ingest Worker...
INFO:root:Ingested 1 items.
INFO:root:Ingested 1 items.
...
```

### Stop Worker
Press `Ctrl+C` to gracefully stop the worker.

---

## Render Deployment

### Configuration
The worker has a **commented configuration block** inside `render.yaml`:

```yaml
# ================================
# KALDRA NEWS INGEST WORKER (optional)
# ================================
# workers:
#   - name: kaldra-news-worker
#     type: worker
#     runtime: python3
#     envVars:
#       PYTHON_VERSION: 3.11
#     buildCommand: "pip install -r requirements.txt"
#     startCommand: "python scripts/run_news_ingest.py"
#     plan: starter
```

### Activation Steps
1. **Uncomment** the worker section in `render.yaml`
2. **Commit and push** changes to `main` branch
3. **Deploy** via Render dashboard
4. **Monitor** worker logs in Render dashboard

### Monitoring
- View logs: Render Dashboard → Workers → kaldra-news-worker → Logs
- Check status: Verify worker is "Running"
- Monitor metrics: CPU, Memory usage in dashboard

---

## Future Workers

### GEO Speech Ingest Worker
**Purpose**: Ingest geopolitical speeches, press releases, and diplomatic communications

**Data Sources**:
- UN speeches
- Government press releases
- Diplomatic cables (public)
- Think tank reports

**File**: `kaldra_data/workers/geo_ingest_worker.py` (planned)

---

### Product Review Ingest Worker
**Purpose**: Ingest product reviews and user feedback

**Data Sources**:
- Amazon reviews
- G2 reviews
- Capterra reviews
- Reddit product discussions
- YouTube product reviews

**File**: `kaldra_data/workers/product_ingest_worker.py` (planned)

---

### Safeguard Threat Monitor Worker
**Purpose**: Monitor for coordinated inauthentic behavior and disinformation

**Data Sources**:
- Twitter/X (bot detection)
- Reddit (astroturfing detection)
- Fact-checking databases
- Known disinformation campaigns

**File**: `kaldra_data/workers/safeguard_ingest_worker.py` (planned)

---

### High-Frequency TW369 Narrative Drift Worker
**Purpose**: Real-time narrative drift detection using TW369 engine

**Data Sources**:
- Live news feeds
- Social media streams
- Breaking news alerts

**File**: `kaldra_data/workers/tw369_drift_worker.py` (planned)

---

## Future Implementations

### Real Data Source Integration
- [ ] Connect to NewsAPI for real news ingestion
- [ ] Integrate with GDELT for geopolitical events
- [ ] Add Bloomberg API for financial news
- [ ] Implement RSS feed aggregation
- [ ] Add social media APIs (Twitter, Reddit)

### Persistence Layer
- [ ] PostgreSQL database integration
- [ ] Firestore for real-time sync
- [ ] S3 for raw data archival
- [ ] Redis for caching

### Pipeline Enhancements
- [ ] Embedding generation during ingestion
- [ ] Real-time preprocessing
- [ ] Deduplication logic
- [ ] Entity extraction (NER)

### Integration
- [ ] Direct integration with KALDRA Core via API Gateway
- [ ] Webhook notifications for new data
- [ ] Event-driven architecture
- [ ] Message queue (Kafka/RabbitMQ)

### Scheduling
- [ ] Dynamic scheduler (APScheduler)
- [ ] Cron-based scheduling
- [ ] Priority-based fetching
- [ ] Adaptive fetch intervals

---

## Enhancements (Short/Medium Term)

### Reliability
- [ ] Retry logic with exponential backoff
- [ ] Circuit breaker pattern
- [ ] Health check endpoint
- [ ] Graceful shutdown handling

### Data Quality
- [ ] Cache of already processed articles
- [ ] Duplicate detection
- [ ] Data validation schemas
- [ ] Quality scoring

### Observability
- [ ] Structured logging (JSON format)
- [ ] Prometheus metrics endpoint
- [ ] Grafana dashboards
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring

### Scalability
- [ ] Support for multiple concurrent sources
- [ ] Parallel processing
- [ ] Batch ingestion
- [ ] Rate limiting per source

---

## Research Track (Long Term)

### Streaming Architecture
- [ ] Real-time streaming ingestion of global narrative events
- [ ] Apache Kafka integration
- [ ] Stream processing (Apache Flink)
- [ ] Event sourcing pattern

### TW369 Integration
- [ ] Direct connection to TW369 Drift Engine
- [ ] Real-time drift calculation
- [ ] Anomaly detection triggers
- [ ] Predictive narrative modeling

### Geopolitical Enrichment
- [ ] Named Entity Recognition (NER)
- [ ] Automatic Δ144 archetype mapping
- [ ] Cultural context extraction
- [ ] Geopolitical risk scoring

### Multi-Domain Narrative Modeling
- [ ] Cross-domain narrative tracking
- [ ] Narrative coherence scoring
- [ ] Story-level aggregation
- [ ] Temporal narrative evolution

### Prediction & Anomalies
- [ ] LSTM/Transformer models for news drift
- [ ] Anomaly detection in narrative patterns
- [ ] Predictive alerts
- [ ] Scenario forecasting

### Specialized Models
- [ ] Fine-tuned transformers for news analysis
- [ ] Domain-specific embedding models
- [ ] Custom bias detection models
- [ ] Narrative manipulation detection

---

## Known Limitations

### Current Implementation
- ⚠️ **Mock Data Only**: Uses placeholder data, not real news sources
- ⚠️ **No Persistence**: Data not saved to database
- ⚠️ **No Authentication**: No API key management for external sources
- ⚠️ **No Parallelism**: Single-threaded execution
- ⚠️ **Simplified Loop**: Uses basic `while True` without advanced scheduling
- ⚠️ **No Error Recovery**: Limited error handling and retry logic
- ⚠️ **No Monitoring**: No metrics or health checks

### Scalability Constraints
- Single worker instance
- No load balancing
- No distributed processing
- Limited to Render starter plan resources

---

## Testing

### Local Testing
```bash
# Test worker execution
python scripts/run_news_ingest.py

# Verify logs appear
# Expected: "Starting News Ingest Worker..."
# Expected: "Ingested 1 items." (repeating every 60s)
```

### Integration Testing
```bash
# Test with simulated requests (future)
# Test error handling
# Test graceful shutdown (Ctrl+C)
```

### Render Compatibility
- [ ] Verify worker starts successfully on Render
- [ ] Check logs are accessible
- [ ] Confirm continuous operation
- [ ] Test restart behavior

---

## Next Steps

### Immediate (Q1 2026)
1. **Real News API Integration**
   - Integrate NewsAPI for real news ingestion
   - Add API key management
   - Implement rate limiting

2. **Data Lab → API Gateway Integration**
   - Connect ingested data to KALDRA Core
   - Implement data transformation pipeline
   - Add signal generation from ingested data

3. **Worker Monitor Dashboard**
   - Create monitoring UI
   - Display ingestion metrics
   - Show worker health status

4. **Prometheus Metrics**
   - Add metrics endpoint
   - Track ingestion rate
   - Monitor error rates

### Medium Term (Q2 2026)
5. **Additional Workers**
   - Implement GEO ingest worker
   - Implement Safeguard ingest worker
   - Implement Product ingest worker

6. **Database Integration**
   - PostgreSQL for persistent storage
   - Migration scripts
   - Query optimization

7. **Advanced Scheduling**
   - Dynamic fetch intervals
   - Priority-based scheduling
   - Multi-source coordination

---

## Troubleshooting

### Worker Won't Start
**Issue**: Worker fails to start locally

**Solutions**:
- Check Python version (requires 3.11+)
- Verify virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`
- Check for syntax errors in worker file

### No Logs Appearing
**Issue**: Worker runs but no logs visible

**Solutions**:
- Verify logging level is set to INFO
- Check console output
- Ensure `logging.basicConfig()` is called

### Worker Crashes on Render
**Issue**: Worker starts but crashes immediately

**Solutions**:
- Check Render logs for error messages
- Verify `startCommand` in render.yaml is correct
- Ensure all dependencies are in requirements.txt
- Check for missing environment variables

---

## References

- **Worker Implementation**: `kaldra_data/workers/news_ingest_worker.py`
- **Execution Script**: `scripts/run_news_ingest.py`
- **Render Configuration**: `render.yaml`
- **Data Lab Overview**: `docs/core/MASTER_ENGINE_AND_DATALAB_OVERVIEW.md`

---

**End of Workers Documentation**
