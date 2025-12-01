# Δ12 and Δ144 — Archetypal Layers and Their Relation

**Version**: 2.4 Planning  
**Status**: Specification Document  
**Last Updated**: 2025-11-28

---

## 1. Introduction

The KALDRA engine operates on two complementary archetypal layers:

- **Δ12** (Delta-12): The **base archetypal layer** representing 12 fundamental archetypes
- **Δ144** (Delta-144): The **state crystallization matrix** representing 144 specific archetypal states (12 archetypes × 12 states each)

### Key Distinction

**Δ12 is the foundation; Δ144 is the manifestation.**

- **Δ12** answers: *"Which archetypal energy is dominant?"*
- **Δ144** answers: *"What specific state is this archetype expressing right now?"*

Think of Δ12 as the **archetype family** and Δ144 as the **specific member** within that family, shaped by context, tension, and temporal dynamics.

---

## 2. Formal Definition

### 2.1. Δ12 — Base Archetypal Vector

**Δ12** is a 12-dimensional probability distribution over the fundamental archetypes:

```
Δ12 ∈ ℝ¹² where Σ Δ12[i] = 1.0, Δ12[i] ∈ [0,1]
```

**Components**:
```
Δ12 = [
    A01_INNOCENT,
    A02_ORPHAN,
    A03_WARRIOR,
    A04_CAREGIVER,
    A05_SEEKER,
    A06_LOVER,
    A07_RULER,
    A08_REBEL,
    A09_MAGICIAN,
    A10_SAGE,
    A11_JESTER,
    A12_CREATOR
]
```

**Interpretation**: Each component represents the **relative activation** of that archetype in the current context.

### 2.2. Δ144 — State Crystallization Matrix

**Δ144** is a function mapping from archetypal base + contextual signals to a specific state:

```
Δ144: (archetype_id, plane_scores, profile_scores, modifiers) → state_id
```

Where:
- **archetype_id** ∈ {A01...A12} (from Δ12 dominant)
- **plane_scores** ∈ ℝ³ (TW369 planes: 3, 6, 9)
- **profile_scores** ∈ ℝ³ (EXPANSIVE, CONTRACTIVE, TRANSCENDENT)
- **modifiers** ∈ ℝ⁶² (dynamic emotional/structural vectors)

**Output**: A specific state from the 144-state space, e.g., `A07_RULER_6_05` (Ruler archetype, Plane 6, State 05).

### 2.3. Relationship

```
Δ12 (base energy) → selects archetype family
    ↓
Δ144 (contextual refinement) → selects specific state within family
```

---

## 3. Flow in KALDRA Engine

### 3.1. Signal Pipeline

```
TEXT INPUT
    ↓
[Bias Engine] → toxicity, polarization
    ↓
[Embedding Generator] → semantic vector
    ↓
[Kindra 3×48] → cultural/semiotic scores
    ↓
[TW369 Engine] → plane scores (3/6/9), drift, regime
    ↓
[Δ12 Projection] → base archetype probabilities
    ↓
[Δ144 Inference] → specific archetypal state
    ↓
KALDRA SIGNAL
```

### 3.2. Δ12 Projection from Kindra

**Kindra 3×48** (144 cultural vectors across 3 layers) projects onto **Δ12** through learned or rule-based mappings:

```python
# Conceptual mapping
Δ12[A07_RULER] ∝ f(
    K42_BOUNDARY_TERMS,      # Institutional language
    K38_POWER_DYNAMICS,      # Authority signals
    K15_STRUCTURAL_STABILITY # Order emphasis
)

Δ12[A08_REBEL] ∝ f(
    K19_CREATIVE_RUPTURE,    # Disruption
    K27_ANTI_ESTABLISHMENT,  # Challenge to authority
    K33_CHAOS_SIGNALS        # Disorder embrace
)
```

**Current Implementation**: Rule-based heuristics  
**v2.4+ Vision**: Learned embeddings or statistical correlations

### 3.3. Δ144 Refinement from TW369

Once **Δ12** identifies the dominant archetype (e.g., `A07_RULER`), **TW369** provides the contextual signals to select the specific state:

```python
# TW369 outputs
plane_scores = {
    "3": 0.2,  # Action/Expansion
    "6": 0.6,  # Structure/Contraction ← dominant
    "9": 0.2   # Metanoia/Transcendence
}

# Δ144 uses this to select state
# High Plane 6 → Contractive states favored
# Result: A07_RULER_6_05 (Defensive Leadership)
```

---

## 4. Interaction with TW369 & Painlevé

### 4.1. Δ12 Defines Macro Regimes

**Δ12** establishes the **archetypal regime** that influences TW369 dynamics:

| Archetype Family | TW369 Regime | Typical Plane | Drift Tendency |
|------------------|--------------|---------------|----------------|
| RULER, CAREGIVER | Stability-seeking | Plane 6 (Structure) | Low drift |
| REBEL, CREATOR | Disruption-prone | Plane 3 (Action) | High drift |
| SAGE, MAGICIAN | Synthesis-oriented | Plane 9 (Metanoia) | Oscillating drift |

**Example**: If Δ12 shows high `A07_RULER`, TW369 expects:
- Preference for Plane 6 (structure)
- Lower tolerance for drift
- Painlevé filter tuned for stability detection

### 4.2. Δ144 Defines Micro States on the Surface

**Δ144** provides the **fine-grained position** on the archetypal manifold that TW369 tracks over time:

```
Δ144 at t=0: A07_RULER_6_05 (Defensive Leadership)
    ↓ [drift accumulates]
Δ144 at t=1: A07_RULER_6_06 (Reactive Leadership)
    ↓ [crisis threshold crossed]
Δ144 at t=2: A07_RULER_9_09 (Servant Leadership - transcendence)
```

**TW369's Role**: Compute the **drift trajectory** between these states.

**Painlevé's Role**: Detect **critical transitions** (e.g., when drift crosses zero, signaling phase change).

### 4.3. Feedback Loop (v2.4+ Vision)

```
Δ12/Δ144 → TW369 (forward: state defines dynamics)
    ↓
TW369 drift → Δ12/Δ144 (backward: dynamics modulate state)
```

**Current**: Open loop (Δ12/Δ144 → TW369 only)  
**v2.4+**: Closed loop (TW369 drift feeds back to adjust Δ12 probabilities)

---

## 5. Impact on Products (Alpha/Geo/Product/Safeguard)

### 5.1. KALDRA-Alpha (Financial Markets)

**Δ12 Role**: Identify market regime archetype
- **RULER** → Institutional control, regulatory focus
- **REBEL** → Disruption, volatility, innovation
- **SAGE** → Information asymmetry, wisdom premium

**Δ144 Role**: Pinpoint specific market state
- `A07_RULER_6_05` → Defensive institutions (risk-off)
- `A08_REBEL_3_01` → Disruptive innovation (risk-on)
- `A10_SAGE_9_09` → Market wisdom synthesis (inflection point)

**Signal Translation**:
```
Δ12[RULER] = 0.7 → "Institutional dominance"
Δ144 = A07_RULER_6_06 → "Reactive regulation"
→ Alpha Signal: "Regulatory tightening likely, defensive positioning"
```

### 5.2. KALDRA-Geo (Geopolitical Risk)

**Δ12 Role**: Identify geopolitical archetype
- **WARRIOR** → Conflict, aggression
- **CAREGIVER** → Humanitarian focus, aid
- **MAGICIAN** → Transformation, regime change

**Δ144 Role**: Specific geopolitical state
- `A03_WARRIOR_3_02` → Escalating conflict
- `A04_CAREGIVER_6_07` → Defensive humanitarianism
- `A09_MAGICIAN_9_10` → Shadow revelation (hidden agendas exposed)

**Signal Translation**:
```
Δ12[WARRIOR] = 0.8 → "Conflict archetype dominant"
Δ144 = A03_WARRIOR_6_05 → "Defensive posturing"
→ Geo Signal: "Tensions high but not yet kinetic, watch for triggers"
```

### 5.3. KALDRA-Product (Product-Market Fit)

**Δ12 Role**: Product archetype
- **CREATOR** → Innovation-driven
- **CAREGIVER** → User-centric, empathy
- **JESTER** → Playful, engaging

**Δ144 Role**: Product lifecycle state
- `A12_CREATOR_3_01` → Early innovation
- `A04_CAREGIVER_6_05` → Mature, defensive (feature parity)
- `A11_JESTER_9_11` → Transcendent playfulness (viral potential)

### 5.4. KALDRA-Safeguard (Narrative Risk)

**Δ12 Role**: Narrative archetype
- **INNOCENT** → Naive, vulnerable
- **ORPHAN** → Victimhood, grievance
- **REBEL** → Resistance, disruption

**Δ144 Role**: Specific narrative risk state
- `A01_INNOCENT_6_06` → Defensive naivety (denial)
- `A02_ORPHAN_9_10` → Shadow orphan (radicalization risk)
- `A08_REBEL_3_03` → Accelerating rebellion

**Signal Translation**:
```
Δ12[ORPHAN] = 0.6 → "Grievance narrative"
Δ144 = A02_ORPHAN_9_10 → "Shadow revelation imminent"
→ Safeguard Signal: "High radicalization risk, monitor for action triggers"
```

---

## 6. Mathematical Formalism (v2.4+ Vision)

### 6.1. Δ12 as Probability Simplex

```
Δ12 ∈ Δ¹¹ (11-simplex in ℝ¹²)
```

**Properties**:
- Convex
- Bounded
- Differentiable (for gradient-based optimization)

### 6.2. Δ144 as Manifold Embedding

```
Δ144: Δ¹¹ × ℝ³ × ℝ³ × ℝ⁶² → S¹⁴³ (143-simplex)
```

Where:
- **Δ¹¹**: Δ12 base
- **ℝ³**: TW369 plane scores
- **ℝ³**: Profile scores
- **ℝ⁶²**: Modifier scores
- **S¹⁴³**: 144-state probability distribution

### 6.3. Temporal Evolution

```
Δ12(t+1) = Δ12(t) + α · ∇drift(Δ144(t))
```

**Interpretation**: Drift in Δ144 state space feeds back to adjust Δ12 probabilities over time.

**v2.4 Goal**: Implement this feedback loop with configurable α (learning rate).

---

## 7. Implementation Roadmap (v2.4+)

### Phase 1: Explicit Δ12 Representation
- [ ] Create `Delta12Vector` dataclass
- [ ] Implement Kindra → Δ12 projection
- [ ] Store Δ12 alongside Δ144 in KALDRA signal

### Phase 2: Δ12 ↔ TW369 Integration
- [ ] Map Δ12 archetypes to TW369 regime parameters
- [ ] Use Δ12 to configure Painlevé filter sensitivity
- [ ] Document archetype-specific drift tolerances

### Phase 3: Temporal Feedback Loop
- [ ] Implement drift → Δ12 adjustment
- [ ] Add memory/persistence for Δ12 evolution
- [ ] Create visualization of Δ12 trajectory over time

---

## 8. References

- **Schema**: `schema/archetypes/archetypes_12.core.json`
- **Schema**: `schema/archetypes/delta144_states.core.json`
- **Code**: `src/archetypes/delta144_engine.py`
- **Docs**: `docs/math/DELTA144_INFERENCE.md`
- **Docs**: `docs/math/TW369_ENGINE_SPEC.md`

---

**Status**: Planning document for v2.4  
**Next**: Integrate with TW369 deepening and drift memory specs
