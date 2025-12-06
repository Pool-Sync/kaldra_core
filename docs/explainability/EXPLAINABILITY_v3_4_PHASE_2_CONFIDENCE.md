# Explainability v3.4 Phase 2 - Confidence & Decision Tracing

**Status:** ✅ IMPLEMENTED  
**Version:** KALDRA v3.4 Phase 2  
**Date:** December 2025  
**Component:** Explainability Layer

---

## Overview

Phase 2 extends the Transparency Layer by adding **confidence scoring** and **decision tracing** to explanations. This enables KAL DRA to articulate not only *what* and *why*, but also *how confident* it is and *how* it arrived at conclusions.

### Relation to Phase 1

Phase 1 (NL Explanations) provided natural language generation with LLM support and fallback.  
Phase 2 adds **meta-information** about explanation quality and reasoning paths.

### Key Features

- **Overall Confidence Score**: Single [0,1] score indicating explanation reliability
- **Per-Component Confidence**: Breakdown by module (Delta144, Story, TW369, Multi-Stream, etc.)
- **Decision Trace**: Sequential steps showing reasoning path
- **Backward Compatible**: Phase 1 behavior preserved when confidence disabled

---

## Architecture

### Data Flow

```
UnifiedContext
    ↓
ExplanationGenerator
    ├─ Extract Facts
    ├─ Generate Explanation (LLM/Template/Barebones)
    └─ Compute Confidence (Phase 2)
        ↓
    ConfidenceEngine
        ├─ Component Analysis
        ├─ Trace Builder
        └─ Overall Score
        ↓
    Explanation (extended)
        ├─ summary
        ├─ details
        ├─ raw_facts
        ├─ confidence ← NEW
        └─ trace ← NEW
```

---

## Confidence Model

### Heuristic Scoring

Phase 2 uses **heuristic-based** confidence (not probabilistic/Bayesian):

**Base Score:** 0.5

**Adjustments:**
- **+0.08** per component present (Delta144, polarities, story, drift, multistream)
- **-0.2** if context degraded
- **Averaged** with component scores

**Components Detected:**
- `delta144`: Delta144 state present
- `polarities`: Polarity scores available
- `story`: StoryContext with arc
- `tw369`: DriftContext with regime
- `multistream`: Multi-stream divergence analysis

### Component Confidence

Each component gets a score:

| Component | Score Range | Criteria |
|-----------|-------------|----------|
| delta144 | 0.8 | State ID clearly identified |
| polarities | 0.6-0.9 | Based on number of polarities |
| story | 0.5-0.9 | Based on coherence score |
| tw369 | 0.75 | Regime identified (not UNKNOWN) |
| multistream | 0.6-0.85 | Based on number of comparisons |

---

## Decision Trace

### Trace Steps

Each `DecisionStep` represents one reasoning action:

```python
@dataclass
class DecisionStep:
    step: str             # e.g., "delta144_evaluation"
    description: str       # What happened
    weight: float          # Contribution [0,1]
    source: str            # "engine", "heuristic", "llm"
    metadata: Dict         # Additional context
```

### Example Trace

```
[
  {
    "step": "delta144_evaluation",
    "description": "Identified archetypal state: threshold",
    "weight": 0.2,
    "source": "engine"
  },
  {
    "step": "polarity_balance",
    "description": "Dominant polarity: order (0.70)",
    "weight": 0.15,
    "source": "engine"
  },
  {
    "step": "story_arc",
    "description": "Narrative arc stage: crossing_threshold",
    "weight": 0.2,
    "source": "engine"
  },
  {
    "step": "explanation_mode",
    "description": "Explanation generated via template mode",
    "weight": 0.15,
    "source": "explainability"
  }
]
```

---

## Usage Examples

### Basic Usage

```python
from src.explainability.explanation_generator import ExplanationGenerator
from src.unification.states.unified_state import UnifiedContext

# Initialize (confidence enabled by default)
generator = ExplanationGenerator()

# Generate explanation
context = UnifiedContext(...)  # From pipeline
explanation = generator.generate(context)

# Access confidence
print(f"Confidence: {explanation.confidence.overall:.2f}")

# Per-component confidence
for comp in explanation.confidence.components:
    print(f"{comp.name}: {comp.score:.2f} - {comp.reason}")

# Decision trace
for step in explanation.trace:
    print(f"{step.step}: {step.description} (weight: {step.weight})")
```

### Disabling Confidence (Phase 1 Behavior)

```python
# Explicitly disable confidence
generator = ExplanationGenerator(confidence_engine=None)

explanation = generator.generate(context)

# No confidence or trace
assert explanation.confidence is None
assert len(explanation.trace) == 0
```

### Accessing Confidence from Details

```python
explanation = generator.generate(context)

# Confidence also added to details for convenience
if "confidence" in explanation.details:
    print(f"Overall: {explanation.details['confidence']['overall']}")
    for comp in explanation.details['confidence']['components']:
        print(f"{comp['name']}: {comp['score']}")
```

---

## Testing

### Test Coverage

**12 comprehensive tests** covering:

1. ✅ Basic overall score validation
2. ✅ Delta144 component detection
3. ✅ Story component detection
4. ✅ Degraded context penalty
5. ✅ Trace step generation
6. ✅ Generator populates confidence
7. ✅ Phase 1 backward compatibility
8. ✅ Graceful handling of missing fields
9. ✅ Rich vs lean context comparison
10. ✅ LLM mode trace step
11. ✅ Template mode trace step
12. ✅ Barebones mode trace step

### Running Tests

```bash
# Phase 2 tests
PYTHONPATH=/Users/niki/Desktop/kaldra_core pytest tests/explainability/test_explanation_confidence.py -v

# Phase 1 tests (backward compat)
PYTHONPATH=/Users/niki/Desktop/kaldra_core pytest tests/explainability/test_explanation_generator.py -v
```

---

## API Reference

### New Data Structures

```python
@dataclass
class ComponentConfidence:
    name: str
    score: float
    reason: str
    metadata: Dict[str, Any]

@dataclass
class DecisionStep:
    step: str
    description: str
    weight: float
    source: str
    metadata: Dict[str, Any]

@dataclass
class ExplanationConfidence:
    overall: float
    components: List[ComponentConfidence]
    trace: List[DecisionStep]
    metadata: Dict[str, Any]
```

### Extended Explanation Class

```python
class Explanation:
    summary: str
    details: Dict[str, Any]
    raw_facts: Dict[str, Any]
    confidence: Optional[ExplanationConfidence]  # NEW
    trace: List[DecisionStep]                     # NEW
```

---

## Limitations & Future Work

### Current Limitations

- **Not in API**: Confidence not exposed via SignalAdapter yet (Phase 3)
- **Heuristic Scores**: Not statistical/probabilistic
- **No Fine-tuning**: Weights are hardcoded
- **Single Language**: English only

### Phase 3: API Exposure (Planned)

- Expose confidence via SignalAdapter
- Add to REST API responses
- Include in frontend display

### Future Enhancements

- **Bayesian Confidence**: Statistical scoring
- **Learned Weights**: ML-based component weights
- **Uncertainty Quantification**: Confidence intervals
- **Alternative Hypotheses**: Multiple explanations with confidence

---

## Related Documentation

- [Explainability Phase 1 (NL Explanations)](file:///Users/niki/Desktop/kaldra_core/docs/explainability/EXPLAINABILITY_v3_4_PHASE_1.md)
- [Multi-Stream Integration (v3.3)](file:///Users/niki/Desktop/kaldra_core/docs/multistream/MULTI_STREAM_INTEGRATION_v3_3_PHASE_3.md)
- [Story Engine (v3.2)](file:///Users/niki/Desktop/kaldra_core/docs/story/STORY_ENGINE_PRIMITIVES_v3_2.md)

---

## Summary

Explainability Phase 2 adds transparency to transparency:

✅ **Confidence Scoring**: Overall + per-component  
✅ **Decision Tracing**: Sequential reasoning steps  
✅ **Backward Compatible**: Phase 1 preserved  
✅ **Well-Tested**: 12/12 tests passing  
✅ **Production Ready**: Graceful error handling

KALDRA can now explain not just *why*, but *how confident* it is in those explanations.
