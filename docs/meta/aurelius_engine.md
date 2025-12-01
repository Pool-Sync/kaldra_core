# AureliusEngine v3.1 — Stoic Analysis with Semantic Intelligence

**Version:** 3.1  
**Status:** INTEGRATED  
**Module:** `src/meta/aurelius.py`  
**Tests:** `tests/meta/test_aurelius_engine.py`

---

## Overview

The **AureliusEngine** analyzes text through a 12-dimensional Stoic philosophical lens, mapping to the 4 Cardinal Virtues and providing insights into control dichotomy, mortality awareness, and fate acceptance.

### Purpose

- **Stoic Analysis**: Detect Stoic themes in text (control dichotomy, virtues, serenity, etc.)
- **Virtue Mapping**: Calculate 4 Cardinal Virtues (Wisdom, Courage, Justice, Temperance)
- **Semantic Intelligence**: Integrate Kindra 3×48 (144 vectors) for cultural/semiotic depth
- **Temporal Awareness**: Incorporate TW369 drift and regime for dynamic adjustments
- **Meta-Level Routing**: Provide high-level signals for MetaStage orchestration

### 12 Stoic Axes

1. **perception_clarity** - Clear, undistorted perception of reality
2. **assent_to_reality** - Acceptance of facts as they are
3. **right_action** - Focus on duty, responsibility, virtue
4. **discipline_of_will** - Consistency, commitment, self-control
5. **emotional_regulation** - Low reactivity, measured response
6. **fate_acceptance** - Acceptance of what cannot be controlled
7. **control_dichotomy** - Distinction between controllable/uncontrollable
8. **premeditatio_malorum** - Anticipation of difficulties (negative visualization)
9. **desire_restraint** - Moderation, absence of excess
10. **character_integrity** - Concern with honor, values, coherence
11. **self_mastery** - Internal dominion, not moved by externals
12. **serenity** - Calm tone, absence of catastrophizing

### 4 Cardinal Virtues

- **Wisdom (Sophia)**: Clear perception + reality acceptance + control awareness
- **Courage (Andreia)**: Right action + discipline + preparation for difficulties
- **Justice (Dikaiosyne)**: Right action + integrity + collective responsibility
- **Temperance (Sophrosyne)**: Restraint + emotional regulation + serenity

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

---

## Output Schema

### AureliusSignal

```python
@dataclass
class AureliusSignal(MetaSignal):
    """Output signal from AureliusEngine analysis."""
    # Stoic-Specific Metrics
    dichotomy_of_control: Dict[str, float]  # {"controllable": x, "not_controllable": y}
    virtue_scores: Dict[str, float]         # {"wisdom": x, "courage": y, "justice": z, "temperance": w}
    memento_mori: float                     # [0, 1] - Urgency/mortality awareness
    amor_fati: float                        # [0, 1] - Active acceptance of fate
    
    # Complete Analysis
    scores: Dict[str, float]                # All 12 axis scores + 4 virtues
    dominant_axes: List[Tuple[str, float]]  # Top 3 axes
    severity: float                         # [0, 1] - Stoic alignment strength
    notes: List[str]                        # Interpretive notes
    
    # MetaSignal Base Fields
    name: str = "aurelius"                  # Engine identifier
    score: float                            # Stoic alignment [0, 1]
    label: str                              # Stoic posture classification
    details: Dict[str, Any]                 # Additional metadata
```

**Field Descriptions:**

- **dichotomy_of_control**: Focus on controllable vs uncontrollable factors
  - `controllable`: Degree of focus on internal/controllable factors
  - `not_controllable`: Degree of focus on external/uncontrollable factors
- **virtue_scores**: 4 Cardinal Virtues, each [0, 1]
  - `wisdom`: Perception clarity + reality acceptance + control awareness
  - `courage`: Right action + discipline + preparation
  - `justice`: Right action + integrity + collective responsibility
  - `temperance`: Restraint + emotional regulation + serenity
- **memento_mori**: Awareness of mortality/urgency (from premeditatio_malorum + existential depth)
- **amor_fati**: Active acceptance of fate (from fate_acceptance + assent_to_reality + serenity)
- **scores**: All 12 dimensional scores + 4 virtues + memento_mori + amor_fati
- **dominant_axes**: Top 3 most prominent axes with scores
- **severity**: Stoic alignment strength (higher = more Stoic)
- **notes**: Human-readable interpretive notes in English
- **label**: Stoic posture classification ("exemplary_stoic" | "stoic" | "mixed" | "non_stoic")

---

## Integration Points

### MetaStage Integration

The AureliusEngine is called by the MetaStage during the unified pipeline:

```python
from src.meta.aurelius import AureliusEngine, MetaInput

# In MetaStage.execute()
aurelius_engine = AureliusEngine()

meta_input = MetaInput(
    text=context.input_ctx.text,
    kindra=context.kindra_ctx,
    tw_state=context.drift_ctx.tw_state,
    archetype_scores=context.archetype_ctx.delta12.to_dict()
)

aurelius_signal = aurelius_engine.analyze(meta_input)

# Store in context
context.meta_ctx.aurelius = aurelius_signal
```

### Kindra 3×48 Integration

Kindra provides 144 semantic vectors across 3 layers:

**Layer 1 (Cultural/Macro)** - 48 vectors
- Control, agency, autonomy, self-determination
- External forces, fate, destiny, circumstances
- Duty, responsibility, obligation, collective action

**Layer 2 (Semiotic/Media)** - 48 vectors
- Emotional intensity, reactivity, passion, urgency
- Calm, measured, balanced, equanimity

**Layer 3 (Structural/Systemic)** - 48 vectors
- Mortality, meaning, purpose, transcendence, existential themes

The engine computes a **Kindra Signature** with 4 key metrics:

```python
{
    "control_focus": 0.5,              # Focus on controllable vs external (Layers 1+2)
    "emotional_volatility": -0.3,      # Emotional intensity vs serenity (Layer 2)
    "collective_responsibility": 0.7,  # Duty/action focus (Layer 1)
    "existential_depth": 0.6           # Symbolic/existential density (Layer 3)
}
```

These metrics adjust the Stoic analysis:
- `control_focus` → adjusts `dichotomy_of_control`
- `emotional_volatility` → reduces `temperance` (if high)
- `collective_responsibility` → boosts `justice` virtue
- `existential_depth` → boosts `memento_mori`

### TW369 Drift Awareness

TW369 provides temporal drift and regime information:

```python
tw_state = TWState(metadata={
    "drift_metric": 0.8,    # [0, 1] - Temporal instability
    "regime": "CRITICAL"    # "STABLE" | "TRANSITION" | "CRITICAL"
})
```

**Drift Adjustments:**
- **High drift (>0.7)**: Boosts `memento_mori` (urgency), `courage`, `temperance`
- **Low drift (<0.3)**: Stable environment

**Regime Adjustments:**
- **CRITICAL**: Boosts `memento_mori`, `courage` (crisis requires action)
- **STABLE**: Slight boost to all virtues (balanced state)
- **TRANSITION**: Boosts `amor_fati` (acceptance of change)

---

## Examples

### Example 1: Basic Stoic Analysis (No Context)

**Input:**
```python
from src.meta.aurelius import AureliusEngine, MetaInput

engine = AureliusEngine()
meta_input = MetaInput(
    text="I focus on what I can control and accept what I cannot. "
         "I remain calm and act with duty and virtue."
)
signal = engine.analyze(meta_input)
```

**Output:**
```json
{
  "name": "aurelius",
  "score": 0.42,
  "label": "stoic",
  "dichotomy_of_control": {
    "controllable": 0.65,
    "not_controllable": 0.35
  },
  "virtue_scores": {
    "wisdom": 0.55,
    "courage": 0.38,
    "justice": 0.35,
    "temperance": 0.40
  },
  "memento_mori": 0.15,
  "amor_fati": 0.48,
  "severity": 0.42,
  "notes": [
    "Stoic posture: stoic",
    "Dominant axis: control dichotomy (0.65)",
    "Strongest virtue: wisdom (0.55)",
    "Strong focus on controllable factors"
  ]
}
```

### Example 2: With Kindra Context

**Input:**
```python
from src.unification.states.unified_state import KindraContext

kindra = KindraContext(
    layer1={
        "duty": 0.9,
        "responsibility": 0.85,
        "collective_action": 0.8
    },
    layer2={
        "calm": 0.7,
        "measured": 0.6
    },
    layer3={
        "existential": 0.75
    }
)

meta_input = MetaInput(
    text="I focus on my duty and responsibility to others.",
    kindra=kindra
)
signal = engine.analyze(meta_input)
```

**Output:**
```json
{
  "virtue_scores": {
    "wisdom": 0.25,
    "courage": 0.40,
    "justice": 0.78,
    "temperance": 0.35
  },
  "memento_mori": 0.45,
  "details": {
    "kindra_signature": {
      "control_focus": 0.0,
      "emotional_volatility": -0.65,
      "collective_responsibility": 0.85,
      "existential_depth": 0.75
    },
    "tw369_applied": false
  }
}
```

**Note:** Kindra boosted `justice` from ~0.4 to 0.78 due to high collective_responsibility, and `memento_mori` from ~0.0 to 0.45 due to existential_depth.

### Example 3: Crisis Scenario (High Drift + CRITICAL Regime)

**Input:**
```python
from src.tw369.tw369_integration import TWState

tw_state = TWState(metadata={
    "drift_metric": 0.9,
    "regime": "CRITICAL"
})

meta_input = MetaInput(
    text="We must prepare for the worst and act with courage.",
    tw_state=tw_state
)
signal = engine.analyze(meta_input)
```

**Output:**
```json
{
  "virtue_scores": {
    "wisdom": 0.15,
    "courage": 0.58,
    "justice": 0.20,
    "temperance": 0.25
  },
  "memento_mori": 0.75,
  "amor_fati": 0.10,
  "details": {
    "tw369_applied": true
  },
  "notes": [
    "Stoic posture: mixed",
    "Strongest virtue: courage (0.58)",
    "Active negative visualization practice detected"
  ]
}
```

**Note:** High drift + CRITICAL regime boosted `memento_mori` significantly and increased `courage`.

### Example 4: Amor Fati (Acceptance of Fate)

**Input:**
```python
meta_input = MetaInput(
    text="I accept my fate with serenity. What is, is perfect. "
         "I embrace reality as it is and remain at peace."
)
signal = engine.analyze(meta_input)
```

**Output:**
```json
{
  "dichotomy_of_control": {
    "controllable": 0.30,
    "not_controllable": 0.70
  },
  "virtue_scores": {
    "wisdom": 0.48,
    "courage": 0.15,
    "justice": 0.10,
    "temperance": 0.65
  },
  "memento_mori": 0.05,
  "amor_fati": 0.72,
  "notes": [
    "Stoic posture: stoic",
    "Strongest virtue: temperance (0.65)",
    "Strong fate acceptance: Amor fati alignment"
  ]
}
```

---

## Known Limitations

### Heuristic-Based Approach (v3.1)

- **Not Learned**: v3.1 uses keyword matching and heuristic rules, not machine learning
- **Keyword Dependency**: Relies on predefined keyword lists for each axis
- **Cultural Bias**: Keywords are English-centric and may not capture non-Western Stoic themes
- **Context Sensitivity**: Limited understanding of irony, sarcasm, or complex rhetorical structures

### Kindra Integration

- **Quality Dependent**: Stoic analysis quality depends on Kindra scoring accuracy
- **Fuzzy Matching**: Vector extraction uses substring matching which may miss nuanced vectors
- **Fixed Weights**: Kindra influence uses fixed weights (not adaptive)

### Temporal Limitations

- **Snapshot Only**: v3.1 analyzes single texts, not temporal sequences
- **No Story Context**: Stoic consistency cannot be measured without StoryContext
- **Approximate Patterns**: Patterns are inferred from keywords, not actual temporal data

### Virtue Calculation

- **Composite Metric**: Virtues are weighted combinations, not direct measurements
- **Threshold Sensitivity**: Classification depends on fixed thresholds that may need calibration
- **Cultural Variance**: Virtues may manifest differently across cultures

---

## Future Implementations

### v3.2 — Temporal Mind Integration

- **StoryContext Integration**: Measure Stoic consistency across narrative timelines
- **Temporal Patterns**: Detect virtue evolution over multiple story events
- **Drift Correlation**: Correlate Stoic posture with TW369 drift evolution

### v3.3 — Domain-Specific Calibration

- **Alpha (Financial)**: Calibrate for CFO/CEO Stoic posture under market stress
- **Geo (Geopolitical)**: Calibrate for state leadership virtue in crisis
- **Product (Brand)**: Calibrate for brand consistency and temperance
- **Safeguard**: Calibrate for emotional regulation in toxic discourse

### v3.4 — Explainability

- **Axis Explanations**: Provide detailed rationale for each axis score
- **Keyword Highlighting**: Show which keywords triggered each axis
- **Kindra Attribution**: Explain how Kindra vectors influenced final scores

### v3.5 — Learned Models

- **Embedding-Based**: Train models to map embeddings → AureliusSignal directly
- **Fine-Tuned LLMs**: Use LLMs fine-tuned on Stoic philosophy corpus
- **Statistical Validation**: Validate virtue scores against large-scale corpora

---

## Enhancements (Short/Medium Term)

### Short Term (v3.1.x)

- **Keyword Expansion**: Add more nuanced keywords for each axis
- **Weight Tuning**: Calibrate Kindra influence weights based on real-world usage
- **Notes Templates**: Improve interpretive notes for dashboard readability
- **Polarity Integration**: Use polarity scores to refine virtue calculation

### Medium Term (v3.2–v3.3)

- **Stoic Consistency Score**: Track virtue consistency over time via StoryContext
- **Archetype-Virtue Mapping**: Deeper integration between Δ144 archetypes and virtues
- **Multi-Language Support**: Extend keyword lists to non-English languages
- **Confidence Scores**: Add per-axis confidence scores

---

## Research Track (Long Term)

### Statistical Modeling

- **Corpus Analysis**: Analyze large corpora (political, corporate, cultural) for Stoic patterns
- **Virtue Distribution**: Study virtue distribution across domains
- **Control Dichotomy**: Model control focus statistically from real-world discourse

### Temporal Modeling

- **Stoic Drift Index**: Measure how entities drift from Stoic posture over time
- **Virtue Evolution**: Track virtue changes over long-term narratives
- **Regime-Virtue Correlation**: Study correlations between TW369 regimes and virtues

### Philosophical Validation

- **Expert Annotation**: Validate engine output against Stoic philosophy scholars
- **Philosophical Corpus**: Test against Marcus Aurelius' Meditations and Stoic texts
- **Cross-Cultural Study**: Validate across different cultural contexts

---

## Testing

### Test Suite

**Location:** `tests/meta/test_aurelius_engine.py`

**Coverage:**
- ✅ Basic functionality (3 tests)
- ✅ Kindra 3×48 integration (3 tests)
- ✅ TW369 drift awareness (4 tests)
- ✅ Virtue scores calculation (2 tests)
- ✅ Dichotomy of control (2 tests)
- ✅ Memento mori and amor fati (2 tests)
- ✅ Stoic posture classification (1 test)
- ✅ Backward compatibility (2 tests)
- ✅ Notes generation (3 tests)
- ✅ Full integration (1 test)
- ✅ Anti-patterns (1 test)

**Run Tests:**
```bash
cd /Users/niki/Desktop/kaldra_core
python3 -m pytest tests/meta/test_aurelius_engine.py -v
```

**Expected:** All 24 tests pass

---

## API Usage

### Class-Based API (v3.1)

```python
from src.meta.aurelius import AureliusEngine, MetaInput, AureliusSignal

# Initialize engine
engine = AureliusEngine()

# Create input
meta_input = MetaInput(
    text="Your text here",
    kindra=kindra_context,  # Optional
    tw_state=tw_state,      # Optional
    archetype_scores={}     # Optional
)

# Analyze
signal: AureliusSignal = engine.analyze(meta_input)

# Access results
print(f"Stoic Posture: {signal.label}")
print(f"Virtue Scores: {signal.virtue_scores}")
print(f"Dichotomy of Control: {signal.dichotomy_of_control}")
print(f"Memento Mori: {signal.memento_mori}")
print(f"Amor Fati: {signal.amor_fati}")
```

### Legacy API (v2.9 Backward Compatibility)

```python
from src.meta.aurelius import analyze_meta

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

- ✅ Refactored to class-based `AureliusEngine`
- ✅ Added `MetaInput` and `AureliusSignal` dataclasses
- ✅ Integrated Kindra 3×48 (144 vectors) via `_compute_kindra_signature()`
- ✅ Integrated TW369 drift/regime via `_apply_tw369_adjustments()`
- ✅ Added 4 Cardinal Virtues calculation
- ✅ Added dichotomy of control calculation
- ✅ Added memento_mori (mortality awareness) calculation
- ✅ Added amor_fati (fate acceptance) calculation
- ✅ Added Stoic posture classification
- ✅ Maintained backward compatibility with v2.9 via `analyze_meta()` wrapper
- ✅ Created comprehensive test suite (24 tests, 100% pass rate)

### v2.9 (Legacy)

- Function-based `analyze_meta()` API
- 12-dimensional keyword-based scoring
- Optional Delta12 and TWState adjustments
- Returns `MetaEngineResult`

---

## References

### Stoic Philosophy

- Marcus Aurelius. *Meditations*
- Epictetus. *Enchiridion* (Handbook)
- Seneca. *Letters from a Stoic*
- Musonius Rufus. *Lectures and Fragments*

### KALDRA Documentation

- [KALDRA v3.1 Exoskeleton](file:///Users/niki/Desktop/kaldra_core/docs/roadmaps/KALDRA_V3_1_EXOSKELETON.md)
- [Kindra Δ144 Alignment Summary](file:///Users/niki/Desktop/kaldra_core/docs/core/KINDRA_DELTA144_ALIGNMENT_SUMMARY.md)
- [Unification Pipeline Flow](file:///Users/niki/Desktop/kaldra_core/docs/core/UNIFICATION_PIPELINE_FLOW.md)

---

**Last Updated:** 2025-12-01  
**Author:** KALDRA Development Team  
**Version:** 3.1.0
