# KALDRA CORE — PIPELINE VALIDATION GUIDE

**Version**: 2.1  
**Date**: 2025-11-24  
**Purpose**: Comprehensive validation procedures for KALDRA Core

---

## OVERVIEW

This guide provides step-by-step validation procedures to ensure the KALDRA Core pipeline is functioning correctly across all components.

**Validation Levels**:
1. **Component-Level** — Individual engine validation
2. **Integration-Level** — Cross-engine validation
3. **End-to-End** — Full pipeline validation
4. **Production-Level** — Performance and reliability

---

## 1. COMPONENT-LEVEL VALIDATION

### 1.1 Δ144 Engine Validation

**Objective**: Verify Δ144 engine loads schemas and produces valid distributions

**Commands**:
```bash
cd /Users/niki/Desktop/kaldra_core

# Run Δ144 tests
pytest tests/core/test_delta144.py -v
pytest tests/test_delta144_engine.py -v

# Expected: All tests pass
```

**Manual Validation**:
```python
from src.archetypes.delta144_engine import Delta144Engine
import numpy as np

# Initialize engine
engine = Delta144Engine.from_default_files(d_ctx=256)

# Create test embedding
embedding = np.random.randn(256)

# Infer state
result = engine.infer_from_vector(embedding)

# Validate
assert result.probs is not None
assert len(result.probs) == 144
assert np.isclose(np.sum(result.probs), 1.0, atol=0.01)
print("✅ Δ144 Engine Valid")
```

**Checklist**:
- [ ] All 4 schemas load successfully
- [ ] Inference produces 144-dimensional distribution
- [ ] Distribution sums to ~1.0
- [ ] State ID is valid
- [ ] No errors or warnings

---

### 1.2 Kindra Loaders Validation

**Objective**: Verify all 3 layers load 48 vectors correctly

**Commands**:
```bash
# Run loader tests
pytest tests/kindras/test_loaders.py -v

# Expected: 7/7 tests pass
```

**Manual Validation**:
```python
from src.kindras.layer1_cultural_macro_loader import Layer1Loader
from src.kindras.layer2_semiotic_media_loader import Layer2Loader
from src.kindras.layer3_structural_systemic_loader import Layer3Loader

# Load all layers
l1 = Layer1Loader("schema/kindras/kindra_vectors_layer1_cultural_macro_48.json")
l2 = Layer2Loader("schema/kindras/kindra_vectors_layer2_semiotic_media_48.json")
l3 = Layer3Loader("schema/kindras/kindra_vectors_layer3_structural_systemic_48.json")

# Validate
assert len(l1.vectors) == 48
assert len(l2.vectors) == 48
assert len(l3.vectors) == 48

# Check vector structure
v = l1.get_vector("E01")
assert v.id == "E01"
assert v.layer == "L1_CULTURAL_MACRO"
assert v.tw_plane == "3"
assert v.scale_type is not None
assert v.scale_direction is not None

print("✅ All Kindra Loaders Valid")
```

**Checklist**:
- [ ] Layer 1 loads 48 vectors
- [ ] Layer 2 loads 48 vectors
- [ ] Layer 3 loads 48 vectors
- [ ] All vectors have required fields
- [ ] Domain filtering works
- [ ] No duplicate IDs

---

### 1.3 Kindra Scorers Validation

**Objective**: Verify scorers produce valid scores

**Commands**:
```bash
# Run scorer tests
pytest tests/kindras/test_scorers_bridges.py::TestScorers -v
```

**Manual Validation**:
```python
from src.kindras.layer1_cultural_macro_scoring import Layer1Scorer

scorer = Layer1Scorer()
loader = Layer1Loader("schema/kindras/kindra_vectors_layer1_cultural_macro_48.json")

context = {
    "layer1_overrides": {
        "E01": 0.8,
        "S09": -0.5
    }
}

scores = scorer.score(context, loader.get_all_vectors())

# Validate
assert len(scores) == 48
assert scores["E01"] == 0.8
assert scores["S09"] == -0.5
assert all(-1.0 <= v <= 1.0 for v in scores.values())

print("✅ Kindra Scorers Valid")
```

**Checklist**:
- [ ] Scorers return 48 scores
- [ ] Scores in range [-1.0, 1.0]
- [ ] Overrides work correctly
- [ ] Default scores are 0.0

---

### 1.4 Kindra Bridges Validation

**Objective**: Verify bridges apply scores to Δ144 correctly

**Commands**:
```bash
# Run bridge tests
pytest tests/kindras/test_scorers_bridges.py::TestBridges -v
```

**Manual Validation**:
```python
from src.kindras.layer1_delta144_bridge import Layer1Delta144Bridge

bridge = Layer1Delta144Bridge("schema/kindras/kindra_layer1_to_delta144_map.json")

base_dist = {f"STATE_{i:03d}": 1.0 for i in range(144)}
kindra_scores = {"E01": 0.5, "S09": -0.3}

adjusted = bridge.apply(base_dist, kindra_scores)

# Validate
assert len(adjusted) == 144
assert all(v >= 0 for v in adjusted.values())
# Note: With empty mappings, distribution should be unchanged

print("✅ Kindra Bridges Valid")
```

**Checklist**:
- [ ] Bridges load mapping files
- [ ] Apply method returns 144 values
- [ ] All values non-negative
- [ ] Boost/suppress logic works (when mappings populated)
- [ ] Negative scores invert logic

---

### 1.5 TW369 Validation

**Objective**: Verify TW Oracle and Integration work

**Commands**:
```bash
# Run TW369 tests
pytest tests/core/test_tw369.py -v
pytest tests/test_tw_oracle.py -v
```

**Manual Validation**:
```python
from src.tw369.oracle_tw_painleve import TWPainleveOracle, TWConfig
from src.tw369.tw369_integration import TW369Integrator
import numpy as np

# Test Oracle
oracle = TWPainleveOracle(TWConfig(window_size=50, alpha=0.99))
window = np.random.randn(50, 16)
trigger, stats = oracle.detect(window)

assert isinstance(trigger, bool)
assert stats.lambda_max > 0
assert stats.threshold > 0

# Test Integrator
integrator = TW369Integrator()
tw_state = integrator.create_state(
    layer1_scores={"E01": 0.5},
    layer2_scores={"S09": 0.3},
    layer3_scores={"P17": -0.2}
)

assert tw_state.plane3_cultural_macro == {"E01": 0.5}
assert tw_state.plane6_semiotic_media == {"S09": 0.3}
assert tw_state.plane9_structural_systemic == {"P17": -0.2}

print("✅ TW369 Valid")
```

**Checklist**:
- [ ] Oracle detects events
- [ ] TWState creation works
- [ ] Drift calculation runs (even if placeholder)
- [ ] Evolve method runs

---

### 1.6 Epistemic Limiter Validation

**Objective**: Verify τ layer makes correct decisions

**Commands**:
```bash
# Run epistemic tests
pytest tests/test_epistemic_limiter.py -v
```

**Manual Validation**:
```python
from src.core.epistemic_limiter import EpistemicLimiter
import numpy as np

limiter = EpistemicLimiter(tau=0.65)

# High confidence case
probs_high = np.zeros(144)
probs_high[0] = 0.8
probs_high[1:] = 0.2 / 143

decision = limiter.from_probs(probs_high)
assert decision.status == "OK"
assert decision.delegate == False
assert decision.confidence >= 0.65

# Low confidence case
probs_low = np.ones(144) / 144
decision = limiter.from_probs(probs_low)
assert decision.status == "INCONCLUSIVO"
assert decision.delegate == True

print("✅ Epistemic Limiter Valid")
```

**Checklist**:
- [ ] High confidence → OK status
- [ ] Low confidence → INCONCLUSIVO
- [ ] Threshold τ respected
- [ ] Delegate flag correct

---

## 2. INTEGRATION-LEVEL VALIDATION

### 2.1 Master Engine Pipeline Validation

**Objective**: Verify complete Master Engine flow

**Commands**:
```bash
# Run master engine tests
pytest tests/test_master_engine_v2.py -v
pytest tests/test_integration_master_engine.py -v
```

**Manual Validation**:
```python
from src.core.kaldra_master_engine import KaldraMasterEngineV2
import numpy as np

engine = KaldraMasterEngineV2()

# Create test inputs
embedding = np.random.randn(256)
tw_window = np.random.randn(50, 16)

# Run inference
signal = engine.infer_from_embedding(embedding, tw_window=tw_window)

# Validate
assert signal.archetype_probs.shape == (144,)
assert isinstance(signal.tw_trigger, bool)
assert signal.epistemic.status in ["OK", "INCONCLUSIVO"]
assert signal.delta_state is not None

print("✅ Master Engine Pipeline Valid")
```

**Checklist**:
- [ ] Engine initializes all components
- [ ] Inference runs without errors
- [ ] Signal contains all fields
- [ ] Δ144 → Kindra → TW → τ flow works

---

### 2.2 Kindra Pipeline Validation

**Objective**: Verify Kindra-specific pipeline

**Commands**:
```bash
# Run Kindra pipeline tests
pytest tests/core/test_pipeline.py -v

# Expected: 3/3 tests pass
```

**Manual Validation**:
```python
from src.core.kaldra_engine_pipeline import KALDRAEnginePipeline

pipeline = KALDRAEnginePipeline(schema_base_path="schema/kindras")

base_delta144 = {f"STATE_{i:03d}": 1.0 for i in range(144)}
context = {
    "country": "BR",
    "layer1_overrides": {"E01": 0.5},
    "layer2_overrides": {"S09": 0.3},
    "layer3_overrides": {"P17": -0.2}
}

result = pipeline.process(base_delta144, context, evolve_steps=0)

# Validate
assert "final_distribution" in result
assert "layer1_scores" in result
assert "layer2_scores" in result
assert "layer3_scores" in result
assert "intermediate_distributions" in result
assert "tw_state" in result

assert result["layer1_scores"]["E01"] == 0.5
assert result["layer2_scores"]["S09"] == 0.3
assert result["layer3_scores"]["P17"] == -0.2

print("✅ Kindra Pipeline Valid")
```

**Checklist**:
- [ ] Pipeline initializes all components
- [ ] Sequential layer application works
- [ ] Intermediate distributions tracked
- [ ] TW369 integration works

---

## 3. END-TO-END VALIDATION

### 3.1 Full System Test

**Objective**: Validate complete system from text input to signal output

**Test Script**:
```python
# test_e2e.py
from src.core.kaldra_master_engine import KaldraMasterEngineV2
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize
engine = KaldraMasterEngineV2()
encoder = SentenceTransformer('all-MiniLM-L6-v2')  # If available

# Test text
text = "The CEO is optimistic about revenue growth and market expansion."

# Generate embedding
embedding = encoder.encode(text)

# Run inference
signal = engine.infer_from_embedding(embedding)

# Validate
print(f"Top Archetype: {signal.delta_state['archetype_id']}")
print(f"Confidence: {signal.epistemic.confidence:.2f}")
print(f"Status: {signal.epistemic.status}")
print(f"TW Trigger: {signal.tw_trigger}")

assert signal.archetype_probs.sum() > 0.99
assert signal.epistemic.status in ["OK", "INCONCLUSIVO"]

print("✅ End-to-End Test Passed")
```

**Run**:
```bash
python test_e2e.py
```

**Checklist**:
- [ ] Text → Embedding works
- [ ] Embedding → Δ144 works
- [ ] Δ144 → Kindra works
- [ ] Kindra → TW works
- [ ] TW → τ works
- [ ] Final signal valid

---

### 3.2 API Integration Test

**Objective**: Validate API endpoints

**Commands**:
```bash
# Run API tests
pytest tests/api/ -v

# Expected: All API tests pass
```

**Manual Test**:
```bash
# Start API server (if not running)
# uvicorn kaldra_api.main:app --reload

# Test endpoint
curl -X POST http://localhost:8000/engine/kaldra/signal \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The market is showing signs of volatility",
    "context_features": {
      "domain": "financial",
      "language": "en"
    }
  }'

# Expected: JSON response with archetype_probs, tw, epistemic fields
```

**Checklist**:
- [ ] API server starts
- [ ] Endpoint responds
- [ ] Response has correct structure
- [ ] No 500 errors

---

## 4. PRODUCTION-LEVEL VALIDATION

### 4.1 Performance Benchmarks

**Objective**: Ensure acceptable performance

**Benchmark Script**:
```python
import time
import numpy as np
from src.core.kaldra_master_engine import KaldraMasterEngineV2

engine = KaldraMasterEngineV2()

# Warm-up
for _ in range(10):
    embedding = np.random.randn(256)
    engine.infer_from_embedding(embedding)

# Benchmark
times = []
for _ in range(100):
    embedding = np.random.randn(256)
    start = time.time()
    signal = engine.infer_from_embedding(embedding)
    times.append(time.time() - start)

avg_time = np.mean(times)
p95_time = np.percentile(times, 95)

print(f"Average inference time: {avg_time*1000:.2f}ms")
print(f"P95 inference time: {p95_time*1000:.2f}ms")

# Targets
assert avg_time < 0.5  # < 500ms average
assert p95_time < 1.0  # < 1s P95

print("✅ Performance Benchmarks Met")
```

**Targets**:
- [ ] Average inference < 500ms
- [ ] P95 inference < 1s
- [ ] Memory usage < 2GB
- [ ] No memory leaks

---

### 4.2 Stress Testing

**Objective**: Validate system under load

**Stress Test**:
```python
import concurrent.futures
import numpy as np
from src.core.kaldra_master_engine import KaldraMasterEngineV2

engine = KaldraMasterEngineV2()

def run_inference(i):
    embedding = np.random.randn(256)
    return engine.infer_from_embedding(embedding)

# Concurrent requests
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(run_inference, i) for i in range(100)]
    results = [f.result() for f in futures]

assert len(results) == 100
assert all(r.archetype_probs.shape == (144,) for r in results)

print("✅ Stress Test Passed")
```

**Checklist**:
- [ ] Handles 10 concurrent requests
- [ ] No crashes under load
- [ ] All results valid
- [ ] Response times acceptable

---

## 5. VALIDATION AUTOMATION

### 5.1 Complete Test Suite

**Run All Tests**:
```bash
cd /Users/niki/Desktop/kaldra_core

# Run all tests
pytest tests/ -v --cov=src --cov-report=html

# Expected: 57/57 tests pass (v2.1)
# Target: 90%+ coverage (v2.2)
```

**Coverage Report**:
```bash
# View coverage
open htmlcov/index.html
```

---

### 5.2 Validation Checklist Script

**Create**: `scripts/validate_kaldra.py`

```python
#!/usr/bin/env python3
"""
KALDRA Core Validation Script
Runs all validation checks and reports status
"""

import sys
import subprocess

def run_check(name, command):
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"{'='*60}")
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode == 0:
        print(f"✅ {name} PASSED")
        return True
    else:
        print(f"❌ {name} FAILED")
        print(result.stderr.decode())
        return False

checks = [
    ("Δ144 Engine Tests", "pytest tests/core/test_delta144.py -v"),
    ("Kindra Loader Tests", "pytest tests/kindras/test_loaders.py -v"),
    ("Kindra Scorer/Bridge Tests", "pytest tests/kindras/test_scorers_bridges.py -v"),
    ("TW369 Tests", "pytest tests/core/test_tw369.py -v"),
    ("Epistemic Limiter Tests", "pytest tests/test_epistemic_limiter.py -v"),
    ("Master Engine Tests", "pytest tests/test_master_engine_v2.py -v"),
    ("Pipeline Tests", "pytest tests/core/test_pipeline.py -v"),
    ("API Tests", "pytest tests/api/ -v"),
]

results = []
for name, command in checks:
    results.append(run_check(name, command))

print(f"\n{'='*60}")
print("VALIDATION SUMMARY")
print(f"{'='*60}")
print(f"Passed: {sum(results)}/{len(results)}")
print(f"Failed: {len(results) - sum(results)}/{len(results)}")

if all(results):
    print("\n✅ ALL VALIDATIONS PASSED")
    sys.exit(0)
else:
    print("\n❌ SOME VALIDATIONS FAILED")
    sys.exit(1)
```

**Run**:
```bash
chmod +x scripts/validate_kaldra.py
python scripts/validate_kaldra.py
```

---

## 6. TROUBLESHOOTING

### 6.1 Common Issues

**Issue**: Tests fail with FileNotFoundError

**Solution**:
```bash
# Verify working directory
cd /Users/niki/Desktop/kaldra_core

# Check schema files exist
ls -la schema/archetypes/
ls -la schema/kindras/
```

---

**Issue**: Import errors

**Solution**:
```bash
# Add src to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/Users/niki/Desktop/kaldra_core/src"

# Or install in development mode
pip install -e .
```

---

**Issue**: Δ144 distribution doesn't sum to 1.0

**Solution**:
- Check if softmax is applied
- Verify no NaN values
- Check for numerical overflow

---

**Issue**: Kindra bridges have no effect

**Solution**:
- Verify mapping files are populated
- Check that boost/suppress lists are not empty
- Validate kindra_scores are non-zero

---

## 7. VALIDATION SCHEDULE

### Pre-Commit
- [ ] Run unit tests for modified modules
- [ ] Check code formatting
- [ ] Verify no new warnings

### Pre-PR
- [ ] Run full test suite
- [ ] Check test coverage
- [ ] Run validation script

### Pre-Release
- [ ] Run all validation levels
- [ ] Performance benchmarks
- [ ] Stress testing
- [ ] API integration tests
- [ ] Documentation review

---

## CONCLUSION

This validation guide ensures KALDRA Core maintains high quality and reliability. Follow these procedures:

1. **During Development**: Component-level validation
2. **Before Commits**: Integration-level validation
3. **Before Releases**: End-to-end + production validation

**Target Metrics**:
- ✅ 100% test pass rate
- ✅ 90%+ code coverage
- ✅ < 500ms average inference
- ✅ No memory leaks
- ✅ All documentation current

**Next Steps**:
1. Run validation script
2. Address any failures
3. Document any new issues
4. Update this guide as needed
