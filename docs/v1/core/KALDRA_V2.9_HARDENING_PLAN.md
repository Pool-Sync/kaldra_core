# KALDRA v2.9 Technical Plan — Hardening & Performance

**Codename:** Hardening & Performance
**Target Version:** v2.9
**Status:** DRAFT / PLANNING
**Date:** 2025-11-30

---

## 2.1. Overview

**Objective:** Transform KALDRA from an advanced experimental engine into a **hardened, performant, production-ready system**.

While versions v2.3–v2.8 focused on feature expansion (Real AI, Math Deepening, Meta-Engines, Story Arcs, Polarities, Guardian Layer), v2.9 focuses on **reliability, stability, and observability**. This version aims to ensure the system can handle failures gracefully, scale efficiently, and provide deep visibility into its operations.

**Core Scope:**
*   **Performance:** Optimize latency and throughput; reduce resource overhead.
*   **Hardening:** Implement robust error handling, timeouts, retries, and circuit breakers.
*   **Testing:** Expand test coverage to include load, stress, and chaos testing.
*   **Observability:** Implement structured logging, metrics, and tracing.
*   **Cleanup:** Remove legacy simulation code and technical debt.

---

## 2.2. Current State (Post v2.8)

The KALDRA architecture has grown significantly in complexity.

**Key Components:**
*   **Master Engine:** Orchestrates a complex pipeline (Input -> Tau -> Delta144 -> Kindra -> TW369 -> Meta -> Story -> Tau Output -> Safeguard).
*   **Δ12 / Δ144:** Now uses real embeddings and polarity modulation.
*   **Kindra 3×48:** Rule-based scoring with optional LLM and polarity hooks.
*   **TW369:** Mathematical drift engine with Painlevé solvers and Tracy-Widom statistics.
*   **Meta-Engines:** 12-axis analysis for Nietzsche, Aurelius, and Campbell.
*   **Story Engine:** Temporal aggregation and arc detection.
*   **Guardian Layer:** Tau (Epistemic) and Safeguard (Safety) layers.

**Fragilities & Risks:**
*   **No Timeouts:** External calls (LLM, Embeddings, Bias) and internal heavy computations (Painlevé) lack strict timeouts. A hung process could stall the entire pipeline.
*   **Fail-Fast vs. Fallback:** The system currently tends to fail fast or rely on ad-hoc `try/except` blocks. We need a unified fallback strategy.
*   **Resource Intensity:**
    *   **Painlevé Solver:** Can be CPU-intensive for certain regimes.
    *   **Embeddings:** Latency dependent on provider (OpenAI vs. Local).
    *   **Story Buffer:** In-memory growth potential if not capped strictly.
*   **Observability Gap:** We have logs, but no aggregated metrics (e.g., "average Tau score over last hour") or tracing IDs across the full lifecycle.

---

## 2.3. Performance & Latency (Plan)

**Goals (Targets, not Guarantees):**
*   **Latency (p95):**
    *   **LLM Off:** < 200ms (Internal math only)
    *   **LLM On:** < 2000ms (Dependent on provider, but internal overhead minimized)
*   **Throughput:** Capable of handling concurrent requests without state corruption (Master Engine is stateless per request, but shared resources need checking).

**Performance Audit Plan:**
> **Perf Audit — Implemented** (see `perf/` directory)
1.  **Profiling:** Use `cProfile` or similar to identify bottlenecks in:
    *   `TWPainleveOracle` (Solver iterations)
    *   `Delta144Engine` (Vector operations)
    *   `StoryAggregator` (History traversal)
2.  **Optimization Candidates:**
    *   **Vectorization:** Ensure all numpy operations are fully vectorized.
    *   **Caching:** Cache embedding results for identical inputs? (LRU Cache).
    *   **Lazy Loading:** Ensure heavy models/tables are loaded only once.

**Proposed Test Files:**
*   `tests/perf/test_pipeline_perf.py`: Benchmark full inference cycle.
*   `tests/perf/test_tw369_perf.py`: Benchmark solver performance.
*   `tests/perf/test_story_engine_perf.py`: Benchmark aggregation with full buffers.

---

## 2.4. Hardening & Failures (Plan)

**Strategy:** "Graceful Degradation" — The system should never crash; it should return the best possible signal given the available components.

**Failure Handling:**
*   **LLM/Embeddings:**
    *   If unavailable -> Fallback to Legacy/Heuristic mode immediately.
    *   Log error with `WARN` level.
    *   Flag result as `degraded: true`.
*   **Bias / Safeguard / Tau:**
    *   If analysis fails -> Assume "High Risk" (Fail Safe) or "Neutral" depending on config.
    *   Safeguard failure -> Default to `BLOCK_OUTPUT` if critical, or `FLAG_RISK` if minor.
*   **Data Corruption:**
    *   Schema validation on inputs.
    *   `try/except` blocks around all JSON parsing and state loading.

**Resilience Patterns:**
*   **Timeouts:** Enforce strict timeouts on all network calls (e.g., 5s for LLM).
*   **Retries:** Exponential backoff for transient network errors (max 3 retries).
*   **Circuit Breakers:** If an external service fails N times, stop calling it for X minutes and use fallback.

**Validation:**
*   Ensure `KaldraSignal` is always returned, even if populated with default/safe values.

---

## 2.5. Test Strategy v2.9

**Unit Tests:**
*   Focus on edge cases in new v2.8 modules (Tau/Safeguard).
*   Test fallback logic in `EmbeddingGenerator` and `KindraLLMScorer`.

**Integration Tests:**
*   **Full Pipeline:** Verify interaction of all components.
*   **Degraded Modes:** Verify pipeline behavior when specific components are disabled/mock-failed.

**Load & Stress Tests:**
*   **Soak Test:** Run engine for 1 hour with continuous inputs to check for memory leaks.
*   **Burst Test:** Send 100 requests in parallel (if async supported) or rapid sequence.

**Chaos Tests:**
*   Simulate random failures in dependencies (Mock side effects).
*   Simulate slow responses (latency injection).

**Proposed Test Files:**
*   `tests/hardening/test_failover_llm.py`
*   `tests/hardening/test_failover_bias_and_safeguard.py`
*   `tests/hardening/test_tau_clamp_behavior.py`
*   `tests/story/test_story_engine_under_load.py`

---

## 2.6. Observability & Logging

**Metrics (to be exposed via logs or future metrics endpoint):**
*   **Latency:** `inference_time_ms`, `component_time_ms` (breakdown).
*   **Errors:** Count of exceptions by module.
*   **Business Metrics:**
    *   `avg_tau_score`
    *   `safeguard_trigger_rate`
    *   `drift_velocity_avg`

**Logging Standard:**
*   **Format:** JSON structured logs.
*   **Context:** All logs must include `request_id`.
*   **Levels:**
    *   `INFO`: High-level flow (Inference Start/End).
    *   `DEBUG`: Detailed internal state (only when enabled).
    *   `WARN`: Fallbacks, non-critical failures.
    *   `ERROR`: Unhandled exceptions, critical failures.

**Tracing:**
*   Pass `request_id` through all function calls in the pipeline.

---

## 2.7. API & Frontend Impact (Plan)

**API Gateway:**
*   Include `x-kaldra-status` header in responses (e.g., `ok`, `degraded`).
*   Expose `risk_summary` and `tau_score` in the standard response body.

**Frontend (4iam.ai):**
*   **Status Indicator:** Show "System Health" based on Tau/Safeguard signals.
*   **Degraded Mode UI:** If running on fallbacks, show a subtle indicator (e.g., "Running in Offline Mode").
*   **Latency Indicator:** Visual cue if processing is taking longer than usual.

---

## 2.8. Cleanup & Legacy

**Candidates for Removal/Refactoring:**
*   **Simulation Stubs:** Remove any v2.2-era simulation code that is fully replaced by v2.3+ implementations.
*   **Deprecated Configs:** Clean up unused keys in `config.py`.
*   **Documentation:** Archive or update outdated specs (pre-v2.6).
*   **TODOs:** Audit codebase for critical TODOs and resolve them.

---

## 2.9. Execution Plan v2.9 (Phases)

**Phase 1: Perf Audit & Profiling**
*   **Goal:** Identify bottlenecks.
*   **Deliverables:** Profiling report, optimization plan.

**Phase 2: Hardening Implementation**
*   **Goal:** Implement timeouts, retries, and fallbacks.
*   **Deliverables:** Updated `EmbeddingGenerator`, `KindraLLMScorer`, `KaldraMasterEngine`.

**Phase 3: Test Suite Expansion**
*   **Goal:** Verify robustness.
*   **Deliverables:** `tests/hardening/`, `tests/perf/`.

**Phase 4: Observability**
*   **Goal:** Visibility into system health.
*   **Deliverables:** Structured logging updates, metrics collection hooks.

**Phase 5: Cleanup & Legacy**
*   **Goal:** Technical debt reduction.
*   **Deliverables:** Cleaned codebase, updated docs.

**Phase 6: Release**
*   **Goal:** Official v2.9 release.
*   **Deliverables:** Release Notes, Changelog, Roadmap Update.
