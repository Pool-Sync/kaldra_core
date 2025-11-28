# KALDRA API Gateway - Technical Walkthrough

**Version**: 2.1  
**Last Updated**: 2025-11-23  
**Status**: Production Ready

---

## Overview

The KALDRA API Gateway is a FastAPI-based REST service that exposes the KALDRA Master Engine V2 symbolic intelligence capabilities through HTTP endpoints. It serves as the primary integration point for the 4IAM.AI frontend and external clients.

---

## Architecture

### Components

```
kaldra_api/
├── main.py                 # FastAPI app initialization
├── dependencies.py         # Dependency injection (Master Engine singleton)
├── schemas/
│   └── signal.py          # Pydantic request/response models
└── routers/
    ├── router_engine.py   # KALDRA signal generation
    ├── router_news.py     # News aggregation
    └── router_status.py   # Health checks
```

### Technology Stack

- **Framework**: FastAPI 0.121+
- **Server**: Uvicorn (ASGI)
- **Validation**: Pydantic v2
- **CORS**: Enabled for frontend integration
- **Logging**: Python logging with structured fields

---

## Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{"status": "ok"}
```

**Use Case**: Load balancer health checks, monitoring

---

### 2. KALDRA Signal Generation

**Endpoint**: `POST /engine/kaldra/signal`

**Request**:
```json
{
  "text": "Artificial intelligence is transforming society"
}
```

**Response**:
```json
{
  "archetype": "A08_REBEL",
  "delta_state": "A08_REBEL_6_05",
  "tw_regime": "STABLE",
  "kindra_distribution": [
    {"state_index": 89, "prob": 0.007152},
    {"state_index": 127, "prob": 0.007111},
    {"state_index": 120, "prob": 0.007108},
    {"state_index": 121, "prob": 0.007084},
    {"state_index": 97, "prob": 0.007082}
  ],
  "bias_score": 0.1,
  "bias_label": "neutral",
  "narrative_risk": 0.34,
  "confidence": 0.0,
  "explanation": "Master Engine V2: INCONCLUSIVO",
  "meta_modifiers": {}
}
```

**Fields**:
- `archetype`: Real archetype ID from Delta144 (e.g., "A08_REBEL")
- `delta_state`: Specific state within archetype (e.g., "A08_REBEL_6_05")
- `tw_regime`: Tracy-Widom anomaly detection ("STABLE" | "ANOMALY")
- `kindra_distribution`: Top-5 archetype states with probabilities
- `bias_score`: Text bias score [0.0, 1.0]
- `bias_label`: Bias classification (neutral/moderate/negative/extreme)
- `narrative_risk`: Composite risk score [0.0, 1.0]
- `confidence`: Epistemic confidence [0.0, 1.0]
- `explanation`: Human-readable status
- `meta_modifiers`: Future use (currently empty)

**Processing Pipeline**:
1. Text validation
2. Bias detection (keyword + heuristics)
3. Embedding generation (placeholder: hash-based)
4. Master Engine V2 inference:
   - Delta144 semantic matching
   - Kindra cultural modulation
   - TW-Painlevé anomaly detection
   - Epistemic limiting (τ layer)
5. Narrative risk calculation
6. Response serialization

**Performance**: ~500ms average

---

### 3. News Aggregation

**Endpoint**: `GET /kaldra/news?query=AI&limit=20`

**Parameters**:
- `query` (required): Search query string
- `limit` (optional): Max articles per source (default: 20, max: 100)

**Response**:
```json
{
  "query": "AI",
  "total_articles": 10,
  "sources": ["mediastack", "gnews"],
  "articles": [
    {
      "source": "mediastack",
      "timestamp": "2025-11-23T09:05:49+00:00",
      "text": "Article description...",
      "author": "Author Name",
      "url": "https://...",
      "title": "Article Title",
      "category": "technology"
    }
  ]
}
```

**External APIs**:
- **MediaStack**: News API (500 req/month free tier)
- **GNews**: Global news aggregator

**Features**:
- Rate limiting (1 req/sec per source)
- Timestamp-based sorting (most recent first)
- Normalized output format
- Graceful error handling

**Performance**: ~2-3s (external API latency)

---

## Dependency Injection

### Master Engine Singleton

**File**: `kaldra_api/dependencies.py`

```python
from functools import lru_cache
from src.core.kaldra_master_engine import KaldraMasterEngineV2

@lru_cache()
def get_master_engine() -> KaldraMasterEngineV2:
    """
    Singleton instance of KALDRA Master Engine V2.
    Initialized once and reused across requests.
    """
    return KaldraMasterEngineV2.from_default_files(
        d_ctx=256,
        tau=0.65
    )
```

**Benefits**:
- Single engine instance (resource efficient)
- Lazy initialization
- Thread-safe (FastAPI handles concurrency)

**Usage in Routers**:
```python
from fastapi import Depends
from ..dependencies import get_master_engine

@router.post("/kaldra/signal")
def generate_signal(
    payload: KaldraSignalRequest,
    engine: KaldraMasterEngineV2 = Depends(get_master_engine)
):
    signal = engine.infer_from_embedding(embedding)
    # ...
```

---

## Schema Definitions

### Request Schema

```python
class KaldraSignalRequest(BaseModel):
    text: str = Field(..., description="Input text to analyze")
```

### Response Schema

```python
class KindraDistributionItem(BaseModel):
    state_index: int
    prob: float

class KaldraSignalResponse(BaseModel):
    archetype: str
    delta_state: str
    tw_regime: Literal["STABLE", "ANOMALY"]
    kindra_distribution: List[KindraDistributionItem]
    bias_score: float
    bias_label: str | None
    narrative_risk: float | None
    confidence: float
    explanation: str
    meta_modifiers: Mapping[str, List[float]]
```

---

## Logging

### Structured Logging

**Events Logged**:

1. **Request Received**:
```python
logger.info("KALDRA signal request received", extra={"text_len": len(text)})
```

2. **Signal Generated**:
```python
logger.info(
    "KALDRA signal generated",
    extra={
        "top_idx": top_idx,
        "archetype_id": archetype_id,
        "confidence": conf,
        "tw_trigger": signal.tw_trigger,
        "bias_score": bias_score,
        "narrative_risk": narrative_risk,
    }
)
```

3. **Errors**:
```python
logger.exception("KALDRA Master Engine error")
```

**Configuration**:
- Logger name: `kaldra_api.routers.router_engine`
- Format: Python logging (configurable via logging config)
- Level: INFO (production), DEBUG (development)

---

## CORS Configuration

**Allowed Origins**:
```python
origins = [
    "http://localhost:3000",      # Local development
    "http://localhost:8000",      # API docs
    "https://4iam-frontend.vercel.app"  # Production frontend
]
```

**Settings**:
- `allow_credentials`: True
- `allow_methods`: ["*"]
- `allow_headers`: ["*"]

---

## Error Handling

### Standard Error Response

```json
{
  "detail": "Error message"
}
```

### Error Codes

- **400 Bad Request**: Empty text input
- **500 Internal Server Error**: Master Engine failure
- **404 Not Found**: Invalid endpoint

### Graceful Degradation

**Bias Calculation**:
```python
try:
    bias_result = compute_bias_score_from_text(text)
    bias_score = float(bias_result["bias_score"])
    bias_label = classify_bias(bias_score)
except Exception:
    # Fallback to defaults
    bias_score = 0.0
    bias_label = None
```

---

## Deployment

### Local Development

```bash
cd /Users/niki/Desktop/kaldra_core
source .venv/bin/activate
set -o allexport; source .env.local; set +o allexport
uvicorn kaldra_api.main:app --reload --port 8000
```

### Production

```bash
uvicorn kaldra_api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Environment Variables**:
```bash
# Required for news aggregation
MEDIASTACK_API_KEY=your_key
GNEWS_API_KEY=your_key

# Optional
KALDRA_ENV=production
```

---

## Testing

### API Tests

**Location**: `tests/api/`

**Run Tests**:
```bash
source .venv/bin/activate
python -m pytest tests/api/ -v
```

**Coverage**:
- Bias integration (4 tests)
- Kindra distribution (5 tests)
- Delta144 exposure (5 tests)
- Narrative risk (6 tests)

**Total**: 20/20 passing ✅

---

## Performance Optimization

### Recommendations

1. **Caching**: Implement Redis for repeated queries
2. **Async Processing**: Use background tasks for news aggregation
3. **Connection Pooling**: Reuse HTTP connections for external APIs
4. **Rate Limiting**: Implement per-client rate limits

### Current Bottlenecks

- Embedding generation (placeholder implementation)
- External API latency (news aggregation)
- Semantic similarity computation (Delta144)

---

## Security

### Best Practices

✅ Environment variable-based configuration  
✅ No hardcoded credentials  
✅ CORS whitelist  
✅ Input validation (Pydantic)  
✅ Error message sanitization  

### Future Enhancements

- [ ] API key authentication
- [ ] Rate limiting per client
- [ ] Request signing
- [ ] Audit logging

---

## Monitoring

### Metrics to Track

- Request rate (req/sec)
- Response time (p50, p95, p99)
- Error rate (%)
- External API quota usage
- Master Engine confidence distribution

### Recommended Tools

- **APM**: Sentry, DataDog
- **Logging**: ELK Stack, CloudWatch
- **Metrics**: Prometheus + Grafana

---

## API Documentation

**Interactive Docs**: `http://localhost:8000/docs`

FastAPI auto-generates OpenAPI documentation with:
- Request/response schemas
- Try-it-out functionality
- Model definitions
- Authentication (when implemented)

---

## Changelog

See [CHANGELOG_v2.1.md](../CHANGELOG_v2.1.md) for detailed release notes.

---

**Maintained by**: 4IAM.AI Engineering Team  
**Last Review**: 2025-11-23
