# KALDRA Master Engine V2 - Technical Documentation

**Version**: 2.0  
**Last Updated**: 2025-11-23  
**Status**: Production

---

## Overview

The KALDRA Master Engine V2 is the central orchestrator of the symbolic intelligence system, integrating four core components to produce comprehensive narrative analysis signals.

---

## Architecture

### Component Integration

```
┌─────────────────────────────────────────────────────────┐
│           KALDRA Master Engine V2                       │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Delta144   │  │    Kindra    │  │  TW-Painlevé │ │
│  │    Engine    │→ │  Cultural    │→ │    Oracle    │ │
│  │              │  │  Modulation  │  │              │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│         ↓                  ↓                  ↓        │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Epistemic Limiter (τ Layer)              │  │
│  └──────────────────────────────────────────────────┘  │
│                          ↓                             │
│                   KaldraSignal                         │
└─────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Delta144 Engine

**Purpose**: Semantic archetype inference

**Input**: Embedding vector (d_ctx dimensions)  
**Output**: 144-state probability distribution

**Process**:
1. Generate state embeddings (deterministic RNG from descriptions)
2. Normalize input vector
3. Compute cosine similarity with all 144 states
4. Apply softmax with temperature (τ = 0.65)

**Key Method**:
```python
def infer_from_vector(self, vector: np.ndarray) -> StateInferenceResult:
    # Normalize input
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm
    
    # Compute similarities
    similarities = self.state_embeddings @ vector
    
    # Softmax with temperature
    exp_sim = np.exp(similarities / self.temperature)
    probs = exp_sim / exp_sim.sum()
    
    # Select winner
    winner_idx = np.argmax(probs)
    return StateInferenceResult(...)
```

**Configuration**:
- `d_ctx`: Embedding dimension (default: 256)
- `temperature`: Softmax temperature (default: 0.65)

---

### 2. Kindra Cultural Modulation

**Purpose**: Apply cultural/contextual modulation to archetype probabilities

**Input**: 
- Base probabilities (144 states)
- Context embedding (d_ctx dimensions)

**Output**: Modulated probabilities (144 states)

**Architecture** (PyTorch):
```python
class KaldraKindraCulturalMod(nn.Module):
    def __init__(self, d_ctx=256):
        # Context normalization
        self.ctx_norm = nn.LayerNorm(d_ctx)
        
        # Projection to 48 Kindra vectors (per plane)
        self.W = nn.ModuleDict({
            p: nn.Linear(d_ctx, 48) for p in ["3", "6", "9"]
        })
        
        # Mapping 48 Kindras → 144 states (per plane)
        self.M = nn.ParameterDict({
            p: nn.Parameter(torch.randn(48, 144) * 0.01)
            for p in ["3", "6", "9"]
        })
        
        # Plane weights (learnable)
        self.lambda_raw = nn.Parameter(torch.zeros(3))
```

**Process**:
1. Normalize context
2. Project to Kindra space (3 planes × 48 vectors)
3. Apply sigmoid activation
4. Map to state space via learned matrices
5. Weighted combination of planes
6. Modulate base probabilities

---

### 3. TW-Painlevé Oracle

**Purpose**: Detect anomalies in time-series data using Tracy-Widom distribution

**Input**: Time window of observations (optional)  
**Output**: `(tw_trigger: bool, tw_stats: TWStats)`

**Algorithm**:
1. Compute covariance matrix
2. Extract eigenvalues
3. Apply Painlevé filter (edge correction heuristic)
4. Compare max eigenvalue to Tracy-Widom threshold
5. Trigger if λ_max > threshold

**Key Parameters**:
- `beta`: Matrix ensemble type (1=GOE, 2=GUE, 4=GSE)
- `threshold`: Detection threshold (default: 2.0)

**Current Implementation**:
- Painlevé filter: Stub with 2% damping for λ > 2.0
- Future: Full Painlevé II numerical solution

---

### 4. Epistemic Limiter (τ Layer)

**Purpose**: Assess confidence and delegate low-confidence decisions

**Input**: Probability distribution (144 states)  
**Output**: `EpistemicDecision`

**Decision Logic**:
```python
def from_probs(self, probs: np.ndarray) -> EpistemicDecision:
    max_prob = float(probs.max())
    
    if max_prob >= self.tau:
        return EpistemicDecision(
            confidence=max_prob,
            status="OK",
            should_delegate=False
        )
    else:
        return EpistemicDecision(
            confidence=max_prob,
            status="INCONCLUSIVO",
            should_delegate=True
        )
```

**Configuration**:
- `tau`: Confidence threshold (default: 0.65)

---

## Master Engine Pipeline

### Initialization

```python
class KaldraMasterEngineV2:
    def __init__(
        self,
        delta_engine: Optional[Delta144Engine] = None,
        d_ctx: int = 256,
        tau: float = 0.65
    ):
        # Initialize components
        self.delta = delta_engine or Delta144Engine.from_default_files(d_ctx=d_ctx)
        self.kindra_mod = KaldraKindraCulturalMod(d_ctx=d_ctx)
        self.tau_layer = EpistemicLimiter(tau=tau)
        self.tw_oracle = TWPainleveOracle()
```

### Inference Flow

```python
def infer_from_embedding(
    self,
    embedding: np.ndarray,
    tw_window: Optional[np.ndarray] = None
) -> KaldraSignal:
    # 1. Delta144 inference
    result = self.delta.infer_from_vector(embedding)
    base_probs = np.asarray(result.probs, dtype=float)
    
    # 2. Kindra modulation
    ctx = torch.tensor(embedding, dtype=torch.float32).unsqueeze(0)
    probs_t = torch.tensor(base_probs, dtype=torch.float32).unsqueeze(0)
    modulated = self.kindra_mod(probs_t, ctx, apply_softmax=True)[0]
    modulated_np = modulated.detach().cpu().numpy()
    
    # 3. TW anomaly detection (optional)
    tw_trigger = False
    tw_stats = None
    if tw_window is not None:
        tw_trigger, tw_stats = self.tw_oracle.detect(tw_window)
    
    # 4. Epistemic limiting
    epistemic = self.tau_layer.from_probs(modulated_np)
    
    # 5. Return signal
    return KaldraSignal(
        archetype_probs=modulated_np,
        tw_trigger=tw_trigger,
        tw_stats=tw_stats,
        epistemic=epistemic,
        delta_state=result.to_dict()
    )
```

---

## Output Schema

### KaldraSignal

```python
@dataclass
class KaldraSignal:
    archetype_probs: np.ndarray      # 144 probabilities
    tw_trigger: bool                  # Anomaly detected
    tw_stats: Optional[TWStats]       # TW statistics
    epistemic: EpistemicDecision      # Confidence assessment
    delta_state: Optional[Any]        # Delta144 result dict
```

### StateInferenceResult (Delta144)

```python
@dataclass
class StateInferenceResult:
    archetype: Archetype              # Winning archetype
    state: ArchetypeState             # Specific state
    active_modifiers: List[Modifier]  # Applied modifiers
    scores: Dict[str, Any]            # Plane/profile scores
    probs: List[float]                # Full distribution
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "archetype": {
                "id": self.archetype.id,
                "label": self.archetype.label,
                "essence": self.archetype.essence
            },
            "state": {
                "id": self.state.id,
                "label": self.state.label,
                "profile": self.state.profile,
                "description": self.state.description
            },
            "active_modifiers": [...],
            "scores": self.scores
        }
```

---

## Configuration

### Default Configuration

```python
@classmethod
def from_default_files(
    cls,
    d_ctx: int = 256,
    tau: float = 0.65
) -> "KaldraMasterEngineV2":
    delta = Delta144Engine.from_default_files(d_ctx=d_ctx)
    return cls(delta_engine=delta, d_ctx=d_ctx, tau=tau)
```

### Tunable Parameters

| Parameter | Default | Range | Impact |
|-----------|---------|-------|--------|
| `d_ctx` | 256 | 64-512 | Embedding dimension |
| `tau` | 0.65 | 0.5-0.9 | Confidence threshold |
| `temperature` | 0.65 | 0.1-2.0 | Softmax sharpness |

---

## Performance Characteristics

### Computational Complexity

- **Delta144 Inference**: O(d_ctx × 144) - cosine similarity
- **Kindra Modulation**: O(d_ctx × 48 × 3) - neural network forward pass
- **TW Detection**: O(n²) - covariance computation (n = window size)
- **Epistemic Limiting**: O(144) - max probability

### Memory Footprint

- State embeddings: ~144 × d_ctx × 8 bytes
- Kindra parameters: ~(d_ctx × 48 + 48 × 144) × 3 planes × 4 bytes
- Total: ~500KB for d_ctx=256

### Latency

- **Without TW**: ~50-100ms
- **With TW** (window=100): ~150-200ms

---

## Testing

### Unit Tests

**Location**: `tests/test_master_engine_v2.py`

**Coverage**:
- Initialization
- Inference without TW
- Inference with TW window

**Results**: 3/3 passing ✅

### Integration Tests

**Location**: `tests/test_integration_master_engine.py`

**Coverage**:
- Full flow validation
- TW anomaly detection
- Determinism
- Low confidence delegation

**Results**: 4/4 passing ✅

---

## Future Enhancements

### Planned Improvements

1. **Embedding Generation**
   - Replace hash-based placeholder with real sentence encoder
   - Options: SentenceTransformers, OpenAI embeddings

2. **Painlevé Filter**
   - Implement full Painlevé II numerical solution
   - Improve edge correction accuracy

3. **Kindra Learning**
   - Train Kindra modulation on labeled data
   - Fine-tune plane weights

4. **Performance**
   - GPU acceleration for batch processing
   - Caching for repeated queries

---

## References

- [Delta144 Engine Documentation](./DELTA144_INFERENCE.md)
- [API Gateway Walkthrough](./API_GATEWAY_WALKTHROUGH.md)
- [CHANGELOG v2.1](../CHANGELOG_v2.1.md)

---

**Maintained by**: 4IAM.AI Engineering Team  
**Last Review**: 2025-11-23
