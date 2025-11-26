# KALDRA Core v2.2 — Testing Strategy

**Version**: 2.2  
**Date**: 2025-11-26  
**Status**: Production-Ready  
**Total Tests**: 140 passing

---

## Overview

The KALDRA Core testing strategy is designed to validate a **multi-layered narrative intelligence system** that combines mathematical rigor with cultural sensitivity. Our testing philosophy emphasizes:

1. **Deterministic Reproducibility**: All tests use fixed random seeds to ensure consistent results across environments and CI/CD pipelines.
2. **Hierarchical Validation**: Tests validate each layer independently (Kindra → TW369 → Δ144) and the complete integrated pipeline.
3. **Mathematical Soundness**: Probability distributions, drift calculations, and state transitions are verified for numerical stability.
4. **Performance Baselines**: Explicit time bounds prevent performance regressions.

### Why Deterministic Testing?

KALDRA processes narrative embeddings through multiple stochastic transformations:
- **Kindra Cultural Modulation**: Context-dependent scoring
- **TW369 Drift Calculation**: Temporal evolution modeling
- **Δ144 Archetype Distribution**: Probabilistic state representation

Deterministic testing ensures that:
- Results are reproducible for debugging
- Performance comparisons are valid across versions
- CI/CD pipelines produce consistent outcomes
- Mathematical properties (normalization, bounds) are reliably verified

---

## Test Suite Structure

```
tests/
├── core/                          # Core engine unit tests
│   ├── test_tw369.py             # TW369 drift mathematics (19 tests)
│   ├── test_tw369_edge_cases.py  # TW369 boundary conditions (3 tests)
│   ├── test_config_edge_cases.py # Configuration validation (2 tests)
│   ├── test_kindras.py           # Kindra infrastructure
│   ├── test_meta.py              # Meta-engine routing
│   └── test_bias.py              # Bias detection
│
├── kindras/                       # Kindra scoring tests
│   ├── test_layer1_*.py          # Layer 1 Cultural Macro (7 tests)
│   ├── test_layer2_*.py          # Layer 2 Semiotic Media (6 tests)
│   ├── test_layer3_*.py          # Layer 3 Structural Systemic (4 tests)
│   ├── test_llm_scorer.py        # LLM-based scoring (6 tests)
│   ├── test_hybrid_scorer.py     # Hybrid scoring (6 tests)
│   └── test_scoring_edge_cases.py # Edge cases (3 tests)
│
├── delta144/                      # Δ144 archetype engine tests
│   └── test_delta144_edge_cases.py # Edge cases (2 tests)
│
├── integration/                   # End-to-end pipeline tests
│   └── test_full_pipeline.py     # Complete pipeline (8 tests)
│
└── performance/                   # Stress and performance tests
    └── test_stress.py            # Load testing (3 tests)
```

**Total Coverage**: 140 tests across 5 categories

---

## Test Categories and Responsibilities

### 1. Unit Tests

**Purpose**: Validate individual components in isolation

#### TW369 Engine Tests (19 tests)
- Drift calculation accuracy
- Severity computation
- Plane tension gradients
- Painlevé II filter integration
- Adaptive state-plane mapping
- Advanced drift models (B, C, D)
- Numerical stability under extreme values

#### Kindra Scoring Tests (29 tests)
- Layer 1: Cultural macro scoring (7 countries, 6 sectors)
- Layer 2: Semiotic media scoring (4 tones, 7 channels)
- Layer 3: Structural systemic scoring (3 parameters)
- LLM-based scoring with fallback
- Hybrid scoring (alpha mixing)
- Rule-based deterministic scoring

#### Configuration Tests (2 tests)
- Engine initialization with different `tau` values
- Context dimension (`d_ctx`) validation
- Parameter bounds checking

### 2. Integration Tests (8 tests)

**Purpose**: Validate complete pipeline from embedding to archetype distribution

#### Core Pipeline Tests
```python
test_full_pipeline_basic()
# embedding → Δ144 → Kindra → TW369 → Epistemic → KaldraSignal
# Validates: structure, normalization, epistemic decision
```

#### Determinism Validation
```python
test_full_pipeline_determinism()
# Same input → Same output (with fixed seed)
# Validates: reproducibility, numerical consistency
```

#### TW Oracle Behavior
```python
test_full_pipeline_tw_window_low_tension()
# Zero-valued TW window → Stable distribution
# Validates: no pathological behavior under low tension

test_full_pipeline_tw_window_high_tension()
# High-valued TW window (5.0) → Bounded, finite output
# Validates: numerical stability under extreme tension
```

#### Probability Validity
```python
test_full_pipeline_probability_validity()
# Validates: probs ∈ [0,1], sum ≈ 1.0
```

### 3. Stress Tests (3 tests)

**Purpose**: Validate performance and robustness under load

#### Many Inferences Test
```python
test_stress_many_inferences()
# 100 embeddings → 100 KaldraSignals
# Baseline: ~1.5s total (~0.015s/item)
# Bound: < 30s total
```

#### TW369 Drift Evolution Test
```python
test_stress_tw369_drift_evolution()
# 500 drift calculations with state updates
# Baseline: ~0.5s total
# Bound: < 10s total
# Validates: no NaN/Inf, numerical stability
```

#### Batch Processing Test
```python
test_stress_batch_processing()
# 50 embeddings in batch
# Baseline: ~1.5s total (~0.03s/item)
# Bound: avg < 1s/item
```

### 4. Edge Case Tests (10 tests)

**Purpose**: Validate robustness at boundaries and extreme conditions

#### TW369 Edge Cases (3 tests)
- **Zero State**: All plane values = 0 → No division by zero
- **Extreme Values**: Plane values at ±1.0 → Bounded drift
- **Mixed State**: Positive/negative mix → Stable computation

#### Kindra Edge Cases (3 tests)
- **Empty Embedding**: Zero vector → Valid output
- **Extreme Values**: Large embeddings (×1000) → Finite probabilities
- **Negative Embedding**: All-negative → Valid distribution

#### Δ144 Edge Cases (2 tests)
- **Zero Embedding**: Zero vector → No crash
- **Random Embedding**: Valid probability structure

#### Config Edge Cases (2 tests)
- **Different Tau**: 0.5 vs 0.9 → Correct initialization
- **Different d_ctx**: 128 vs 512 → Correct layer shapes

---

## Deterministic Execution Policy

### Random Number Generation

All tests use **NumPy's modern RNG** with fixed seeds:

```python
# Global seed for reproducibility
RNG_SEED = 42
rng = np.random.default_rng(RNG_SEED)

# Fixture for deterministic embeddings
@pytest.fixture
def sample_embedding():
    return rng.standard_normal(256, dtype=np.float32)

# Local seed for specific tests
rng_local = np.random.default_rng(123)
```

### Seed Usage
- **Seed 42**: Default for all integration and edge case tests
- **Seed 123**: Used in `test_full_pipeline_different_inputs` to ensure variation

### Benefits
1. **CI/CD Consistency**: Same results across different machines
2. **Debugging**: Reproducible failures
3. **Performance Comparison**: Valid benchmarks across versions
4. **Regression Detection**: Deterministic outputs enable exact comparisons

---

## Official Performance Baselines

### Hardware Context
- **Platform**: macOS (Darwin)
- **Python**: 3.13.5
- **Test Framework**: pytest 9.0.1

### Baseline Metrics

#### Inference Stress Test
```
Test: test_stress_many_inferences
Input: 100 random embeddings (256-dim)
Baseline: ~1.5s total (~0.015s per inference)
Bound: < 30s total
Status: ✅ PASSING
```

#### TW369 Drift Stress Test
```
Test: test_stress_tw369_drift_evolution
Input: 500 drift calculation iterations
Baseline: ~0.5s total (~0.001s per iteration)
Bound: < 10s total
Status: ✅ PASSING
```

#### Batch Processing Test
```
Test: test_stress_batch_processing
Input: 50 embeddings in batch
Baseline: ~1.5s total (~0.03s per item)
Bound: avg < 1s per item
Status: ✅ PASSING
```

### Performance Assertions

All stress tests include **explicit time bounds** to prevent regressions:

```python
assert total_time < 10.0  # TW369 drift
assert total_time < 30.0  # Many inferences
assert avg_time < 1.0     # Batch processing
```

---

## Probability Constraints Verification

### Normalization Checks

All tests verify that archetype probability distributions satisfy:

```python
# Sum constraint (with tolerance for floating-point)
assert np.isclose(probs.sum(), 1.0, atol=0.01)

# Non-negativity
assert np.all(probs >= 0)

# Upper bound
assert np.all(probs <= 1)

# Finite values (no NaN/Inf)
assert np.all(np.isfinite(probs))
```

### Drift Stability

TW369 drift calculations are verified for:

```python
# No numerical explosions
for val in drift.values():
    assert not np.isnan(val)
    assert not np.isinf(val)

# Bounded drift values
assert -10.0 <= drift_val <= 10.0
```

### TW Window Behavior

TW oracle behavior is validated under extreme conditions:

```python
# Low tension (zeros) → Stable distribution
tw_window = np.zeros((10, 5))
result = engine.infer_from_embedding(emb, tw_window)
assert np.isclose(result.archetype_probs.sum(), 1.0)

# High tension (5.0) → Finite, bounded output
tw_window = np.full((10, 5), 5.0)
result = engine.infer_from_embedding(emb, tw_window)
assert np.all(np.isfinite(result.archetype_probs))
```

---

## Testing Commands

### Basic Test Execution

```bash
# Run all tests quietly
pytest -q

# Stop on first failure
pytest --disable-warnings --maxfail=1

# Run specific test file
pytest tests/integration/test_full_pipeline.py -v

# Run with markers
pytest -m slow  # Run only stress tests
```

### Coverage Analysis

```bash
# Generate coverage report
pytest --cov=src --cov-report=term-missing

# HTML coverage report
pytest --cov=src --cov-report=html

# Coverage for specific module
pytest --cov=src/tw369 --cov-report=term
```

### Performance Profiling

```bash
# Run stress tests with timing
pytest tests/performance/test_stress.py -v -s

# Profile specific test
pytest tests/performance/test_stress.py::test_stress_tw369_drift_evolution -v -s
```

---

## Future Test Expansion

### Multi-Domain Testing (Roadmap v2.3)

Expand integration tests to cover all application domains:

```python
# KALDRA-Alpha (Finance)
test_alpha_earnings_call_pipeline()
test_alpha_market_sentiment_analysis()

# KALDRA-GEO (Geopolitics)
test_geo_regional_tension_detection()
test_geo_narrative_risk_assessment()

# KALDRA-Product (UX)
test_product_review_analysis()
test_product_feature_sentiment()

# KALDRA-Safeguard (Content Safety)
test_safeguard_toxicity_detection()
test_safeguard_bias_monitoring()
```

### Scoring Mode Validation

Test all scoring modes comprehensively:

```python
# Rule-based scoring (deterministic)
test_rule_based_scoring_consistency()

# LLM-based scoring (with mocked API)
test_llm_scoring_with_fallback()

# Hybrid scoring (alpha mixing)
test_hybrid_alpha_interpolation()
test_hybrid_layer_specific_alpha()
```

### Meta-Engine Routing Tests

Validate meta-engine selection and orchestration:

```python
# Nietzsche meta-engine
test_nietzsche_philosophical_routing()

# Campbell meta-engine
test_campbell_heroic_narrative_routing()

# Aurelius meta-engine
test_aurelius_stoic_routing()

# Fallback mechanisms
test_meta_engine_graceful_degradation()
```

### Advanced Mathematical Tests

```python
# Painlevé II filter validation
test_painleve_filter_numerical_stability()
test_painleve_edge_correction()

# Advanced drift models
test_drift_model_b_nonlinear()
test_drift_model_c_multiscale()
test_drift_model_d_stochastic()

# Adaptive state-plane mapping
test_adaptive_mapping_domain_specific()
test_adaptive_mapping_severity_shift()
```

---

## Future Implementations

### Regression Test Suite
- **Automated version comparison**: Compare outputs between v2.2 and v2.3
- **Breaking change detection**: Flag API signature changes
- **Performance regression alerts**: Automated baseline comparison

### Story-Level Testing
- **Multi-turn coherence**: Validate narrative consistency across conversation turns
- **Temporal evolution**: Test Δ144 distribution changes over time
- **Session management**: Validate story tracking and aggregation

### Real-Time Testing
- **Streaming pipeline tests**: Validate real-time narrative processing
- **Latency benchmarks**: Sub-100ms inference targets
- **Concurrent request handling**: Multi-threaded stress tests

### Database Integration Tests
- **Cultural database queries**: Validate Layer 1/2/3 data retrieval
- **Mapping cache validation**: Test Kindra → Δ144 mapping lookups
- **Schema migration tests**: Validate database version upgrades

---

## Enhancements

### Coverage Expansion
- **Target**: 95%+ code coverage across all modules
- **Focus areas**: Error handling paths, edge cases in meta-routing
- **Tools**: pytest-cov with branch coverage analysis

### Test Automation
- **CI/CD integration**: GitHub Actions for automated test runs
- **Pre-commit hooks**: Run fast tests before commits
- **Nightly builds**: Full test suite + performance benchmarks

### Performance Optimization
- **Parallel test execution**: pytest-xdist for faster runs
- **Test caching**: pytest-cache for incremental testing
- **Profiling integration**: cProfile for bottleneck identification

### Documentation
- **Test case documentation**: Docstrings for all test functions
- **Failure analysis guides**: Common failure patterns and fixes
- **Contribution guidelines**: How to add new tests

---

## Research Track

### Probabilistic Testing
- **Property-based testing**: Use Hypothesis for generative test cases
- **Statistical validation**: Chi-square tests for distribution uniformity
- **Monte Carlo verification**: Validate drift convergence properties

### Painlevé II Mathematical Validation
- **Numerical solver accuracy**: Compare against analytical solutions
- **Stability analysis**: Lyapunov exponents for drift models
- **Phase space exploration**: Validate attractor behavior

### Advanced Drift Models
- **Model comparison framework**: Systematic evaluation of Models A/B/C/D
- **Hyperparameter sensitivity**: Grid search for optimal drift parameters
- **Convergence analysis**: Validate long-term drift behavior

### Cultural Database Validation
- **Cross-cultural consistency**: Validate scoring across all 48 vectors
- **Temporal stability**: Test cultural scores over time
- **Expert validation**: Compare automated scores with human annotations

---

## Known Limitations

### Current Test Gaps

1. **LLM Integration**: Tests use dummy/mocked LLM clients
   - **Impact**: Real LLM behavior not validated
   - **Mitigation**: Use deterministic fallback for CI/CD

2. **Bias Engine**: Bias detection uses placeholder implementation
   - **Impact**: Safeguard domain not fully tested
   - **Mitigation**: Structural tests ensure no crashes

3. **Real Embeddings**: Tests use random embeddings, not real text
   - **Impact**: Semantic validity not tested
   - **Mitigation**: Integration tests validate mathematical properties

4. **Multi-Language**: No tests for non-English narratives
   - **Impact**: Cultural scoring may not generalize
   - **Mitigation**: Framework supports future expansion

### Performance Limitations

1. **Stress Test Scale**: Maximum 500 iterations tested
   - **Impact**: Long-running behavior unknown
   - **Mitigation**: Conservative time bounds prevent hangs

2. **Memory Profiling**: No explicit memory leak tests
   - **Impact**: Memory usage under load not validated
   - **Mitigation**: Stress tests run in bounded time

3. **Concurrent Execution**: No multi-threaded tests
   - **Impact**: Thread safety not validated
   - **Mitigation**: Single-threaded execution guaranteed

### Coverage Gaps

1. **Meta-Engine Routing**: Routing logic partially tested
   - **Current Coverage**: ~30%
   - **Target**: 90%+ (v2.3)

2. **Story Aggregation**: Multi-turn logic not tested
   - **Current Coverage**: 0%
   - **Target**: Full coverage (v2.4)

3. **Error Recovery**: Exception handling paths undertested
   - **Current Coverage**: ~40%
   - **Target**: 80%+ (v2.3)

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-26  
**Maintained By**: KALDRA Core Team  
**Review Cycle**: Quarterly
