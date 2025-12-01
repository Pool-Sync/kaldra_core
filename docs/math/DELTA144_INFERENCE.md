# Delta144 Semantic Inference - Technical Documentation

**Version**: 2.0  
**Last Updated**: 2025-11-23  
**Component**: Delta144 Engine

---

## Overview

The Delta144 Engine performs semantic archetype inference by matching input embeddings against a symbolic state space of 144 archetypal states (12 archetypes × 12 states each).

---

## Architecture

### State Space Structure

```
12 Archetypes × 12 States = 144 Total States

Archetypes (12):
├── A01_INNOCENT
├── A02_ORPHAN
├── A03_WARRIOR
├── A04_CAREGIVER
├── A05_SEEKER
├── A06_LOVER
├── A07_RULER
├── A08_REBEL
├── A09_MAGICIAN
├── A10_SAGE
├── A11_JESTER
└── A12_CREATOR

Each Archetype has 12 States:
├── Plane 3 (States 01-04): Foundational
├── Plane 6 (States 05-08): Relational
└── Plane 9 (States 09-12): Transcendent
```

### State Profiles

Each state belongs to one of three profiles:
- **EXPANSIVE**: Growth, exploration, outward movement
- **CONTRACTIVE**: Consolidation, inward focus, preservation
- **TRANSCENDENT**: Integration, transformation, synthesis

---

## Semantic Inference Algorithm

### 1. State Embedding Generation

**Purpose**: Create semantic representations for all 144 states

**Method**: Deterministic RNG seeded by state descriptions

```python
def _init_state_embeddings(self) -> np.ndarray:
    """
    Generate embeddings for all 144 states.
    Uses deterministic RNG seeded by state description.
    """
    embeddings = np.zeros((144, self.d_ctx), dtype=np.float32)
    
    for idx, state in enumerate(sorted_states):
        # Seed RNG with state description
        seed_text = f"{state.id}_{state.label}_{state.description}"
        seed = sum(ord(c) for c in seed_text) % (2**32)
        rng = np.random.RandomState(seed)
        
        # Generate embedding
        emb = rng.randn(self.d_ctx).astype(np.float32)
        
        # Normalize
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb = emb / norm
        
        embeddings[idx] = emb
    
    return embeddings
```

**Characteristics**:
- Deterministic (same state → same embedding)
- Normalized (unit vectors)
- High-dimensional (d_ctx = 256 default)

---

### 2. Cosine Similarity Computation

**Purpose**: Measure semantic similarity between input and all states

**Formula**:
```
similarity(input, state) = (input · state) / (||input|| × ||state||)
```

### 3. Modifier Auto-Inference (v2.7)

**Purpose**: Automatically detect active modifiers (e.g., "Wounded", "Exiled") based on semantic similarity.

**Method**:
1.  **Modifier Embeddings**: Pre-computed embeddings for all 59 modifiers.
2.  **Similarity Check**: Compute cosine similarity between input text embedding and all modifier embeddings.
3.  **Thresholding**: Apply modifiers with similarity > `KALDRA_MODIFIER_THRESHOLD` (default: 0.65).
4.  **Integration**: Inferred modifiers are combined with manually specified modifiers.

```python
def infer_modifier_scores_from_embedding(self, embedding: np.ndarray) -> Dict[str, float]:
    """
    Infer modifier scores based on cosine similarity with input embedding.
    """
    scores = {}
    
    # Compute dot product with all modifier embeddings
    # (assuming normalized vectors)
    similarities = np.dot(self.modifier_embeddings_matrix, embedding)
    
    for idx, score in enumerate(similarities):
        if score > self.modifier_threshold:
            mod_id = self.modifier_ids[idx]
            scores[mod_id] = float(score)
            
    return scores
```

**Implementation**:
```python
# Normalize input
norm = np.linalg.norm(vector)
if norm > 0:
    vector = vector / norm

# Compute dot products (cosine similarity for unit vectors)
similarities = self.state_embeddings @ vector
```

**Output**: 144 similarity scores in [-1, 1]

---

## 3. Semantic Embeddings (v2.3)

As of v2.3, the engine supports real semantic embeddings via the `EmbeddingGenerator`.

### Architecture
- **EmbeddingGenerator** (`src/core/embedding_generator.py`): Unified provider for embeddings.
- **Providers**:
    - `legacy`: Deterministic simulation based on text hash (default).
    - `openai`: Uses OpenAI API (via `requests` or injected client).
    - `sentence-transformers`: Uses local models (if installed).

### Configuration
Set via environment variables:
```bash
KALDRA_EMBEDDINGS_MODE=REAL  # or LEGACY
KALDRA_EMBEDDINGS_API_KEY=sk-...
KALDRA_EMBEDDINGS_MODEL=text-embedding-3-small
```

When `KALDRA_EMBEDDINGS_MODE=REAL`, the engine will attempt to use OpenAI by default if no other provider is explicitly configured in code.

---

### 4. Softmax with Temperature

**Purpose**: Convert similarities to probability distribution

**Formula**:
```
prob_i = exp(similarity_i / τ) / Σ exp(similarity_j / τ)
```

**Temperature (τ) Effects**:
- **Low τ (0.1-0.5)**: Sharp distribution (high confidence)
- **Medium τ (0.5-1.0)**: Balanced distribution
- **High τ (1.0-2.0)**: Flat distribution (low confidence)

**Implementation**:
```python
# Apply softmax with temperature
exp_sim = np.exp(similarities / self.temperature)
probs = exp_sim / exp_sim.sum()
```

**Default**: τ = 0.65

---

### 4. Winner Selection

**Purpose**: Identify dominant archetype and state

**Method**: Argmax over probability distribution

```python
winner_idx = int(np.argmax(probs))
winner_state = sorted_states[winner_idx]
winner_archetype = self.archetypes[winner_state.archetype_id]
```

---

## Data Structures

### Archetype

```python
@dataclass
class Archetype:
    id: str              # e.g., "A07_RULER"
    label: str           # e.g., "Ruler"
    essence: str         # Core description
    shadow: str          # Shadow aspect
    gift: str            # Positive manifestation
    task: str            # Developmental task
    fear: str            # Core fear
```

**Example**:
```python
Archetype(
    id="A07_RULER",
    label="Ruler",
    essence="Creates order, stability, and prosperity",
    shadow="Tyranny, rigidity, control",
    gift="Leadership, responsibility, organization",
    task="Create a prosperous, successful environment",
    fear="Chaos, being overthrown"
)
```

---

### ArchetypeState

```python
@dataclass
class ArchetypeState:
    id: str              # e.g., "A07_RULER_6_05"
    archetype_id: str    # e.g., "A07_RULER"
    row: int             # 1-12 (archetype index)
    col: int             # 1-12 (state index)
    plane: str           # "3", "6", or "9"
    profile: str         # "EXPANSIVE", "CONTRACTIVE", "TRANSCENDENT"
    label: str           # Human-readable name
    description: str     # Detailed description
```

**Example**:
```python
ArchetypeState(
    id="A07_RULER_6_05",
    archetype_id="A07_RULER",
    row=7,
    col=5,
    plane="6",
    profile="EXPANSIVE",
    label="Diplomatic Leadership",
    description="Balances authority with collaboration..."
)
```

---

### StateInferenceResult

```python
@dataclass
class StateInferenceResult:
    archetype: Archetype              # Winning archetype
    state: ArchetypeState             # Specific state
    active_modifiers: List[Modifier]  # Applied modifiers
    scores: Dict[str, Any]            # Breakdown scores
    probs: List[float]                # Full 144 distribution
```

**Scores Structure**:
```python
{
    "plane_scores": {
        "3": 0.25,  # Foundational plane contribution
        "6": 0.45,  # Relational plane contribution
        "9": 0.30   # Transcendent plane contribution
    },
    "profile_scores": {
        "EXPANSIVE": 0.40,
        "CONTRACTIVE": 0.35,
        "TRANSCENDENT": 0.25
    },
    "chosen_state_score": 0.15  # Winner probability
}
```

---

## Configuration

### Initialization

```python
class Delta144Engine:
    def __init__(
        self,
        archetypes: Dict[str, Archetype],
        states: Dict[str, ArchetypeState],
        modifiers: Dict[str, Modifier],
        d_ctx: int = 256,
        temperature: float = 0.65
    ):
        self.d_ctx = d_ctx
        self.temperature = temperature
        self.state_embeddings = self._init_state_embeddings()
```

### Factory Method

```python
@classmethod
def from_default_files(cls, d_ctx: int = 256) -> "Delta144Engine":
    """Load from schema files and initialize"""
    archetypes = load_archetypes(SCHEMA_DIR / "archetypes.core.json")
    states = load_states(SCHEMA_DIR / "delta144_states.core.json")
    modifiers = load_modifiers(SCHEMA_DIR / "archetype_modifiers.core.json")
    
    return cls(
        archetypes=archetypes,
        states=states,
        modifiers=modifiers,
        d_ctx=d_ctx
    )
```

---

## Performance

### Computational Complexity

**Time Complexity**:
- Embedding generation (one-time): O(144 × d_ctx)
- Inference per query: O(144 × d_ctx)

**Space Complexity**:
- State embeddings: 144 × d_ctx × 4 bytes
- For d_ctx=256: ~147 KB

### Benchmarks

| d_ctx | Inference Time | Memory |
|-------|---------------|--------|
| 128   | ~20ms         | 74 KB  |
| 256   | ~40ms         | 147 KB |
| 512   | ~80ms         | 295 KB |

---

## Semantic Interpretation

### Plane Semantics

**Plane 3 (Foundational)**:
- States 01-04
- Core identity, basic drives
- Individual focus
- Example: "A07_RULER_3_01" - "Establishing Authority"

**Plane 6 (Relational)**:
- States 05-08
- Interpersonal dynamics, relationships
- Social focus
- Example: "A07_RULER_6_05" - "Diplomatic Leadership"

**Plane 9 (Transcendent)**:
- States 09-12
- Integration, higher purpose
- Collective focus
- Example: "A07_RULER_9_09" - "Servant Leadership"

### Profile Semantics

**EXPANSIVE**:
- Outward movement
- Growth, exploration
- Risk-taking
- States: 01, 04, 05, 08, 09, 12

**CONTRACTIVE**:
- Inward movement
- Consolidation, preservation
- Risk-averse
- States: 02, 03, 06, 07, 10, 11

**TRANSCENDENT**:
- Integration
- Synthesis of opposites
- Transformation
- States with high plane 9 contribution

---

## Testing

### Unit Tests

**Location**: `tests/test_delta144_engine.py`

**Test**: `test_delta144_semantic_inference`
```python
def test_delta144_semantic_inference():
    engine = Delta144Engine.from_default_files(d_ctx=128)
    
    # Test vector
    vec = np.random.randn(128).astype(np.float32)
    
    # Infer
    result = engine.infer_from_vector(vec)
    
    # Validate
    assert result.archetype is not None
    assert result.state is not None
    assert len(result.probs) == 144
    assert abs(sum(result.probs) - 1.0) < 1e-5  # Probabilities sum to 1
```

**Results**: 1/1 passing ✅

---

## Future Enhancements

### 1. Learned Embeddings

**Current**: Deterministic RNG  
**Future**: Train embeddings on labeled data

**Approach**:
- Collect text samples labeled with archetypes
- Train encoder (e.g., BERT fine-tuned)
- Learn state embeddings via contrastive learning

### 2. Dynamic Temperature

**Current**: Fixed τ = 0.65  
**Future**: Adaptive temperature based on input uncertainty

**Formula**:
```
τ(input) = τ_base × (1 + uncertainty(input))
```

### 3. Multi-Modal Inference

**Current**: Text embeddings only  
**Future**: Support image, audio, video

**Architecture**:
- Multi-modal encoder (e.g., CLIP)
- Unified embedding space
- Same inference algorithm

---

## References

- Schema: `schema/archetypes/archetypes.core.json`
- Schema: `schema/archetypes/delta144_states.core.json`
- Code: `src/archetypes/delta144_engine.py`
- Tests: `tests/test_delta144_engine.py`

---

**Maintained by**: 4IAM.AI Engineering Team  
**Last Review**: 2025-11-23
