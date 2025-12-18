# KALDRA Core — Meta Engine Routing (v2.3)

**Version:** 2.3  
**Status:** Production-Ready  
**Last Updated:** 2025-11-26  

---

## 1. Overview

Meta Engine Routing provides intelligent, context-based routing and orchestration for KALDRA engine variants. Instead of manually selecting which engine to use, the system automatically analyzes input context and routes to the most appropriate variant.

### Engine Variants

- **default**: General-purpose engine (τ=0.65)
- **alpha**: Financial analysis (τ=0.70, higher certainty)
- **geo**: Geopolitical analysis (τ=0.65, standard)
- **product**: UX/Product analysis (τ=0.60, more exploration)
- **safeguard**: Safety/moderation (τ=0.75, conservative)

---

## 2. Architecture

### Components

**MetaRouter** (`src/meta/engine_router.py`):
- Analyzes input context
- Determines primary and secondary engines
- Returns routing decision with confidence score

**MetaOrchestrator** (`src/meta/engine_orchestrator.py`):
- Coordinates execution across engines
- Handles fallback logic
- Manages timing and error handling

---

## 3. Routing Logic

### Priority Order

1. **Explicit Domain Hints** (confidence: 1.0)
   ```python
   context = RoutingContext(domain_hints=["alpha"])
   # Always routes to alpha
   ```

2. **Metadata-Based Routing** (confidence: 0.8-1.0)
   ```python
   context = RoutingContext(metadata={"domain": "finance"})
   # Routes to alpha
   ```

3. **Keyword-Based Routing** (confidence: varies)
   ```python
   context = RoutingContext(text="earnings revenue profit EPS")
   # Analyzes keywords, routes to alpha if confidence > threshold
   ```

4. **Fallback to Default** (confidence: 1.0)
   ```python
   context = RoutingContext()  # Empty
   # Routes to default
   ```

### Confidence Threshold

Default: `0.3` (30%)

- Below threshold → routes to `default`
- Above threshold → routes to detected engine
- Can be customized: `MetaRouter(confidence_threshold=0.5)`

---

## 4. Usage Examples

### Basic Usage (Automatic Routing)

```python
from src.meta import MetaOrchestrator, RoutingContext
import numpy as np

orchestrator = MetaOrchestrator()
embedding = np.random.randn(256).astype(np.float32)

# Automatic routing based on text
context = RoutingContext(
    text="The company reported strong earnings with revenue growth."
)

result = orchestrator.execute(embedding, context=context)

print(f"Routed to: {result.primary_result.engine_name}")
print(f"Confidence: {result.routing_decision.confidence:.2f}")
print(f"Reasoning: {result.routing_decision.reasoning}")
```

### Explicit Engine Selection

```python
from src.meta import RoutingDecision

# Force specific engine
decision = RoutingDecision(
    primary_engine="geo",
    confidence=1.0
)

result = orchestrator.execute(embedding, routing_decision=decision)
```

### Using Domain Hints

```python
# Explicit hints (most reliable)
context = RoutingContext(
    text="Some text",
    domain_hints=["alpha", "finance"]
)

result = orchestrator.execute(embedding, context=context)
# Guaranteed to route to alpha
```

### Using Metadata

```python
# Metadata-based routing
context = RoutingContext(
    text="Quarterly report",
    metadata={
        "domain": "finance",
        "source": "earnings_call"
    }
)

result = orchestrator.execute(embedding, context=context)
# High confidence routing to alpha
```

### Multi-Engine Execution

```python
# Execute secondary engines
decision = RoutingDecision(
    primary_engine="alpha",
    confidence=0.8,
    secondary_engines=["geo"]  # Also run geo
)

result = orchestrator.execute(embedding, routing_decision=decision)

print(f"Primary: {result.primary_result.engine_name}")
print(f"Secondaries: {[r.engine_name for r in result.secondary_results]}")
```

### Custom Configuration

```python
from src.meta import OrchestrationConfig

config = OrchestrationConfig(
    fallback_to_default=True,  # Use default if primary fails
    timeout_seconds=5.0         # Optional timeout
)

orchestrator = MetaOrchestrator(config=config)
```

---

## 5. Routing Decision Structure

```python
@dataclass
class RoutingDecision:
    primary_engine: str              # "alpha" | "geo" | "product" | "safeguard" | "default"
    confidence: float                # 0.0 to 1.0
    secondary_engines: List[str]     # Additional engines to run
    reasoning: Optional[str]         # Explanation of decision
```

**Example**:
```python
RoutingDecision(
    primary_engine="alpha",
    confidence=0.85,
    secondary_engines=["geo"],
    reasoning="Routed via keywords analysis (confidence: 0.85)"
)
```

---

## 6. Orchestration Result Structure

```python
@dataclass
class OrchestrationResult:
    primary_result: EngineResult           # Result from primary engine
    secondary_results: List[EngineResult]  # Results from secondary engines
    routing_decision: RoutingDecision      # The routing decision made
    total_time: float                      # Total execution time (seconds)
```

**EngineResult**:
```python
@dataclass
class EngineResult:
    engine_name: str                # Name of engine
    signal: Optional[KaldraSignal]  # Output signal
    execution_time: float           # Time taken (seconds)
    success: bool                   # Whether execution succeeded
    error: Optional[str]            # Error message if failed
```

---

## 7. Domain Keywords

### Alpha (Financial)
`earnings`, `revenue`, `profit`, `EPS`, `guidance`, `forecast`, `market`, `stock`, `investor`, `shareholder`, `dividend`, `quarterly`, `annual`, `financial`, `valuation`, `growth`, `margin`, `EBITDA`, `cash flow`, `balance sheet`, `income statement`

### GEO (Geopolitical)
`diplomatic`, `diplomacy`, `sanctions`, `treaty`, `conflict`, `geopolitical`, `sovereignty`, `territorial`, `alliance`, `NATO`, `UN`, `security council`, `ambassador`, `foreign policy`, `bilateral`, `multilateral`, `regime`, `government`, `state`, `nation`

### Product (UX/Product)
`user`, `UX`, `UI`, `interface`, `experience`, `journey`, `friction`, `usability`, `design`, `feature`, `workflow`, `onboarding`, `conversion`, `engagement`, `retention`, `churn`, `feedback`, `pain point`, `customer`, `satisfaction`, `NPS`

### Safeguard (Safety/Moderation)
`harmful`, `toxic`, `abuse`, `harassment`, `hate`, `violence`, `manipulation`, `misinformation`, `disinformation`, `propaganda`, `extremism`, `radicalization`, `threat`, `dangerous`, `illegal`, `inappropriate`, `offensive`, `explicit`, `NSFW`, `moderation`

---

## 8. Performance

### Routing Overhead

- Keyword analysis: < 1ms
- Metadata analysis: < 0.1ms
- Total routing overhead: < 2ms

### Execution Time

- Single engine: ~15-20ms (typical)
- With routing: ~17-22ms (routing + execution)
- Multi-engine: ~35-45ms (sequential execution)

---

## 9. Error Handling

### Fallback Behavior

If primary engine fails and `fallback_to_default=True`:
```python
result = orchestrator.execute(embedding, routing_decision=invalid_decision)
# Automatically falls back to default engine
assert result.primary_result.engine_name == "default"
assert result.primary_result.success == True
```

### No Fallback

```python
config = OrchestrationConfig(fallback_to_default=False)
orchestrator = MetaOrchestrator(config=config)

result = orchestrator.execute(embedding, routing_decision=invalid_decision)
# Returns failed result without fallback
assert result.primary_result.success == False
assert result.primary_result.error is not None
```

---

## 10. Testing

### Test Coverage

- **Router Tests**: 13 tests
- **Orchestrator Tests**: 14 tests
- **Total**: 27 tests, all passing

### Running Tests

```bash
# All meta tests
pytest tests/meta/ -v

# Router only
pytest tests/meta/test_engine_router.py -v

# Orchestrator only
pytest tests/meta/test_engine_orchestrator.py -v
```

---

## 11. Future Enhancements

### Phase 1 (v2.4)
- **LLM-Based Routing**: Use embedding similarity for more accurate routing
- **Learned Routing**: Train classifier on labeled data
- **Adaptive Routing**: Learn from user feedback

### Phase 2 (v2.5)
- **Parallel Execution**: Run multiple engines concurrently
- **Streaming Results**: Yield results as they become available
- **Confidence Calibration**: Improve confidence score accuracy

### Phase 3 (v3.0)
- **Multi-Modal Routing**: Support image, audio, video inputs
- **Cross-Engine Fusion**: Combine results from multiple engines
- **Dynamic Engine Loading**: Load engines on-demand

---

## 12. Known Limitations

### Routing Accuracy

- Keyword-based routing is simple substring matching
- No semantic understanding (yet)
- Requires explicit keywords for best results

### Performance

- Sequential execution only (no parallelization)
- Each engine loads separately (no shared state)
- Routing adds ~2ms overhead

### Configuration

- Engine variants differ only in τ (tau) parameter
- No per-variant TW config or Kindra settings (yet)
- All variants use same Δ144 and Kindra models

---

## 13. API Reference

### MetaRouter

```python
class MetaRouter:
    def __init__(self, confidence_threshold: float = 0.3)
    def route(self, context: RoutingContext) -> RoutingDecision
```

### MetaOrchestrator

```python
class MetaOrchestrator:
    def __init__(self, config: Optional[OrchestrationConfig] = None)
    def execute(
        self,
        embedding: np.ndarray,
        context: Optional[RoutingContext] = None,
        routing_decision: Optional[RoutingDecision] = None,
        tw_window: Optional[np.ndarray] = None,
    ) -> OrchestrationResult
```

### RoutingContext

```python
@dataclass
class RoutingContext:
    text: Optional[str] = None
    embedding: Optional[np.ndarray] = None
    metadata: Optional[Dict[str, Any]] = None
    domain_hints: Optional[List[str]] = None
```

---

## 14. Related Files

- **Implementation**: `src/meta/engine_router.py`, `src/meta/engine_orchestrator.py`
- **Tests**: `tests/meta/test_engine_router.py`, `tests/meta/test_engine_orchestrator.py`
- **Integration**: `src/core/kaldra_master_engine.py`

---

**Document Status**: Complete and Production-Ready  
**Location**: `docs/META_ENGINE_ROUTING.md`
