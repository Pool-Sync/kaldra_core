# NietzscheEngine v3.1 — Nietzschean Analysis with Semantic Intelligence

**Version:** 3.1  
**Status:** INTEGRATED  
**Module:** `src/meta/nietzsche.py`  
**Tests:** `tests/meta/test_nietzsche_engine.py`

---

## Overview

The **NietzscheEngine** analyzes text through a 12-dimensional Nietzschean philosophical lens, providing deep insights into power dynamics, morality types, nihilistic tendencies, and transcendence potential.

### Purpose

- **Philosophical Analysis**: Detect Nietzschean themes in text (will to power, ressentiment, eternal return, etc.)
- **Morality Classification**: Classify discourse as master/slave/mixed morality
- **Semantic Intelligence**: Integrate Kindra 3×48 (144 vectors) for cultural/semiotic depth
- **Temporal Awareness**: Incorporate TW369 drift and regime for dynamic adjustments
- **Meta-Level Routing**: Provide high-level signals for MetaStage orchestration

### 12 Nietzschean Axes

1. **will_to_power** - Drive for dominance, creation, self-overcoming
2. **resentment** - Envy, victimization, reactive negativity (ressentiment)
3. **life_affirmation** - Positive embrace of existence
4. **life_negation** - Rejection, exhaustion, world-weariness
5. **free_spirit** - Independence from tradition and convention
6. **active_nihilism** - Creative destruction, burning the old
7. **passive_nihilism** - Despair, apathy, giving up
8. **eternal_return_acceptance** - Radical acceptance of fate/cyclical patterns
9. **transvaluation** - Inversion of traditional values
10. **dionysian_force** - Chaos, excess, primal energy
11. **apollonian_order** - Form, harmony, rational structure
12. **amor_fati** - Loving acceptance of what is

---

## Input Schema

### MetaInput

```python
@dataclass
class MetaInput:
    """Standard input for meta-engine analysis (v3.1)."""
    text: str                                    # Required: Input text
    delta144_state: Optional[str] = None         # Current Δ144 state ID
    archetype_scores: Dict[str, float] = {}      # Archetype distribution
    kindra: Optional[KindraContext] = None       # Kindra 3×48 context
    tw_state: Optional[TWState] = None           # TW369 drift/regime
    bias_score: Optional[float] = None           # Bias detection score
    polarity_scores: Optional[Dict[str, float]] = None
    modifiers: Optional[Dict[str, float]] = None
```

**Required Fields:**
- `text`: The input text to analyze

**Optional Fields:**
- `kindra`: KindraContext with 3 layers × 48 vectors = 144 total semantic scores
- `tw_state`: TWState with drift_metric and regime for temporal awareness
- `archetype_scores`: Archetype distribution for archetypal adjustments
- `delta144_state`: Current Δ144 state identifier
- `bias_score`: Bias detection score
- `polarity_scores`: Polarity scores for additional context
- `modifiers`: Custom adjustment modifiers

---

## Output Schema

### NietzscheSignal

```python
@dataclass
class NietzscheSignal(MetaSignal):
    """Output signal from NietzscheEngine analysis."""
    # Primary Nietzschean Metrics
    will_to_power: float          # [0, 1] - Power/dominance drive
    morality_type: str            # "master" | "slave" | "mixed"
    eternal_return: float         # [0, 1] - Cyclical pattern strength
    transcendence: float          # [0, 1] - Übermensch markers
    
    # Complete Analysis
    scores: Dict[str, float]      # All 12 axis scores
    dominant_axes: List[Tuple[str, float]]  # Top 3 axes
    severity: float               # [0, 1] - Overall intensity
    notes: List[str]              # Interpretive notes
    
    # MetaSignal Base Fields
    name: str = "nietzsche"       # Engine identifier
    score: float                  # Confidence/strength [0, 1]
    label: str                    # Primary classification
    details: Dict[str, Any]       # Additional metadata
```

**Field Descriptions:**

- **will_to_power**: Strength of power-seeking, dominance, self-overcoming themes
- **morality_type**: Classification of moral framework
  - `"master"`: High will to power, low resentment, creative/affirmative
  - `"slave"`: Low will to power, high resentment, reactive/negative
  - `"mixed"`: Contradictory or intermediate signals
- **eternal_return**: Strength of cyclical/repetitive patterns, fate acceptance
- **transcendence**: Markers of Übermensch (overman) potential - high will, low resentment, free spirit
- **scores**: All 12 dimensional scores as dict
- **dominant_axes**: Top 3 most prominent axes with scores
- **severity**: Overall intensity (max of positive or negative axes)
- **notes**: Human-readable interpretive notes in English

---

## Integration Points

### MetaStage Integration

The NietzscheEngine is called by the MetaStage during the unified pipeline:

```python
from src.meta.nietzsche import NietzscheEngine, MetaInput

# In MetaStage.execute()
nietzsche_engine = NietzscheEngine()

meta_input = MetaInput(
    text=context.input_ctx.text,
    kindra=context.kindra_ctx,
    tw_state=context.drift_ctx.tw_state,
    archetype_scores=context.archetype_ctx.delta12.to_dict()
)

nietzsche_signal = nietzsche_engine.analyze(meta_input)

# Store in context
context.meta_ctx.nietzsche = nietzsche_signal
```

### Kindra 3×48 Integration

Kindra provides 144 semantic vectors across 3 layers:

**Layer 1 (Cultural/Macro)** - 48 vectors
- Power dynamics, dominance, hierarchy, authority
- Victimhood, grievance, resentment, blame

**Layer 2 (Semiotic/Media)** - 48 vectors
- Conflict, tension, opposition, dialectic
- Victim narratives, injustice framing

**Layer 3 (Structural/Systemic)** - 48 vectors
- Archetypal patterns (hero, sage, etc.)
- Mythic themes, universal patterns, transcendence

The engine computes a **Kindra Signature** with 4 key metrics:

```python
{
    "power_climate": 0.7,        # Cultural power dynamics (Layer 1)
    "ressentiment_index": 0.3,   # Victim/blame patterns (Layers 1+2)
    "mythic_intensity": 0.6,     # Archetypal resonance (Layer 3)
    "conflict_tension": 0.5      # Dialectical forces (Layer 2)
}
```

These metrics adjust the 12 Nietzschean axes:
- `power_climate` → boosts `will_to_power`
- `ressentiment_index` → boosts `resentment`
- `mythic_intensity` → boosts `eternal_return`, `amor_fati`, `transcendence`
- `conflict_tension` → boosts `dionysian_force` (if high) or `apollonian_order` (if low)

### TW369 Drift Awareness

TW369 provides temporal drift and regime information:

```python
tw_state = TWState(metadata={
    "drift_metric": 0.8,    # [0, 1] - Temporal instability
    "regime": "CRITICAL"    # "STABLE" | "TRANSITION" | "CRITICAL"
})
```

**Drift Adjustments:**
- **High drift (>0.7)**: Boosts `will_to_power`, `eternal_return`, `dionysian_force`
- **Low drift (<0.3)**: Boosts `apollonian_order`, `amor_fati`

**Regime Adjustments:**
- **CRITICAL**: Boosts `active_nihilism`, `transvaluation`
- **STABLE**: Boosts `life_affirmation`
- **TRANSITION**: Boosts `transvaluation`

---

## Examples

### Example 1: Basic Analysis (No Context)

**Input:**
```python
from src.meta.nietzsche import NietzscheEngine, MetaInput

engine = NietzscheEngine()
meta_input = MetaInput(
    text="We will dominate the market with superior strength and power. "
         "We lead, we conquer, we triumph through excellence."
)
signal = engine.analyze(meta_input)
```

**Output:**
```json
{
  "name": "nietzsche",
  "score": 0.85,
  "label": "master",
  "will_to_power": 0.87,
  "morality_type": "master",
  "eternal_return": 0.12,
  "transcendence": 0.65,
  "scores": {
    "will_to_power": 0.87,
    "resentment": 0.05,
    "life_affirmation": 0.42,
    "life_negation": 0.03,
    "free_spirit": 0.15,
    "active_nihilism": 0.08,
    "passive_nihilism": 0.02,
    "eternal_return_acceptance": 0.12,
    "transvaluation": 0.10,
    "dionysian_force": 0.25,
    "apollonian_order": 0.18,
    "amor_fati": 0.08
  },
  "dominant_axes": [
    ["will_to_power", 0.87],
    ["life_affirmation", 0.42],
    ["dionysian_force", 0.25]
  ],
  "severity": 0.87,
  "notes": [
    "Morality type: master",
    "Dominant axis: will to power (0.87)",
    "Übermensch potential: High will to power and free spirit"
  ]
}
```

### Example 2: With Kindra Context

**Input:**
```python
from src.unification.states.unified_state import KindraContext

kindra = KindraContext(
    layer1={
        "power_dynamics": 0.9,
        "dominance": 0.85,
        "hierarchy": 0.75
    },
    layer2={
        "conflict": 0.6,
        "tension": 0.55
    },
    layer3={
        "archetypal_hero": 0.8,
        "mythic_pattern": 0.7
    }
)

meta_input = MetaInput(
    text="We will overcome all obstacles.",
    kindra=kindra
)
signal = engine.analyze(meta_input)
```

**Output:**
```json
{
  "will_to_power": 0.92,
  "morality_type": "master",
  "transcendence": 0.78,
  "details": {
    "kindra_signature": {
      "power_climate": 0.83,
      "ressentiment_index": 0.0,
      "mythic_intensity": 0.75,
      "conflict_tension": 0.58
    },
    "tw369_applied": false
  }
}
```

**Note:** Kindra boosted `will_to_power` from ~0.6 to 0.92 and `transcendence` from ~0.5 to 0.78.

### Example 3: Slave Morality Detection

**Input:**
```python
meta_input = MetaInput(
    text="It's so unfair. I'm the victim here. They don't deserve what they have. "
         "Why them and not me? I blame them for everything."
)
signal = engine.analyze(meta_input)
```

**Output:**
```json
{
  "will_to_power": 0.08,
  "morality_type": "slave",
  "resentment": 0.82,
  "transcendence": 0.12,
  "notes": [
    "Morality type: slave",
    "Dominant axis: resentment (0.82)"
  ]
}
```

### Example 4: With TW369 Drift

**Input:**
```python
from src.tw369.tw369_integration import TWState

tw_state = TWState(metadata={
    "drift_metric": 0.9,
    "regime": "CRITICAL"
})

meta_input = MetaInput(
    text="We must tear down the old structures and rebuild.",
    tw_state=tw_state
)
signal = engine.analyze(meta_input)
```

**Output:**
```json
{
  "will_to_power": 0.75,
  "active_nihilism": 0.68,
  "transvaluation": 0.55,
  "dionysian_force": 0.62,
  "details": {
    "tw369_applied": true
  },
  "notes": [
    "Active nihilism detected: Creative destruction mode"
  ]
}
```

**Note:** High drift + CRITICAL regime boosted `active_nihilism` and `transvaluation`.

---

## Known Limitations

### Heuristic-Based Approach (v3.1)

- **Not Learned**: v3.1 uses keyword matching and heuristic rules, not machine learning
- **Keyword Dependency**: Relies on predefined keyword lists for each axis
- **Cultural Bias**: Keywords are English-centric and may not capture non-Western Nietzschean themes
- **Context Sensitivity**: Limited understanding of irony, sarcasm, or complex rhetorical structures

### Kindra Integration

- **Quality Dependent**: Nietzschean analysis quality depends on Kindra scoring accuracy
- **Fuzzy Matching**: Vector extraction uses substring matching which may miss nuanced vectors
- **Fixed Weights**: Kindra influence uses fixed weights (not adaptive)

### Temporal Limitations

- **Snapshot Only**: v3.1 analyzes single texts, not temporal sequences
- **No Story Context**: `eternal_return` detection is limited without StoryContext
- **Approximate Patterns**: Cyclical patterns are inferred from keywords, not actual temporal data

### Morality Classification

- **Simplified Model**: Master/slave/mixed is a reduction of Nietzsche's complex genealogy
- **Threshold Sensitivity**: Classification depends on fixed thresholds that may need calibration
- **Cultural Variance**: Morality types may manifest differently across cultures

### Transcendence Calculation

- **Composite Metric**: Transcendence is a weighted combination, not a direct measurement
- **Übermensch Approximation**: True Übermensch requires deeper philosophical analysis
- **Context Required**: Transcendence is better assessed with biographical/historical context

---

## Future Implementations

### v3.2 — Temporal Mind Integration

- **StoryContext Integration**: Analyze `eternal_return` across narrative timelines
- **Temporal Patterns**: Detect cyclical themes over multiple story events
- **Drift Correlation**: Correlate Nietzschean themes with TW369 drift evolution

### v3.3 — Domain-Specific Calibration

- **Alpha (Financial)**: Calibrate for market power dynamics, competitive language
- **Geo (Geopolitical)**: Calibrate for state power, international relations
- **Product (Brand)**: Calibrate for brand identity, consumer empowerment
- **Safeguard**: Calibrate for toxic power dynamics, victimization narratives

### v3.4 — Explainability

- **Axis Explanations**: Provide detailed rationale for each axis score
- **Keyword Highlighting**: Show which keywords triggered each axis
- **Kindra Attribution**: Explain how Kindra vectors influenced final scores

### v3.5 — Learned Models

- **Embedding-Based**: Train models to map embeddings → NietzscheSignal directly
- **Fine-Tuned LLMs**: Use LLMs fine-tuned on Nietzschean philosophy corpus
- **Statistical Validation**: Validate morality types against large-scale corpora

---

## Enhancements (Short/Medium Term)

### Short Term (v3.1.x)

- **Keyword Expansion**: Add more nuanced keywords for each axis
- **Weight Tuning**: Calibrate Kindra influence weights based on real-world usage
- **Notes Templates**: Improve interpretive notes for dashboard readability
- **Polarity Integration**: Use polarity scores to refine morality classification

### Medium Term (v3.2–v3.3)

- **Genealogy Analysis**: Track value transvaluation over time via StoryContext
- **Archetype-Morality Mapping**: Deeper integration between Δ144 archetypes and morality types
- **Multi-Language Support**: Extend keyword lists to non-English languages
- **Confidence Scores**: Add per-axis confidence scores

---

## Research Track (Long Term)

### Statistical Modeling

- **Corpus Analysis**: Analyze large corpora (political, corporate, cultural) for Nietzschean patterns
- **Morality Distribution**: Study master/slave/mixed distribution across domains
- **Power Dynamics**: Model "will to power" statistically from real-world discourse

### Temporal Modeling

- **Eternal Return Detection**: Develop statistical models for cyclical narrative patterns
- **Transvaluation Tracking**: Track value inversions over long-term narratives
- **Regime-Morality Correlation**: Study correlations between TW369 regimes and morality types

### Philosophical Validation

- **Expert Annotation**: Validate engine output against Nietzsche scholars
- **Philosophical Corpus**: Test against Nietzsche's own writings and commentaries
- **Cross-Cultural Study**: Validate across different cultural contexts

---

## Testing

### Test Suite

**Location:** `tests/meta/test_nietzsche_engine.py`

**Coverage:**
- ✅ Basic functionality (25 tests)
- ✅ Kindra 3×48 integration (3 tests)
- ✅ TW369 drift awareness (3 tests)
- ✅ Morality type classification (4 tests)
- ✅ Axis-specific detection (7 tests)
- ✅ Transcendence calculation (2 tests)
- ✅ Backward compatibility (2 tests)
- ✅ Notes generation (3 tests)
- ✅ Full integration (1 test)

**Run Tests:**
```bash
cd /Users/niki/Desktop/kaldra_core
python3 -m pytest tests/meta/test_nietzsche_engine.py -v
```

**Expected:** All 25 tests pass

### Regression Testing

```bash
python3 -m pytest tests/meta/test_nietzsche_engine.py tests/meta/test_aurelius_engine.py tests/meta/test_campbell_engine.py -v
```

**Expected:** All NietzscheEngine, AureliusEngine, and CampbellEngine tests pass

---

## API Usage

### Class-Based API (v3.1)

```python
from src.meta.nietzsche import NietzscheEngine, MetaInput, NietzscheSignal

# Initialize engine
engine = NietzscheEngine()

# Create input
meta_input = MetaInput(
    text="Your text here",
    kindra=kindra_context,  # Optional
    tw_state=tw_state,      # Optional
    archetype_scores={}     # Optional
)

# Analyze
signal: NietzscheSignal = engine.analyze(meta_input)

# Access results
print(f"Morality Type: {signal.morality_type}")
print(f"Will to Power: {signal.will_to_power}")
print(f"Transcendence: {signal.transcendence}")
print(f"Dominant Axes: {signal.dominant_axes}")
```

### Legacy API (v2.9 Backward Compatibility)

```python
from src.meta.nietzsche import analyze_meta

# Legacy function-based API
result = analyze_meta(
    text="Your text here",
    delta12=delta12_vector,  # Optional
    tw_state=tw_state,       # Optional
    bias_score=0.1           # Optional
)

# Returns MetaEngineResult (legacy format)
print(result.scores)
print(result.dominant_axes)
print(result.severity)
print(result.notes)
```

---

## Changelog

### v3.1 (Current)

- ✅ Refactored to class-based `NietzscheEngine`
- ✅ Added `MetaInput` and `NietzscheSignal` dataclasses
- ✅ Integrated Kindra 3×48 (144 vectors) via `_compute_kindra_signature()`
- ✅ Integrated TW369 drift/regime via `_apply_tw369_adjustments()`
- ✅ Added morality type classification (`master`/`slave`/`mixed`)
- ✅ Added transcendence calculation (Übermensch potential)
- ✅ Maintained backward compatibility with v2.9 via `analyze_meta()` wrapper
- ✅ Created comprehensive test suite (25 tests, 100% pass rate)

### v2.9 (Legacy)

- Function-based `analyze_meta()` API
- 12-dimensional keyword-based scoring
- Optional Delta12 and TWState adjustments
- Returns `MetaEngineResult`

---

## References

### Nietzschean Philosophy

- Nietzsche, F. (1886). *Beyond Good and Evil*
- Nietzsche, F. (1887). *On the Genealogy of Morals*
- Nietzsche, F. (1883-1885). *Thus Spoke Zarathustra*
- Nietzsche, F. (1888). *The Antichrist*

### KALDRA Documentation

- [KALDRA v3.1 Exoskeleton](file:///Users/niki/Desktop/kaldra_core/docs/roadmaps/KALDRA_V3_1_EXOSKELETON.md)
- [Kindra Δ144 Alignment Summary](file:///Users/niki/Desktop/kaldra_core/docs/core/KINDRA_DELTA144_ALIGNMENT_SUMMARY.md)
- [Unification Pipeline Flow](file:///Users/niki/Desktop/kaldra_core/docs/core/UNIFICATION_PIPELINE_FLOW.md)

---

**Last Updated:** 2025-12-01  
**Author:** KALDRA Development Team  
**Version:** 3.1.0
