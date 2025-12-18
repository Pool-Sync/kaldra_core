# KindraEngine v3.1 — Technical Documentation

## Overview
**KindraEngine v3.1** is the semantic and cultural analysis engine for KALDRA, operating on **3×48 vectors (144 total)** across three conceptual layers.

---

## Architecture

### Layers
1. **Layer 1 — Cultural/Macro (48 vectors)**
   - Global cultural patterns, zeitgeist, macro narratives
   - Maps to TW369 Plane 3 (Material/Physical)

2. **Layer 2 — Semiotic/Media (48 vectors)**
   - Media discourse, symbolic systems, communication patterns
   - Maps to TW369 Plane 6 (Relational/Emotional)

3. **Layer 3 — Structural/Systemic (48 vectors)**
   - Deep structural patterns, systemic forces, abstract dynamics
   - Maps to TW369 Plane 9 (Abstract/Conceptual)

---

## Core Components

### `KindraEngine`
Located: `src/kindras/kindra_engine.py`

**Main Method:**
```python
def score_all_layers(
    text: str,
    embedding: Optional[np.ndarray] = None,
    delta144_state: Optional[str] = None,
    archetype_scores: Optional[Dict[str, float]] = None
) -> KindraContext
```

**Responsibilities:**
1. Score all 144 vectors (3×48) against input text
2. Calculate TW plane distribution (3/6/9)
3. Aggregate Delta144 weights using normalized maps
4. Return populated `KindraContext`

---

### `KindraLLMScorer`
Located: `src/kindras/llm_adapter.py`

**Scoring Strategy (v3.1):**
- Heuristic keyword matching
- Direct mention detection (ID/name)
- Example/keyword frequency analysis
- Simple saturation curve

**Future (v3.2+):**
- Real LLM API calls (OpenAI/local)
- Embedding similarity integration
- Contextual relevance scoring

---

### Loaders
Located: `src/kindras/loaders.py`

**Functions:**
- `load_layer_vectors(layer: int)` → Dict of vector definitions
- `load_layer_mapping(layer: int)` → Kindra→Delta144 mapping

**Data Source:** `schema/kindras/`
- `kindra_vectors_layer1_cultural_macro_48.json`
- `kindra_vectors_layer2_semiotic_media_48.json`
- `kindra_vectors_layer3_structural_systemic_48.json`
- `kindra_layer1_to_delta144_map.json`
- `kindra_layer2_to_delta144_map.json`
- `kindra_layer3_to_delta144_map.json`

---

## KindraContext Output

```python
@dataclass
class KindraContext:
    layer1: Dict[str, float]              # 48 vector scores
    layer2: Dict[str, float]              # 48 vector scores
    layer3: Dict[str, float]              # 48 vector scores
    tw_plane_distribution: Dict[int, float]  # {3: 0.33, 6: 0.33, 9: 0.34}
    delta144_weights: Dict[str, float]    # Aggregated Delta144 influence
    metadata: Dict[str, Any]              # Engine version, etc.
```

---

## Integration Points

### 1. CoreStage
```python
# CoreStage.execute()
kindra_ctx = self.kindra_engine.score_all_layers(
    text=context.input_ctx.text,
    embedding=context.input_ctx.embedding,
    delta144_state=delta144_result.state.id,
    archetype_scores=delta12.scores
)
context.kindra_ctx = kindra_ctx
```

### 2. MetaStage (ConsumesKindra data)
All three meta-engines (Nietzsche, Aurelius, Campbell) receive `meta_input.kindra` populated with real Kindra data.

---

## Testing

### Unit Tests
`tests/kindras/test_kindra_engine.py` — 5 tests
- Execution without error
- Layer population (48 vectors each)
- TW plane distribution normalization
- Delta144 weight aggregation

### Integration Tests
`tests/unification/test_core_stage_integration.py` — 2 tests
- CoreStage integration flow
- Dependency injection/fallback

**Status:** ✅ All 12 tests passing

---

## Limitations (v3.1)

1. **Heuristic scoring only** — Real LLM integration deferred to v3.2
2. **No embedding similarity** — Embedding integration planned for v3.2
3. **Static mapping** — Delta144 weights use fixed maps, not learned
4. **No temporal analysis** — Kindra drift tracking is v3.2+
5. **No domain calibration** — Domain-specific tuning is v3.3+

---

## Future Roadmap

### v3.2 — Kindra Temporal
- Integrate with StoryBuffer
- Track Kindra drift over time
- Temporal pattern detection

### v3.3 — Kindra Domains
- Domain-specific profiles (Alpha, Geo, Product, Safeguard)
- Custom vector weights per domain

### v3.4 — Kindra Explainable
- Trace vector scores back to text excerpts
- Generate human-readable explanations

### v3.5–v3.6 — Kindra Learned
- Learn optimal vector weights from data
- Adaptive mapping to Delta144
