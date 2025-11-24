# KALDRA Core v2.1 — Release Notes

**Version**: 2.1.0  
**Release Date**: 2025-11-24  
**Status**: Production Ready

---

## 🧠 Overview

KALDRA Core v2.1 marks a significant milestone in the evolution of the 4IAM.AI ecosystem. This release transitions the project from a local development environment to a fully deployed, production-ready cloud architecture.

**Key Highlights**:
- **Master Engine V2**: Fully integrated semantic inference engine with Δ144 and TW369 components.
- **Production API Gateway**: High-performance FastAPI backend deployed on Render.com.
- **Frontend Integration**: Next.js frontend (4iam.ai) fully integrated with the backend via secure API contracts.
- **Data Lab**: New module for automated data ingestion, starting with global news aggregation.
- **Containerization**: Full Docker support for consistent deployment across environments.

---

## ✨ New Features

### Phase 4: Master Engine Consolidation
- **Semantic Inference**: Replaced mock logic with real cosine similarity search against 144 archetype states.
- **Bias Detection**: Integrated keyword-based bias scoring (absolutist/emotional terms).
- **Narrative Risk**: Real-time calculation of narrative risk based on bias, confidence, and TW triggers.

### Phase 5: API Gateway
- **Endpoints**: Stabilized REST API contracts for `/engine/kaldra/signal` and `/kaldra/news`.
- **Dependency Injection**: Singleton pattern for Master Engine to ensure performance and state consistency.
- **CORS & Security**: Configured for secure cross-origin requests from the Vercel frontend.

### Phase 6: Frontend Integration
- **Client Library**: Robust TypeScript client (`kaldra_client.ts`) with retry logic, timeouts, and automatic fallback to mock data.
- **Type Safety**: Shared TypeScript interfaces ensuring frontend-backend contract alignment.
- **Environment Config**: Seamless switching between "mock" and "real" modes via environment variables.

### Data Lab (Phase 9)
- **News Ingestion**: Automated workers to fetch and normalize news from MediaStack and GNews.
- **CLI Tools**: Scripts for local execution and cron job management.
- **Extensible Architecture**: Foundation laid for future earnings, geopolitics, and product review workers.

---

## 🔌 External APIs

This release integrates two primary external data sources for the Data Lab:

1. **MediaStack**: Global news aggregation.
2. **GNews**: Real-time news search.

These APIs are currently used by the **News Ingest Worker** to populate the raw data layer, which will feed into KALDRA-Geo and KALDRA-Alpha modules in future updates.

---

## 🧪 Testing Summary

The release has been rigorously tested with a suite of **57 passing tests**:

- **37 Core Tests**: Covering Master Engine logic, Δ144 inference, TW369 oracle, and bias detection.
- **20 API Tests**: Validating endpoint responses, error handling, schema validation, and integration flows.

**Coverage**:
- ✅ Master Engine V2 Inference
- ✅ Δ144 State Transitions
- ✅ Bias & Risk Calculation
- ✅ API Request/Response Cycles
- ✅ News Ingestion Logic (Mocked)

---

## 🚀 Deployment Summary

### Backend (Render.com)
- **Service**: `kaldra-core-api`
- **Runtime**: Docker (Python 3.11-slim)
- **Infrastructure**: Defined via `render.yaml` (Infrastructure as Code).
- **Configuration**: Environment variables for secure API key management.

### Frontend (Vercel)
- **Project**: `4iam-frontend`
- **Framework**: Next.js 14 (App Router)
- **Integration**: Connected via `NEXT_PUBLIC_KALDRA_API_URL`.

---

## ⚠️ Breaking Changes

> **None**. There are no breaking changes for external consumers of the API between v2.0 and v2.1. The API contract remains backward compatible.

---

## 🔮 Next Steps (High-Level)

The foundation is set for **KALDRA Cloud** (v2.2+):

1. **Real Embeddings**: Transition from heuristic/placeholder embeddings to high-dimensional vector models (e.g., OpenAI, HuggingFace).
2. **Expanded Ingestion**: Integrations for X (Twitter), YouTube, and Reddit.
3. **Observability**: Implementation of structured logging, metrics (Prometheus/Grafana), and tracing.
4. **Public Dashboard**: A unified "KALDRA Signals" dashboard for real-time monitoring of global narratives.

---

**Maintained by**: 4IAM.AI Engineering Team
