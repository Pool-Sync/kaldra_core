# KALDRA Code Coverage Report v2.9

Generated on: Sun Nov 30 08:45:31 -03 2025

## Summary

This report identifies potentially unused Python files in the KALDRA codebase.

## Methodology

- Scanned all Python files in `src/`
- Built import dependency graph
- Identified files that are never imported
- Excluded: `__init__.py`, `*main*.py`, `config.py`

## Potentially Dead Files

Found 44 potentially unused files:

- src/apps/alpha/analyzer.py
- src/apps/alpha/earnings_analyzer.py
- src/apps/alpha/earnings_ingest.py
- src/apps/alpha/earnings_pipeline.py
- src/apps/alpha/ingest.py
- src/apps/geo/geo_analyzer.py
- src/apps/geo/geo_ingest.py
- src/apps/geo/geo_risk_engine.py
- src/apps/geo/geo_signals.py
- src/apps/product/product_analyzer.py
- src/apps/product/product_ingest.py
- src/apps/product/product_kindra_mapping.py
- src/apps/safeguard/bias_monitor.py
- src/apps/safeguard/narrative_guard.py
- src/apps/safeguard/toxicity_detector.py
- src/archetypes/api_adapter.py
- src/archetypes/delta12_vector.py
- src/archetypes/delta144_engine.py
- src/archetypes/polarity_mapping.py
- src/archetypes/tw_delta_bridge.py
- src/bias/detector.py
- src/bias/mitigation.py
- src/bias/providers/base.py
- src/bias/providers/heuristic.py
- src/bias/providers/perspective.py
- src/bias/scoring.py
- src/common/unified_signal.py
- src/common/unified_state.py
- src/core/audit_trail.py
- src/core/cache_utils.py
- src/core/embedding_cache.py
- src/core/embedding_generator.py
- src/core/epistemic_limiter.py
- src/core/hardening/circuit_breaker.py
- src/core/hardening/fallbacks.py
- src/core/hardening/retries.py
- src/core/hardening/timeouts.py
- src/core/kaldra_engine_pipeline.py
- src/core/kaldra_logger.py
- src/core/kaldra_master_engine.py
- src/core/observability/logging.py
- src/core/observability/metrics.py
- src/core/story_aggregator.py
- src/core/story_tracker.py

## Recommendations

1. **Review** each file listed above
2. **Verify** it's truly unused (may be used dynamically or in tests)
3. **Archive or Delete** confirmed dead code

## Notes

- This is a heuristic analysis
- Dynamic imports (e.g., `importlib`) are not detected
- Test files may import modules not shown here
- Entry points and scripts may not be imported but are still needed
