# KALDRA V2.1 — Release Notes

**Release Date:** November 28, 2025  
**Version:** 2.1.0  
**Status:** Production

---

## Overview

KALDRA V2.1 marks the first **production deployment** of the KALDRA symbolic intelligence platform. This release establishes the foundational infrastructure for the KALDRA Alpha dashboard, deployed on Vercel with a FastAPI backend on Render.

Key achievements:
- ✅ Production-ready frontend on Vercel
- ✅ Stable API Gateway on Render
- ✅ CORS configuration for cross-origin requests
- ✅ Data Lab workers for news ingestion
- ✅ Comprehensive documentation suite

---

## Frontend Deployment

### Vercel Deployment
- **Platform:** Vercel (Next.js 14 App Router)
- **Domain:** `https://4iam.ai`
- **Preview URL:** `https://4iam-frontend.vercel.app`
- **Build:** Successful with TypeScript validation

### Environment Configuration
Configured environment variables:
- `NEXT_PUBLIC_KALDRA_API_MODE=remote`
- `NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-core-api.onrender.com`
- `NEXT_PUBLIC_FRONTEND_ENV=production`

### CORS Integration
- Frontend successfully connects to Render backend
- Real-time KALDRA signal processing working
- No CORS errors in production

---

## API Gateway Updates

### CORS Middleware
Added comprehensive CORS configuration in `kaldra_api/main.py`:
```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost:8000",
    "https://4iam.ai",
    "https://www.4iam.ai",
    "https://4iam-frontend.vercel.app",
]
allow_origin_regex="https?://.*"  # Permissive for dev/preview
```

### Health Check Improvements
- `/health` endpoint stable and monitored by Render
- Returns `{"status": "ok"}` on successful startup
- Used for deployment health verification

### Monitoring Integration
- Prometheus metrics stubs in `kaldra_api/monitoring/metrics.py`
- Request counting and latency tracking (foundation)
- Graceful fallback if `prometheus_client` not installed

---

## Data Lab Workers

### News Ingestion Worker
Implemented automated news ingestion pipeline:

**Files Created:**
- `kaldra_data/workers/news_ingest_worker.py` - Core worker logic
- `scripts/run_news_ingest.py` - Execution script

**Features:**
- Fetches news from Mediastack and GNews APIs
- Saves raw data to `data/news/raw/{date}/{query}.jsonl`
- Configurable query and limit parameters
- Error handling for API failures

**Usage:**
```bash
python scripts/run_news_ingest.py --query "AI" --limit 50
```

**Render Cron Job Ready:**
```yaml
# Commented in render.yaml for future activation
jobs:
  - name: kaldra-news-ingest
    schedule: "0 * * * *"  # every hour
    command: ["python", "scripts/run_news_ingest.py", "--query", "AI", "--limit", "50"]
```

---

## Infrastructure

### Render Deployment
- **Service:** `kaldra-api`
- **Region:** Oregon
- **Plan:** Starter (free tier)
- **Docker:** Using `Dockerfile` for containerization
- **Auto-deploy:** Enabled on `main` branch push

### Docker Configuration
- Base image: `python:3.11-slim`
- Uvicorn server with 2 workers
- Health check on `/health` endpoint
- Environment variables managed via Render dashboard

### Environment Variables
Configured on Render:
- `KALDRA_ENV=production`
- News API keys (Mediastack, GNews)
- Social media API keys (X/Twitter, Reddit, YouTube)
- `PYTHONUNBUFFERED=1`
- `WEB_CONCURRENCY=2`

---

## Bug Fixes

### FastAPI Import Error
**Issue:** `NameError: name 'Any' is not defined` in `kaldra_api/monitoring/metrics.py`

**Fix:** Added missing import:
```python
from typing import Optional, Callable, Any
```

**Impact:** Prevented FastAPI from starting, blocking health checks and deployment.

### Type Definition Issues
**Issue:** `KaldraTWRegime` type mismatch in mock data

**Fixes:**
1. Updated `KaldraTWRegime` to include `"CRITICAL"` and `"UNSTABLE"`
2. Fixed `kindra_distribution` structure (Object → Array)
3. Fixed `narrative_risk` type (String → Number)
4. Updated `KaldraSignalDistribution` component to handle array structure

**Impact:** Enabled successful Vercel build and deployment.

---

## Documentation Added

### Frontend Documentation
- `docs/ENV_REFERENCE_FRONTEND.md` - Environment variable reference
- `docs/FRONTEND_STRUCTURE_CHECKLIST.md` - Structure validation checklist
- `docs/DEPLOY_FRONTEND_VERCEL.md` - Vercel deployment guide
- `docs/PRODUCTION_NOTES.md` - Production behavior notes

### Data Lab Documentation
- `docs/DATALAB_WORKERS.md` - Worker implementation guide

### Release Documentation (This Release)
- `docs/KALDRA_V2.1_RELEASE_NOTES.md` - This document
- `docs/PRODUCTION_ARCHITECTURE_OVERVIEW.md` - System architecture
- `docs/KALDRA_CLOUD_ROADMAP.md` - Future development roadmap

---

## Known Issues / Limitations

### Current Limitations
1. **No Database Integration:** Data stored in local files (JSONL format)
2. **Manual Cron Jobs:** Worker scheduling requires manual Render dashboard configuration
3. **No Authentication:** API endpoints are publicly accessible
4. **Limited Monitoring:** Basic health checks only, no comprehensive observability
5. **Single Region:** Deployed only in Oregon region

### Minor Issues
- Mock data uses simplified TW regime values for compatibility
- Some frontend components use placeholder data
- No automated testing in CI/CD pipeline yet

---

## Next Steps

### Immediate (Q4 2025)
- [ ] Activate Render cron job for news ingestion
- [ ] Add Prometheus metrics endpoint
- [ ] Implement basic API rate limiting
- [ ] Add error tracking (Sentry or similar)

### Short-term (Q1 2026)
- [ ] Deploy GEO, Product, and Safeguard dashboards
- [ ] Integrate database for persistent storage
- [ ] Implement user authentication
- [ ] Add automated testing suite

### Medium-term (Q2-Q3 2026)
- [ ] Real-time processing pipeline
- [ ] Advanced analytics features
- [ ] Multi-region deployment
- [ ] Enterprise features (multi-tenancy, SSO)

See `docs/KALDRA_CLOUD_ROADMAP.md` for detailed roadmap.

---

## Contributors

- KALDRA Core Team
- Frontend: Next.js 14 + TypeScript + Tailwind CSS
- Backend: FastAPI + Python 3.11
- Infrastructure: Vercel + Render + Docker

---

## Resources

- **Production Frontend:** https://4iam.ai
- **API Gateway:** https://kaldra-core-api.onrender.com
- **Documentation:** `docs/` directory
- **Repository:** (internal)

---

**End of Release Notes**
