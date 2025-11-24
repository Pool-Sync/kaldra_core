# KALDRA Cloud — Roadmap & Vision

**Version**: 1.0  
**Last Updated**: 2025-11-24  
**Status**: Planning

---

## 🌌 Objective

The **KALDRA Cloud** initiative aims to evolve the current monolithic KALDRA Core into a distributed, multi-module service mesh. This transformation will enable specialized processing for different domains (Alpha, Geo, Product, Safeguard) while maintaining a unified semantic core.

**Core Philosophy**:
- **Specialization**: Dedicated services for distinct analytical domains.
- **Scalability**: Independent scaling of ingestion and inference layers.
- **Unification**: A single "KALDRA Signal" language across all modules.

---

## 🗺️ Roadmap Phases

### v2.2 — Real Embeddings & Hardening (Next Immediate Step)
**Goal**: Move from heuristic/mock embeddings to production-grade vector models.

- **Embeddings**: Integrate `sentence-transformers` or OpenAI Embeddings API for true semantic understanding.
- **Pipeline**: Establish a robust `Ingest -> Embedding -> Vector Store` pipeline.
- **Storage**: Implement persistent storage (S3/Postgres/VectorDB) for Data Lab output.
- **Observability**: Add structured logging and basic metrics (Prometheus).

### v2.3 — Service Modularization
**Goal**: Decouple the monolithic API into specialized namespaces or microservices.

- **KALDRA-Alpha**: Dedicated module for financial markets and earnings analysis.
- **KALDRA-Geo**: Specialized service for geopolitical risk and event tracking.
- **KALDRA-Product**: Module for consumer sentiment and product launch analysis.
- **KALDRA-Safeguard**: Centralized risk, bias, and narrative safety engine.

**Architecture Options**:
1. **Monolith with Modular Routing**: Single backend, strict code separation (e.g., `/alpha/*`, `/geo/*`).
2. **Microservices**: Separate Render services for each module (higher complexity, better isolation).

### v2.4 — Unified "KALDRA Cloud" Dashboard
**Goal**: A single pane of glass for all KALDRA intelligence.

- **Unified UI**: 4iam.ai dashboard aggregating signals from Alpha, Geo, and Product.
- **Visual Engine**: Integration of symbolic visualizations (Kindra Glyphs, Δ144 Grids) powered by real data.
- **Worker Monitor**: UI for tracking status and health of Data Lab ingestion workers.

---

## 🏭 Worker Evolution

The Data Lab will expand with specialized workers feeding specific modules:

| Worker | Target Module | Source Data | Status |
|---|---|---|---|
| **News Ingest** | Geo / General | MediaStack, GNews | ✅ **Active** |
| **Earnings Ingest** | Alpha | FMP, AlphaVantage | 📅 Planned |
| **Geo Event Ingest** | Geo | GDELT, ACLED | 📅 Planned |
| **Product Reviews** | Product | Reddit, YouTube, Amazon | 📅 Planned |
| **Social Pulse** | Safeguard | X (Twitter), BlueSky | 📅 Planned |

---

## 📐 Design Principles

1. **Incremental Evolution**: "Small bites" approach. Deliver value in every minor release (v2.2, v2.3...).
2. **API Compatibility**: Maintain backward compatibility for the `/engine/kaldra/signal` core contract.
3. **Testing First**: No new module without comprehensive integration tests.
4. **Documentation**: Every new service or worker must have a corresponding `WALKTHROUGH.md`.

---

**Maintained by**: 4IAM.AI Engineering Team
