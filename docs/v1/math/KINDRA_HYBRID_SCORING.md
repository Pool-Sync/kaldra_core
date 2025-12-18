# Kindra Hybrid Scoring (Option C)

## 1. Overview

The **Kindra Hybrid Scoring** system combines LLM-based and Rule-Based scoring using a configurable mixing ratio:

```
score_final = clamp(alpha * score_llm + (1 - alpha) * score_rule)
```

Where:
- `alpha ∈ [0, 1]`: Mixing ratio
- `alpha = 0`: Pure rule-based
- `alpha = 0.5`: Equal mix
- `alpha = 1`: Pure LLM

## 2. Why Hybrid Scoring?

### Advantages

1. **Smooth Transition**: Gradually shift from rule-based to LLM scoring
2. **Risk Mitigation**: Blend deterministic rules with LLM inference
3. **Domain Flexibility**: Different alpha per layer/domain
4. **Fallback Safety**: Maintains rule-based when LLM unavailable
5. **Experimentation**: A/B test different mixing ratios

### Use Cases

- **Conservative Domains**: Low alpha (more rule-based)
- **Experimental Domains**: High alpha (more LLM)
- **Production Rollout**: Gradual alpha increase
- **Layer-Specific**: Different alpha for L1/L2/L3

## 3. Architecture

### Components

1. **KindraHybridScorer** (`src/kindras/kindra_hybrid_scorer.py`)
   - Mixes LLM and rule-based scores
   - Supports global and layer-specific alpha
   - Automatic clamping to [-1, 1]

2. **Configuration** (`schema/kindras/kindra_hybrid_config.json`)
   - `alpha_global`: Default mixing ratio
   - `alpha_layers`: Layer-specific overrides

3. **Integration** (`src/kindras/scoring_dispatcher.py`)
   - Hybrid mode in dispatcher
   - Seamless switching between modes

## 4. Mixing Formula

### Basic Formula

```
score_final = alpha * score_llm + (1 - alpha) * score_rule
```

### With Clamping

```python
def mix(llm, rule, alpha):
    mixed = alpha * llm + (1 - alpha) * rule
    return clamp(mixed, -1.0, 1.0)
```

### Examples

| alpha | LLM Score | Rule Score | Final Score |
|-------|-----------|------------|-------------|
| 0.0   | 0.8       | -0.2       | -0.2        |
| 0.5   | 0.8       | -0.2       | 0.3         |
| 1.0   | 0.8       | -0.2       | 0.8         |

## 5. Configuration

### Global Alpha

```json
{
  "enabled": true,
  "alpha_global": 0.5
}
```

### Layer-Specific Alpha

```json
{
  "enabled": true,
  "alpha_global": 0.5,
  "alpha_layers": {
    "1": 0.7,
    "2": 0.5,
    "3": 0.3
  }
}
```

In this example:
- Layer 1: 70% LLM, 30% rule-based
- Layer 2: 50% LLM, 50% rule-based
- Layer 3: 30% LLM, 70% rule-based

## 6. Usage

### Basic Usage

```python
from src.kindras.kindra_hybrid_scorer import KindraHybridScorer

# Initialize hybrid scorer
scorer = KindraHybridScorer(
    llm_scorer=my_llm_scorer,
    rule_scorer=my_rule_scorer,
    alpha_global=0.5
)

# Score text
scores = scorer.score(
    text="A empresa anunciou inovação...",
    context={"country": "BR", "kindra_layer": 1},
    vectors={"E01": {}, "T25": {}}
)
```

### Integration with Dispatcher

```python
from src.kindras.scoring_dispatcher import KindraScoringDispatcher

# Initialize with hybrid mode
dispatcher = KindraScoringDispatcher(
    llm_client=my_llm_client,
    scoring_mode="hybrid",
    hybrid_config={
        "alpha_global": 0.6,
        "alpha_layers": {"1": 0.8}
    }
)

# Run scoring
result = dispatcher.run_all(context, base_vectors)
```

### Layer-Specific Alpha

```python
scorer = KindraHybridScorer(
    llm_scorer=llm,
    rule_scorer=rule,
    alpha_global=0.5,
    alpha_layers={
        "1": 0.7,  # Layer 1: more LLM
        "3": 0.3   # Layer 3: more rule-based
    }
)

# Layer 1 uses alpha=0.7
scores_l1 = scorer.score(text, {"kindra_layer": 1}, vectors)

# Layer 2 uses alpha_global=0.5
scores_l2 = scorer.score(text, {"kindra_layer": 2}, vectors)

# Layer 3 uses alpha=0.3
scores_l3 = scorer.score(text, {"kindra_layer": 3}, vectors)
```

## 7. Compatibility

### Δ144 Integration
- ✅ Output format: `{vector_id: score}`
- ✅ Scores always in [-1, 1]
- ✅ Compatible with all Δ144 bridges

### TW369 Integration
- ✅ Scores feed into plane tensions
- ✅ Works with all drift models (A, B, C, D)
- ✅ Compatible with Adaptive Mapping

### Existing Pipeline
- ✅ Drop-in replacement for LLM/rule-based
- ✅ No changes to downstream components
- ✅ Maintains same JSON structure

## 8. Alpha Selection Guide

### Conservative Approach
```json
{
  "alpha_global": 0.3,
  "alpha_layers": {
    "1": 0.4,
    "2": 0.3,
    "3": 0.2
  }
}
```
**Use when**: High-stakes domains, regulatory requirements

### Balanced Approach
```json
{
  "alpha_global": 0.5,
  "alpha_layers": {
    "1": 0.5,
    "2": 0.5,
    "3": 0.5
  }
}
```
**Use when**: General purpose, A/B testing

### Aggressive Approach
```json
{
  "alpha_global": 0.8,
  "alpha_layers": {
    "1": 0.9,
    "2": 0.8,
    "3": 0.7
  }
}
```
**Use when**: Experimental domains, high LLM confidence

## 9. Testing

Run the test suite:

```bash
pytest tests/kindras/test_hybrid_scorer.py -v
```

Tests verify:
- Global alpha mixing
- Layer-specific alpha override
- Score clamping to [-1, 1]
- Multiple vector handling
- Extreme value handling

## 10. Examples

### Example 1: Equal Mix (alpha=0.5)

**Input**:
```python
llm_scores = {"E01": 0.8, "T25": 0.6}
rule_scores = {"E01": -0.2, "T25": 0.2}
alpha = 0.5
```

**Output**:
```python
{
    "E01": 0.3,   # 0.5 * 0.8 + 0.5 * (-0.2)
    "T25": 0.4    # 0.5 * 0.6 + 0.5 * 0.2
}
```

### Example 2: LLM-Heavy (alpha=0.8)

**Input**:
```python
llm_scores = {"E01": 0.9}
rule_scores = {"E01": -0.5}
alpha = 0.8
```

**Output**:
```python
{
    "E01": 0.62   # 0.8 * 0.9 + 0.2 * (-0.5)
}
```

### Example 3: Rule-Heavy (alpha=0.2)

**Input**:
```python
llm_scores = {"E01": 0.7}
rule_scores = {"E01": -0.3}
alpha = 0.2
```

**Output**:
```python
{
    "E01": -0.1   # 0.2 * 0.7 + 0.8 * (-0.3)
}
```

## 11. Performance Considerations

- **Latency**: Sum of LLM + rule-based latency
- **Caching**: Cache both LLM and rule scores
- **Fallback**: If LLM fails, alpha automatically becomes 0
- **Determinism**: Deterministic given same inputs

## 12. Future Enhancements

1. **Dynamic Alpha**: Adjust alpha based on confidence
2. **Context-Aware Alpha**: Alpha based on domain/sector
3. **Learned Alpha**: ML-based alpha optimization
4. **Weighted Mixing**: Non-linear mixing functions
5. **Multi-Model**: Mix more than 2 scorers

## 13. References

- Hybrid Scorer Implementation: `src/kindras/kindra_hybrid_scorer.py`
- Configuration Schema: `schema/kindras/kindra_hybrid_config.json`
- Dispatcher Integration: `src/kindras/scoring_dispatcher.py`
- Tests: `tests/kindras/test_hybrid_scorer.py`
- LLM Scoring: `docs/KINDRA_LLM_SCORING.md`
