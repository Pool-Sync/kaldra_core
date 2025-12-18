# PRODUCTION_ARCHITECTURE_OVERVIEW.md

## 1. System Overview

KALDRA is a **symbolic intelligence platform** that processes text inputs through multiple analytical engines to generate insights. The production architecture consists of three main layers:

1. **Frontend Layer** (Vercel) - User interface and client-side logic
2. **API Gateway Layer** (Render) - Request routing and orchestration
3. **Core Engine Layer** (Python) - KALDRA symbolic processing

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  FRONTEND (Vercel)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Next.js 14 App Router                               │   │
│  │  - TypeScript + Tailwind CSS                         │   │
│  │  - KALDRA Alpha Dashboard                            │   │
│  │  - Real-time signal visualization                    │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS
                         │ (CORS enabled)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              API GATEWAY (Render)                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FastAPI + Uvicorn                                   │   │
│  │  - CORS Middleware                                   │   │
│  │  - Health Checks                                     │   │
│  │  - Request Routing                                   │   │
│  │  - Monitoring Stubs                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 KALDRA CORE ENGINE                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Master Engine V2                                    │   │
│  │  ├─ TW-Painlevé Oracle                               │   │
│  │  ├─ Delta144 Archetype Engine                        │   │
│  │  ├─ Kindra Cultural Modulation                       │   │
│  │  ├─ Bias Detection Engine                            │   │
│  │  └─ Narrative Risk Assessment                        │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Data Lab                                            │   │
│  │  ├─ News Ingestion Workers                           │   │
│  │  ├─ Preprocessing Pipeline                           │   │
│  │  └─ Transformation Layer                             │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Component Architecture

### 2.1 Frontend (Vercel)

**Technology Stack:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React 18

**Key Features:**
- Server-side rendering (SSR)
- Static site generation (SSG) for documentation
- Client-side API calls to Render backend
- Environment-based configuration (mock vs. remote)

**Deployment:**
- Platform: Vercel
- Domain: `https://4iam.ai`
- Auto-deploy: On `main` branch push
- Build command: `next build`
- Output: `.next/` directory

**Environment Variables:**
```bash
NEXT_PUBLIC_KALDRA_API_MODE=remote
NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-core-api.onrender.com
NEXT_PUBLIC_FRONTEND_ENV=production
```

---

### 2.2 API Gateway (Render)

**Technology Stack:**
- FastAPI (Python 3.11)
- Uvicorn ASGI server
- Docker containerization
- CORS middleware

**Key Responsibilities:**
1. **Request Routing:** Routes requests to appropriate KALDRA engines
2. **CORS Handling:** Enables cross-origin requests from Vercel
3. **Health Monitoring:** Provides `/health` endpoint for Render
4. **Error Handling:** Graceful error responses
5. **Metrics Collection:** Prometheus integration stubs

**Endpoints:**
- `GET /health` - Health check
- `POST /engine/kaldra/signal` - KALDRA signal processing
- `GET /status/health` - Detailed status
- `GET /alpha/*` - Alpha-specific endpoints
- `GET /geo/*` - GEO endpoints (future)
- `GET /product/*` - Product endpoints (future)
- `GET /safeguard/*` - Safeguard endpoints (future)

**Deployment:**
- Platform: Render
- Region: Oregon
- Plan: Starter (free tier)
- Container: Docker
- Workers: 2 (Uvicorn)

**Environment Variables:**
```bash
KALDRA_ENV=production
MEDIASTACK_API_KEY=<secret>
GNEWS_API_KEY=<secret>
X_BEARER_TOKEN=<secret>
REDDIT_CLIENT_ID=<secret>
REDDIT_CLIENT_SECRET=<secret>
YOUTUBE_API_KEY=<secret>
PYTHONUNBUFFERED=1
WEB_CONCURRENCY=2
```

---

### 2.3 KALDRA Core Engine

**Components:**

1. **Master Engine V2**
   - Orchestrates all sub-engines
   - Combines outputs into unified signal
   - Located: `src/kaldra_core/engine/master_engine_v2.py`

2. **TW-Painlevé Oracle**
   - Analyzes text stability using Tracy-Widom distribution
   - Returns: `STABLE`, `CRITICAL`, or `UNSTABLE`
   - Located: `src/kaldra_core/engine/tw369/`

3. **Delta144 Archetype Engine**
   - Maps text to 12 archetypes × 12 states = 144 states
   - Returns: Archetype ID and state ID
   - Located: `src/kaldra_core/engine/delta144/`

4. **Kindra Cultural Modulation**
   - Applies cultural context to analysis
   - Returns: Top-5 cultural state probabilities
   - Located: `src/kaldra_core/engine/kindra/`

5. **Bias Detection Engine**
   - Detects narrative bias in text
   - Returns: Bias score (0.0 - 1.0) and label
   - Located: `src/kaldra_core/engine/bias/`

6. **Narrative Risk Assessment**
   - Evaluates narrative manipulation risk
   - Returns: Risk score (0.0 - 1.0)
   - Located: `src/kaldra_core/engine/narrative/`

---

### 2.4 Data Lab (Workers)

**Purpose:** Automated data ingestion and preprocessing

**Workers:**
- `news_ingest_worker.py` - Fetches news from Mediastack and GNews
- (Future) `earnings_ingest_worker.py` - Financial data
- (Future) `geo_ingest_worker.py` - Geopolitical events
- (Future) `product_reviews_worker.py` - Product reviews

**Data Flow:**
```
External APIs → Workers → Raw Data (JSONL) → Preprocessing → Transformation → KALDRA Engine
```

**Storage:**
- Raw data: `data/news/raw/{date}/{query}.jsonl`
- Processed data: `data/news/processed/` (future)
- Embeddings: `data/embeddings/` (future)

---

## 3. Request Lifecycle

### 3.1 User Signal Request

```
1. User enters text in frontend (https://4iam.ai/alpha)
   ↓
2. Frontend sends POST to API Gateway
   POST https://kaldra-core-api.onrender.com/engine/kaldra/signal
   Body: {"text": "user input"}
   ↓
3. API Gateway validates request
   ↓
4. API Gateway calls Master Engine V2
   ↓
5. Master Engine orchestrates sub-engines:
   - TW-Painlevé Oracle
   - Delta144 Archetype Engine
   - Kindra Cultural Modulation
   - Bias Detection Engine
   - Narrative Risk Assessment
   ↓
6. Master Engine combines results
   ↓
7. API Gateway returns JSON response:
   {
     "archetype": "A07_RULER",
     "delta_state": "A07_05",
     "tw_regime": "STABLE",
     "kindra_distribution": [...],
     "bias_score": 0.3,
     "narrative_risk": 0.2,
     "confidence": 0.85,
     "explanation": "Master Engine V2: OK"
   }
   ↓
8. Frontend displays results to user
```

**Typical Response Time:** 200-500ms

---

## 4. Cloud Deployment Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      INTERNET                               │
└────────────┬────────────────────────────────┬───────────────┘
             │                                │
             │ HTTPS                          │ HTTPS
             │                                │
             ▼                                ▼
┌────────────────────────┐      ┌────────────────────────────┐
│   VERCEL (Frontend)    │      │   RENDER (Backend)         │
│  ┌──────────────────┐  │      │  ┌──────────────────────┐  │
│  │  Next.js App     │  │      │  │  Docker Container    │  │
│  │  - SSR/SSG       │  │      │  │  ┌────────────────┐  │  │
│  │  - Edge Network  │  │◄─────┼──┼──┤  FastAPI       │  │  │
│  │  - Auto-scale    │  │ CORS │  │  │  + Uvicorn     │  │  │
│  └──────────────────┘  │      │  │  └────────────────┘  │  │
│                        │      │  │  ┌────────────────┐  │  │
│  Domain:               │      │  │  │  KALDRA Core   │  │  │
│  - 4iam.ai             │      │  │  │  Engines       │  │  │
│  - *.vercel.app        │      │  │  └────────────────┘  │  │
└────────────────────────┘      │  └──────────────────────┘  │
                                │                            │
                                │  Domain:                   │
                                │  - kaldra-core-api         │
                                │    .onrender.com           │
                                │                            │
                                │  Health Check:             │
                                │  - /health → 200 OK        │
                                └────────────────────────────┘
```

**Key Infrastructure:**
- **Vercel:** Global CDN, automatic HTTPS, edge network
- **Render:** Docker-based deployment, health monitoring, auto-scaling

---

## 5. Security Model

### 5.1 CORS Configuration

**Allowed Origins:**
```python
origins = [
    "http://localhost:3000",      # Local development
    "http://localhost:8000",      # Local API testing
    "https://4iam.ai",            # Production domain
    "https://www.4iam.ai",        # Production www
    "https://4iam-frontend.vercel.app",  # Vercel preview
]
allow_origin_regex="https?://.*"  # Permissive for dev/preview
```

### 5.2 Environment Variables

**Frontend (Public):**
- All `NEXT_PUBLIC_*` variables are embedded in client bundle
- No secrets allowed

**Backend (Private):**
- API keys stored in Render dashboard
- Not committed to repository
- Accessed via `os.getenv()`

### 5.3 Current Limitations

⚠️ **No Authentication:** API endpoints are publicly accessible  
⚠️ **No Rate Limiting:** Potential for abuse  
⚠️ **No API Keys:** No user-level access control  
⚠️ **No Encryption at Rest:** Data stored in plain text files

**Future Improvements:**
- Implement JWT-based authentication
- Add API key system for external access
- Implement rate limiting (per IP, per user)
- Encrypt sensitive data at rest

---

## 6. Environments & Variables

### 6.1 Environment Types

| Environment | Frontend URL | Backend URL | Purpose |
|-------------|-------------|-------------|---------|
| **Local** | `localhost:3000` | `localhost:8000` | Development |
| **Preview** | `*.vercel.app` | `kaldra-core-api.onrender.com` | PR testing |
| **Production** | `4iam.ai` | `kaldra-core-api.onrender.com` | Live users |

### 6.2 Configuration Files

**Frontend:**
- `.env.local` (local development, gitignored)
- `.env.example` (template)
- Vercel dashboard (production)

**Backend:**
- `.env.local` (local development, gitignored)
- `.env.example` (template)
- Render dashboard (production)

**Documentation:**
- `docs/ENV_REFERENCE_FRONTEND.md` - Frontend env vars
- `docs/PRODUCTION_NOTES.md` - Production behavior

---

## 7. Monitoring

### 7.1 Current Monitoring

**Health Checks:**
- Endpoint: `/health`
- Returns: `{"status": "ok"}`
- Monitored by: Render platform
- Frequency: Every 30 seconds

**Deployment Logs:**
- Vercel: Build logs, runtime logs
- Render: Container logs, deployment logs

### 7.2 Metrics (Stubs)

**Prometheus Integration:**
- File: `kaldra_api/monitoring/metrics.py`
- Metrics:
  - `kaldra_api_requests_total` (Counter)
  - `kaldra_api_request_duration_seconds` (Histogram)
- Status: Stubs implemented, not yet exposed

### 7.3 Future Monitoring

**Planned:**
- Prometheus metrics endpoint (`/metrics`)
- Grafana dashboards
- Error tracking (Sentry)
- Performance monitoring (New Relic / Datadog)
- Log aggregation (Logtail / Papertrail)
- Uptime monitoring (UptimeRobot / Pingdom)

---

## 8. Scalability Considerations

### 8.1 Current Bottlenecks

1. **Single Region:** Deployed only in Oregon
2. **No Caching:** Every request hits the engine
3. **File-based Storage:** No database for persistence
4. **Limited Workers:** Only 2 Uvicorn workers
5. **No Load Balancing:** Single Render instance

### 8.2 Scaling Strategy

**Horizontal Scaling:**
- Increase Render instances (requires paid plan)
- Add load balancer
- Deploy to multiple regions

**Vertical Scaling:**
- Upgrade Render plan (more CPU/RAM)
- Increase Uvicorn workers

**Caching:**
- Add Redis for frequently requested signals
- Cache archetype/state mappings
- Cache news data

**Database:**
- PostgreSQL for persistent storage
- Store signals, users, analytics
- Enable complex queries

### 8.3 Performance Targets

| Metric | Current | Target (Q1 2026) |
|--------|---------|------------------|
| **Response Time** | 200-500ms | <200ms |
| **Concurrent Users** | ~10 | 1000+ |
| **Requests/sec** | ~5 | 100+ |
| **Uptime** | 95% | 99.9% |

---

## 9. Disaster Recovery

### 9.1 Backup Strategy

**Current:**
- Git repository (code)
- Vercel automatic backups
- Render automatic backups

**Future:**
- Database backups (daily)
- Data Lab raw data backups (S3)
- Configuration backups

### 9.2 Rollback Procedure

**Frontend (Vercel):**
1. Go to Vercel dashboard
2. Select previous deployment
3. Click "Promote to Production"

**Backend (Render):**
1. Go to Render dashboard
2. Select previous deployment
3. Click "Redeploy"

**Code Rollback:**
```bash
git revert <commit-hash>
git push origin main
```

---

## 10. Deployment Checklist

### Pre-Deployment
- [ ] All tests passing locally
- [ ] Environment variables configured
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

### Deployment
- [ ] Push to `main` branch
- [ ] Verify Vercel build succeeds
- [ ] Verify Render deployment succeeds
- [ ] Check health endpoint (`/health`)

### Post-Deployment
- [ ] Smoke test: Send test signal
- [ ] Verify CORS working
- [ ] Check logs for errors
- [ ] Monitor for 15 minutes

---

## 11. Troubleshooting

### Common Issues

**CORS Errors:**
- Verify origin in `kaldra_api/main.py`
- Check Render logs for CORS middleware errors
- Ensure `allow_origin_regex` is set

**Health Check Failures:**
- Check Render logs for startup errors
- Verify all imports are correct
- Check for missing environment variables

**Build Failures:**
- Frontend: Check TypeScript errors
- Backend: Check Python import errors
- Verify all dependencies in `requirements.txt`

---

## 12. References

- **Frontend Deployment:** `docs/DEPLOY_FRONTEND_VERCEL.md`
- **Environment Variables:** `docs/ENV_REFERENCE_FRONTEND.md`
- **Production Notes:** `docs/PRODUCTION_NOTES.md`
- **Workers:** `docs/DATALAB_WORKERS.md`
- **Release Notes:** `docs/KALDRA_V2.1_RELEASE_NOTES.md`
- **Roadmap:** `docs/KALDRA_CLOUD_ROADMAP.md`

---

**End of Architecture Overview**
