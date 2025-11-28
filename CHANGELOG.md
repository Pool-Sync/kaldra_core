# Changelog

## [2.1.0] – 2025-11-28

### Frontend Deployment
- ✅ Deployed to Vercel (`https://4iam.ai`)
- ✅ Next.js 14 App Router with TypeScript
- ✅ Environment variables configured for production
- ✅ Fixed root directory configuration for Vercel build
- ✅ KALDRA Alpha dashboard operational

### API Gateway & Backend
- ✅ Full CORS configuration for production domains
  - `https://4iam.ai`
  - `https://www.4iam.ai`
  - `https://4iam-frontend.vercel.app`
  - Permissive regex for dev/preview environments
- ✅ FastAPI import fix (`Any` type in monitoring/metrics)
- ✅ Health check endpoint stable (`/health`)
- ✅ Deployed to Render with Docker
- ✅ Auto-deploy on main branch push

### Data Lab Workers
- ✅ News ingestion worker implementation
  - `kaldra_data/workers/news_ingest_worker.py`
  - `scripts/run_news_ingest.py`
- ✅ Mediastack and GNews API integration
- ✅ JSONL data storage pipeline
- ✅ Render cron job configuration (commented, ready to activate)

### Type System & Build Fixes
- ✅ Updated `KaldraTWRegime` type definition
- ✅ Fixed `kindra_distribution` structure (Object → Array)
- ✅ Fixed `narrative_risk` type (String → Number)
- ✅ Updated `KaldraSignalDistribution` component for array handling
- ✅ TW-Regime mock values updated for Vercel build compatibility

### Documentation
- ✅ `docs/ENV_REFERENCE_FRONTEND.md` - Frontend environment variables
- ✅ `docs/FRONTEND_STRUCTURE_CHECKLIST.md` - Structure validation
- ✅ `docs/DEPLOY_FRONTEND_VERCEL.md` - Deployment guide
- ✅ `docs/PRODUCTION_NOTES.md` - Production behavior notes
- ✅ `docs/DATALAB_WORKERS.md` - Worker implementation guide
- ✅ `docs/KALDRA_V2.1_RELEASE_NOTES.md` - Comprehensive release notes
- ✅ `docs/PRODUCTION_ARCHITECTURE_OVERVIEW.md` - System architecture
- ✅ `docs/KALDRA_CLOUD_ROADMAP.md` - Future development roadmap

### Infrastructure
- ✅ Render instance configuration (Starter plan)
- ✅ Docker containerization
- ✅ Uvicorn with 2 workers
- ✅ Environment variables managed via Render dashboard
- ✅ Automatic health monitoring

### Bug Fixes
- 🐛 Fixed FastAPI startup crash (missing `Any` import)
- 🐛 Fixed CORS errors between Vercel and Render
- 🐛 Fixed type mismatches in mock data
- 🐛 Fixed Vercel build failures due to type definitions
- 🐛 Several deployment recovery steps documented

### Known Issues
- No database integration (file-based storage)
- No user authentication
- Manual worker scheduling (cron jobs not activated)
- Single region deployment (Oregon)
- Limited monitoring (basic health checks only)



## v2.1
- API Enrichment completo
- Kindra Distribution
- Delta144 real
- Narrative Risk
- Logging estruturado
- News API integration
- Documentação produção criada

## v2.0
- Master Engine V2
- Delta144 semantic
- TW + Painlevé stub
- Bias Engine melhorado
- Testes core (37 total)
