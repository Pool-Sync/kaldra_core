# KALDRA v2.9 Release Notes
**Codename:** HARDENING & PERFORMANCE
**Version:** 2.9.0
**Status:** STABLE
**Date:** 2025-11-30

## 2.9.1 — Overview
KALDRA v2.9 transforms the experimental engine into a production-ready system. It introduces a comprehensive hardening layer, performance profiling, and deep observability.

## 2.9.2 — What Changed
*   **Hardening Layer**:
    *   **Timeouts**: Strict limits on all external and heavy internal calls.
    *   **Retries**: Exponential backoff for transient failures.
    *   **Circuit Breakers**: Automatic failover when services (LLM, Embeddings) become unstable.
    *   **Global Degraded Mode**: The Master Engine now catches all exceptions and returns a valid (but degraded) signal instead of crashing.
*   **Performance**:
    *   **Profiling Suite**: New `perf/` module for benchmarking pipeline, TW369, and Story Engine.
*   **Observability**:
    *   **Structured Logging**: JSON-based logs with `request_id` propagation.
    *   **Metrics**: Hooks for tracking Tau Scores, Drift Velocity, and Error Rates.
*   **Testing**:
    *   New test suites for Hardening, Chaos, and Performance.

## 2.9.3 — Technical Details
*   **New Modules**: `src/core/hardening/`, `src/core/observability/`, `perf/`.
*   **Modified**: `KaldraMasterEngineV2` now wraps all phases in try/except blocks.
*   **Decorators**: `@with_timeout`, `@with_retries`, `@circuit_breaker`, `@safe_fallback`.

## 2.9.4 — Backward Compatibility
*   **Fully Compatible**: The API surface remains the same.
*   **New Output Field**: `KaldraSignal` now includes `degraded: bool`.
