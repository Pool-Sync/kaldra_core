# **KALDRA Future Steps — System Roadmap (v2.4 → v3.0)**

**Status:** Living Document  
**Scope:** Core Engine, Data Lab, Embeddings, TW369, Δ144, Kindra, Logging  
**Updated:** 2025-11-27  
**Version:** 1.0

---

## **Overview**

This document consolidates all **official next steps** for the KALDRA ecosystem, including:

- **Core Engine** orchestration and multi-domain pipelines
- **Embedding Layer** expansion and optimization
- **Data Lab** integration and streaming capabilities
- **TW369 Engine** runtime configuration and observability
- **Δ144 Engine** drift-aware enhancements
- **Kindra Scoring** LLM fine-tuning and hybrid optimization
- **Logging & Audit Trail** persistent backends and distributed tracing
- **Testing & Production** deployment strategies

This roadmap acts as the **master reference** for all future development sprints and architectural decisions.

---

## 1. **Embedding Layer — Roadmap**

### **1.1 Dimension Enforcement (Strict Mode)**

**Objective:** Ensure embedding dimension consistency across all providers and models.

**Tasks:**
- Validate `config.dim` against actual embedding output dimensions
- Raise explicit errors when dimensions mismatch
- Implement intelligent mode with configurable strategies:
  - **Truncate:** Cut extra dimensions
  - **Pad:** Zero-pad missing dimensions
  - **Error:** Strict validation (default)
- Add configuration flag: `embedding.dimension_mode: strict|truncate|pad`

**Impact:** Prevents silent failures in downstream vector operations and ensures mathematical consistency.

---

### **1.2 Async Embedding Pipeline**

**Objective:** Enable high-throughput, non-blocking embedding generation.

**Tasks:**
- Implement `async def encode_async(texts: List[str]) -> List[np.ndarray]`
- Create batch streaming interface for large document sets
- GPU multi-worker queue with configurable concurrency
- Support for async context managers and proper resource cleanup
- Benchmark against synchronous implementation

**Impact:** 10-100x throughput improvement for bulk embedding operations.

---

### **1.3 Embedding Metrics**

**Objective:** Comprehensive observability for embedding operations.

**Tasks:**
- Track batch latency (p50, p95, p99)
- Cache hit/miss ratios
- Provider-specific metrics:
  - SentenceTransformer local inference time
  - OpenAI API latency and rate limits
  - Cohere API performance
  - Custom model inference stats
- Embedding quality metrics:
  - Cosine similarity distributions
  - Cluster coherence scores
- Export metrics to Prometheus/StatsD

**Impact:** Data-driven optimization and provider selection.

---

### **1.4 Provider Expansion**

**Objective:** Support diverse embedding models and providers.

**Tasks:**
- **Google Gemini Embed:** Integration via Vertex AI
- **HuggingFace Models:** Direct model loading and inference
- **Fine-tuned KALDRA Models:**
  - `KALDRA-English-v1`: Optimized for financial/geopolitical narratives
  - `KALDRA-Portuguese-v1`: Brazilian Portuguese specialization
- **Multi-modal Embeddings:**
  - CLIP for image+text
  - Whisper embeddings for audio
  - Video frame embeddings
- Provider fallback chains with automatic retry logic

**Impact:** Domain-specific accuracy improvements and reduced vendor lock-in.

---

## 2. **Data Lab — Roadmap**

### **2.1 Full Integration with EmbeddingRouter**

**Objective:** Unify all Data Lab pipelines with the new embedding architecture.

**Tasks:**
- Update existing pipelines:
  - `AlphaPipeline` → financial narratives
  - `GEOPipeline` → geopolitical events
  - `ProductPipeline` → UX/product feedback
  - `SafeguardPipeline` → safety/toxicity detection
- Create unified abstraction: `KALDRAUnifiedPipeline`
  - Single entry point for all domain-specific processing
  - Configurable embedding strategy per domain
  - Automatic routing based on document type
- Deprecate legacy embedding code paths

**Impact:** Consistent embedding quality across all KALDRA domains.

---

### **2.2 Data Lab Streaming**

**Objective:** Enable real-time, incremental data processing.

**Tasks:**
- Implement streaming ingestion interface:
  - Kafka/Pulsar integration
  - WebSocket streaming
  - File watch mode for local development
- Chunk-level embedding generation
- Automatic TW369 temporal window creation from streaming data
- Incremental Δ144 archetype updates
- Backpressure handling and flow control

**Impact:** Real-time narrative tracking and drift detection.

---

### **2.3 Multi-Modal Inputs**

**Objective:** Extend KALDRA beyond text-only analysis.

**Tasks:**
- **PDF Processing:**
  - Text extraction with layout preservation
  - Table and figure detection
  - Multi-page document chunking
- **Video Analysis:**
  - Frame extraction and embedding
  - Audio transcription + embedding
  - Scene change detection
- **Audio Processing:**
  - Speech-to-text with Whisper
  - Audio embedding for sentiment/tone
- **Image Analysis:**
  - CLIP embeddings
  - OCR for text-in-image
- Unified multi-modal embedding fusion strategy

**Impact:** Comprehensive narrative analysis across all media types.

---

## 3. **TW369 Engine — Roadmap**

### **3.1 Runtime Config Application**

**Objective:** Make TW369 configuration fully dynamic and profile-based.

**Tasks:**
- Implement runtime application of loaded config schemas:
  - Enable/disable individual planes (Epistemic, Ontological, Axiological)
  - Dynamic damping coefficient adjustment
  - Lambda parameter tuning for severity scaling
- Create configuration profiles:
  - **Default:** Balanced sensitivity
  - **Conservative:** High damping, low drift propagation
  - **Exploratory:** Low damping, high sensitivity to narrative shifts
- Hot-reload configuration without engine restart
- Configuration validation and schema enforcement

**Impact:** Adaptive drift detection for different use cases and risk profiles.

---

### **3.2 Painlevé II Enhancements**

**Objective:** Improve mathematical rigor and numerical stability.

**Tasks:**
- Numerical validation of Painlevé II solutions
- Implement approximate solvers for edge cases:
  - Asymptotic expansions
  - Series solutions
  - Rational approximations
- Automatic parameter fitting:
  - Optimize `a`, `b`, `c` coefficients based on historical drift patterns
  - Machine learning-based parameter tuning
- Stability analysis and error bounds
- Fallback to simpler models when Painlevé II is ill-conditioned

**Impact:** More robust drift quantification in extreme scenarios.

---

### **3.3 TW369 Observability**

**Objective:** Deep visibility into drift evolution and plane interactions.

**Tasks:**
- **Per-Plane Logging:**
  - Epistemic tension evolution
  - Ontological drift magnitude
  - Axiological severity scores
- **Drift Visualizations:**
  - Tension histograms over time
  - Drift evolution timeline graphs
  - Plane interaction heatmaps
- **OpenTelemetry Integration:**
  - Distributed tracing for drift calculations
  - Span annotations for each plane
  - Context propagation across engine boundaries
- **Alerting:**
  - Threshold-based drift alerts
  - Anomaly detection in drift patterns

**Impact:** Proactive drift management and root cause analysis.

---

## 4. **Kindra Scoring — Roadmap**

### **4.1 LLM Scoring v2 (Fine-Tuning)**

**Objective:** Transition from zero-shot to fine-tuned LLM scoring.

**Tasks:**
- **Dataset Creation:**
  - Curate 10k+ labeled examples across domains
  - Multi-language support (English, Portuguese, Spanish)
  - Domain-specific datasets (finance, geopolitics, safety)
- **Fine-Tuning Pipeline:**
  - Few-shot prompt optimization
  - LoRA/QLoRA for efficient fine-tuning
  - Model distillation for faster inference
- **Enhanced Output:**
  - Add `confidence_score` field (0.0-1.0)
  - Explanation generation for scores
  - Multi-dimensional scoring (not just single value)
- **Evaluation:**
  - Human evaluation benchmark
  - Inter-annotator agreement metrics

**Impact:** 30-50% improvement in scoring accuracy and consistency.

---

### **4.2 Hybrid Scoring v2**

**Objective:** Dynamic weighting between rule-based and LLM scoring.

**Tasks:**
- **Dynamic Alpha (α) Calculation:**
  - Narrative dominance: High narrative content → higher LLM weight
  - Document type: Structured data → higher rule-based weight
  - Context dominance: Strong country/sector signals → adjust accordingly
- **Context-Aware Weighting:**
  - Country-specific scoring profiles
  - Sector-specific rule emphasis
  - Domain-specific LLM reliance
- **Adaptive Learning:**
  - Track scoring accuracy over time
  - Automatically adjust α based on performance
  - A/B testing framework for scoring strategies

**Impact:** Optimal balance between interpretability and accuracy.

---

### **4.3 Batch LLM Scoring**

**Objective:** Efficient scoring of multiple documents simultaneously.

**Tasks:**
- Implement batch API calls to LLM providers
- Parallel scoring with configurable concurrency
- Intelligent batching strategies:
  - Group similar documents for better prompt reuse
  - Dynamic batch sizing based on token limits
- Caching and deduplication
- Cost optimization through batch pricing

**Impact:** 5-10x cost reduction and throughput improvement.

---

## 5. **Δ144 Engine — Roadmap**

### **5.1 Δ144 Drift-Aware Reweighting**

**Objective:** Adjust archetype detection based on TW369 drift intensity.

**Tasks:**
- Implement dynamic reweighting of 12×12 archetype cells
- High drift → increase sensitivity to narrative shifts
- Low drift → stabilize archetype assignments
- Per-plane drift influence:
  - Epistemic drift → affect knowledge archetypes
  - Ontological drift → affect structural archetypes
  - Axiological drift → affect value archetypes
- Configurable drift-to-weight mapping functions

**Impact:** More responsive archetype detection during narrative turbulence.

---

### **5.2 Δ144 Explanations**

**Objective:** Human-readable explanations for archetype assignments.

**Tasks:**
- Generate natural language explanations:
  - "This narrative is classified as **Visionary** because it emphasizes future possibilities and transformative change."
- Highlight key features that influenced the decision
- Confidence intervals for archetype assignments
- Alternative archetype suggestions with probabilities
- Integration with LLM for richer explanations

**Impact:** Improved interpretability and user trust.

---

### **5.3 Archetype Embedding Projection**

**Objective:** Visualize archetype space and narrative positioning.

**Tasks:**
- **Dimensionality Reduction:**
  - PCA for linear projection
  - UMAP for non-linear manifold learning
  - t-SNE for cluster visualization
- **Interactive Visualizations:**
  - 2D/3D scatter plots of narratives in archetype space
  - Cluster boundaries and archetype regions
  - Temporal evolution animations
- **Archetype Drift Tracking:**
  - Visualize how narratives move through archetype space over time
  - Identify archetype transition patterns

**Impact:** Intuitive understanding of narrative landscape.

---

## 6. **Master Engine — Roadmap**

### **6.1 Unified Orchestration Layer**

**Objective:** Transform Master Engine into a comprehensive pipeline orchestrator.

**Tasks:**
- **Standardized Pipeline:**
  ```
  ingest → embed → kindra → Δ144 → TW369 → epistemic → log
  ```
- **Orchestration Features:**
  - Dependency management between stages
  - Conditional execution based on intermediate results
  - Error handling and retry logic
  - Partial pipeline execution (skip stages)
- **Configuration-Driven:**
  - YAML/JSON pipeline definitions
  - Hot-reload pipeline configurations
  - A/B testing different pipeline variants

**Impact:** Simplified integration and consistent processing across domains.

---

### **6.2 Multi-Domain Pipelines**

**Objective:** Specialized pipelines for each KALDRA domain.

**Tasks:**
- **Alpha Pipeline (Finance):**
  - Financial entity extraction
  - Market sentiment analysis
  - Regulatory compliance checks
- **GEO Pipeline (Geopolitical):**
  - Event extraction and classification
  - Actor relationship mapping
  - Conflict intensity scoring
- **Product Pipeline (UX):**
  - Feature request extraction
  - User sentiment analysis
  - Priority scoring
- **Safeguard Pipeline (Safety):**
  - Toxicity detection
  - Bias identification
  - Content moderation
- **Shared Components:**
  - Common embedding layer
  - Unified logging
  - Cross-domain archetype transfer learning

**Impact:** Domain-optimized accuracy with shared infrastructure.

---

### **6.3 Real-Time Engine**

**Objective:** Enable live narrative tracking and drift monitoring.

**Tasks:**
- **WebSocket Streaming:**
  - Real-time narrative ingestion
  - Live drift evolution updates
  - Streaming archetype assignments
- **Event-Driven Architecture:**
  - Pub/sub for narrative events
  - Event sourcing for audit trail
  - CQRS pattern for read/write separation
- **Live Dashboards:**
  - Real-time drift graphs
  - Live archetype distribution
  - Alert notifications

**Impact:** Immediate narrative intelligence for time-sensitive decisions.

---

## 7. **Logging & Audit Trail — Roadmap**

### **7.1 Persistent Backends**

**Objective:** Durable storage for all KALDRA operations and results.

**Tasks:**
- **PostgreSQL Integration:**
  - Structured logging tables
  - Efficient indexing for queries
  - Time-series partitioning
- **MongoDB Integration:**
  - Document-based logging
  - Flexible schema evolution
  - Aggregation pipelines for analytics
- **DynamoDB Integration:**
  - Serverless scalability
  - Global tables for multi-region
  - TTL for automatic cleanup
- **S3 JSONL Append-Mode:**
  - Cost-effective long-term storage
  - Athena/Presto queryable
  - Immutable audit trail
- **Backend Selection:**
  - Configuration-driven backend choice
  - Multi-backend support (write to multiple)

**Impact:** Compliance-ready audit trail and historical analysis.

---

### **7.2 Metrics Exporter**

**Objective:** Integration with standard monitoring ecosystems.

**Tasks:**
- **Prometheus Exporter:**
  - Custom metrics for all KALDRA components
  - Latency histograms (embedding, scoring, drift)
  - Counter metrics (documents processed, errors)
  - Gauge metrics (current drift levels, active pipelines)
- **StatsD Integration:**
  - Real-time metric streaming
  - Datadog/Grafana compatibility
- **Metric Definitions:**
  - `kaldra_embedding_duration_seconds`
  - `kaldra_kindra_score_distribution`
  - `kaldra_tw369_drift_magnitude`
  - `kaldra_delta144_archetype_assignments`

**Impact:** Unified observability with existing infrastructure.

---

### **7.3 Distributed Tracing (OpenTelemetry)**

**Objective:** End-to-end visibility across KALDRA pipeline stages.

**Tasks:**
- **Span Creation:**
  - SentenceTransformer encoding span
  - Kindra LLM scoring span
  - Δ144 inference span
  - TW369 drift calculation span
- **Context Propagation:**
  - Trace IDs across async operations
  - Baggage for domain-specific metadata
- **Trace Sampling:**
  - Intelligent sampling strategies
  - Always sample errors and slow requests
- **Backend Integration:**
  - Jaeger for trace visualization
  - Zipkin compatibility
  - Cloud provider tracing (AWS X-Ray, GCP Trace)

**Impact:** Root cause analysis and performance optimization.

---

## 8. **Testing Roadmap**

### **8.1 Multi-Domain Test Suite**

**Objective:** Comprehensive validation across all KALDRA domains.

**Tasks:**
- **GEO Scoring Tests:**
  - Geopolitical event classification accuracy
  - Actor relationship extraction
  - Conflict intensity validation
- **Alpha Fundamental Narratives:**
  - Financial sentiment accuracy
  - Market event detection
  - Regulatory compliance scoring
- **Safeguard Toxicity & Bias:**
  - Toxicity detection precision/recall
  - Bias identification across demographics
  - False positive rate minimization
- **Cross-Domain Consistency:**
  - Ensure consistent behavior across domains
  - Archetype stability tests

**Impact:** Production-ready quality assurance.

---

### **8.2 Real Embedding Tests**

**Objective:** Validate embedding generation with actual providers.

**Tasks:**
- **SentenceTransformer Tests:**
  - Model loading and inference
  - Dimension validation
  - Performance benchmarks
- **OpenAI Embedding Tests:**
  - API integration
  - Rate limiting handling
  - Fallback behavior
- **Cohere Embedding Tests:**
  - Multi-language support
  - Batch processing
- **Fallback Chain Tests:**
  - Primary provider failure → fallback activation
  - Graceful degradation
  - Error propagation

**Impact:** Reliable embedding generation in production.

---

### **8.3 Drift Stability Long-Run**

**Objective:** Ensure TW369 drift calculations remain stable over extended periods.

**Tasks:**
- **Long-Run Simulations:**
  - 10,000+ drift evolution steps
  - Verify no runaway drift
  - Numerical stability checks
- **Edge Case Testing:**
  - Zero variance inputs
  - Extreme drift scenarios
  - Rapid narrative shifts
- **Convergence Analysis:**
  - Verify drift eventually stabilizes
  - Identify oscillation patterns
  - Validate damping effectiveness

**Impact:** Trustworthy drift metrics for long-term monitoring.

---

## 9. **Production Deployment Roadmap**

### **9.1 GPU Acceleration**

**Objective:** Maximize embedding and inference performance.

**Tasks:**
- **CUDA Support:**
  - GPU-accelerated SentenceTransformer
  - Batch inference optimization
  - Memory management for large models
- **ROCm Support:**
  - AMD GPU compatibility
  - Performance parity with CUDA
- **Multi-GPU Batching:**
  - Distribute embedding generation across GPUs
  - Load balancing strategies
  - Fault tolerance
- **Faiss Integration:**
  - GPU-accelerated vector search
  - Index building and querying
  - Approximate nearest neighbor search

**Impact:** 10-100x performance improvement for embedding-heavy workloads.

---

### **9.2 API Gateway Embeddings**

**Objective:** Production-ready REST API for KALDRA services.

**Tasks:**
- **Embedding Endpoint:**
  ```
  POST /v1/embedding
  {
    "texts": ["..."],
    "provider": "sentence-transformers",
    "model": "all-MiniLM-L6-v2"
  }
  ```
- **KALDRA Pipeline Endpoint:**
  ```
  POST /v1/kaldra/pipeline
  {
    "text": "...",
    "context": {...},
    "pipeline": "alpha"
  }
  ```
- **API Features:**
  - Authentication and authorization
  - Rate limiting
  - Request validation
  - Response caching
  - API versioning
- **Documentation:**
  - OpenAPI/Swagger specs
  - Interactive API explorer
  - Client SDK generation

**Impact:** Easy integration for external applications.

---

### **9.3 Frontend Integration**

**Objective:** Rich visualization and interaction with KALDRA results.

**Tasks:**
- **Embedding Viewer:**
  - Visualize embedding spaces
  - Similarity search interface
  - Cluster exploration
- **Drift Graphs:**
  - Real-time drift evolution charts
  - Historical drift timelines
  - Plane-specific drift breakdown
- **Archetype Distribution Heatmaps:**
  - 12×12 archetype grid visualization
  - Temporal archetype evolution
  - Narrative positioning in archetype space
- **Interactive Dashboards:**
  - Customizable widgets
  - Real-time updates via WebSocket
  - Export and sharing capabilities

**Impact:** Actionable insights for non-technical stakeholders.

---

## 10. **Appendix**

### **10.1 Fallback Rules**

**Embedding Provider Fallback Chain:**
1. Primary: SentenceTransformer (local)
2. Secondary: OpenAI (API)
3. Tertiary: Cohere (API)
4. Final: Dummy embeddings (development only)

**Scoring Fallback:**
1. Primary: LLM scoring
2. Secondary: Rule-based scoring
3. Tertiary: Default neutral scores

---

### **10.2 Embedding Profiles**

**Profile: Fast (Low Latency)**
- Model: `all-MiniLM-L6-v2`
- Dimensions: 384
- Inference: Local CPU
- Use case: Real-time applications

**Profile: Balanced (Default)**
- Model: `all-mpnet-base-v2`
- Dimensions: 768
- Inference: Local GPU
- Use case: General purpose

**Profile: Accurate (High Quality)**
- Model: `text-embedding-3-large` (OpenAI)
- Dimensions: 3072
- Inference: API
- Use case: Critical analysis

---

### **10.3 TW369 Config Presets**

**Preset: Default**
```yaml
damping: 0.5
lambda_severity: 1.0
planes:
  epistemic: true
  ontological: true
  axiological: true
```

**Preset: Conservative**
```yaml
damping: 0.8
lambda_severity: 0.7
planes:
  epistemic: true
  ontological: false
  axiological: true
```

**Preset: Exploratory**
```yaml
damping: 0.2
lambda_severity: 1.5
planes:
  epistemic: true
  ontological: true
  axiological: true
```

---

### **10.4 Kindra Scoring Modes**

**Mode: Rule-Based Only**
- Use: Highly structured data
- Alpha: 0.0 (no LLM)
- Speed: Fast
- Interpretability: High

**Mode: Hybrid (Default)**
- Use: General narratives
- Alpha: 0.5 (balanced)
- Speed: Medium
- Interpretability: Medium

**Mode: LLM-Dominant**
- Use: Complex, nuanced narratives
- Alpha: 0.8 (high LLM weight)
- Speed: Slow
- Interpretability: Low (requires explanations)

---

### **10.5 Future Architecture Diagrams**

**Planned Diagrams:**
- End-to-end pipeline flow (ingest → output)
- Multi-domain architecture overview
- Real-time streaming architecture
- Distributed tracing flow
- Frontend-backend integration

**Format:** Mermaid diagrams embedded in documentation

---

### **10.6 Links to Existing Specs**

- [KALDRA Core Master Roadmap](./KALDRA_CORE_MASTER_ROADMAP_V2.2.md)
- [Master Engine README](./README_MASTER_ENGINE_V2.md)
- [Master Tasklist](./KALDRA_CORE_MASTER_TASKLIST.md)
- [Embedding Generator Spec](../specs/embedding_generator_spec.md)
- [TW369 Engine Spec](../specs/tw369_spec.md)
- [Δ144 Engine Spec](../specs/delta144_spec.md)
- [Kindra Scoring Spec](../specs/kindra_scoring_spec.md)

---

## **Document Maintenance**

> **This document is auto-updatable in future sprints and acts as the master reference for all future development of KALDRA Core, Engine, Data Lab, and Embedding systems.**

**Update Frequency:** After each major sprint or architectural decision  
**Ownership:** KALDRA Core Team  
**Review Process:** Quarterly roadmap review and prioritization  
**Version Control:** Semantic versioning (MAJOR.MINOR for roadmap updates)

---

**End of Document**
