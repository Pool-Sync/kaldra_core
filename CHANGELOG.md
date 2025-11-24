# Changelog

All notable changes to the **KALDRA Core** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v2.1.0] - 2025-11-24

### 🚀 Production Release
The system has transitioned to a production-ready architecture deployed on Render.com (Backend) and Vercel (Frontend).

### Added
- **Backend Deployment**: Dockerized API Gateway deployed on Render (`kaldra-core-api`).
- **Frontend Integration**: 4iam.ai frontend fully integrated with the backend via REST API.
- **Data Lab**: New module for automated data ingestion.
  - **News Worker**: `news_ingest_worker.py` for MediaStack/GNews aggregation.
  - **CLI**: `scripts/run_news_ingest.py` for local and cron execution.
- **Documentation**:
  - `docs/KALDRA_V2.1_RELEASE_NOTES.md`: Detailed release notes.
  - `docs/PRODUCTION_ARCHITECTURE_OVERVIEW.md`: System architecture guide.
  - `docs/KALDRA_CLOUD_ROADMAP.md`: Future vision and next steps.
  - `docs/DATALAB_WORKERS.md`: Guide for Data Lab workers.

### Changed
- **Infrastructure**: Added `Dockerfile`, `render.yaml`, and production `requirements.txt`.
- **Testing**: Reached 57 passing tests (37 Core, 20 API).

---

## [v2.0.0] - 2025-11-22

### 🌟 Master Engine V2
First stable release of the rewritten KALDRA Master Engine.

### Added
- **Master Engine**: `KaldraMasterEngineV2` with semantic inference logic.
- **Δ144 Engine**: Implementation of the 144-state archetype system.
- **TW369 Oracle**: Tracy-Widom distribution filters and Painlevé transcedents.
- **Bias Engine**: Keyword and heuristic-based bias detection.
- **API Gateway**: Initial FastAPI implementation with dependency injection.

### Removed
- Legacy `kaldra_engine.py` (v1 logic).

---

## [v1.x] - Legacy
- Initial prototypes and mock implementations.
