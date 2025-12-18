# Kindra 3×48 Developer Guide

## Overview

The Kindra 3×48 system is KALDRA's cultural-narrative engine, providing 144 cultural vectors organized across three layers that modulate the Δ144 archetype distribution.

## Architecture

### Three-Layer Structure

```
Layer 1 (Cultural Macro)     → TW Plane 3 → Surface/Behavior
Layer 2 (Semiotic/Media)     → TW Plane 6 → Tension/Drift
Layer 3 (Structural/Systemic) → TW Plane 9 → Deep Structure
```

Each layer contains 48 vectors organized into 6 domains (8 vectors each):
- E01-E08: Expressive
- S09-S16: Social
- P17-P24: Power
- T25-T32: Temporal
- R33-R40: Risk
- M41-M48: Mythic

## Quick Start

### Basic Usage

```python
from core.kaldra_engine_pipeline import KALDRAEnginePipeline

# Initialize pipeline
pipeline = KALDRAEnginePipeline(schema_base_path="schema/kindras")

# Create base Δ144 distribution
base_delta144 = {f"STATE_{i:03d}": 1.0 for i in range(144)}

# Define context
context = {
    "country": "BR",
    "sector": "Tech",
    "layer1_overrides": {"E01": 0.8},  # High expressiveness
    "layer2_overrides": {"S09": 0.6},  # High media richness
    "layer3_overrides": {"P17": -0.3}  # Low power concentration
}

# Run pipeline
result = pipeline.process(base_delta144, context, evolve_steps=0)

# Access results
final_distribution = result["final_distribution"]
l1_scores = result["layer1_scores"]
intermediate = result["intermediate_distributions"]
```

## Component Reference

### Loaders

Load and validate Kindra vector data from JSON files.

```python
from kindras.layer1_cultural_macro_loader import Layer1Loader

loader = Layer1Loader("schema/kindras/kindra_vectors_layer1_cultural_macro_48.json")

# Get all vectors
all_vectors = loader.get_all_vectors()

# Get specific vector
vector = loader.get_vector("E01")

# Filter by domain
expressive_vectors = loader.get_by_domain("EXPRESSIVE")
```

### Scorers

Calculate vector intensities based on context.

```python
from kindras.layer1_cultural_macro_scoring import Layer1Scorer

scorer = Layer1Scorer()
scores = scorer.score(context, loader.get_all_vectors())
# Returns: {"E01": 0.8, "E02": 0.0, ...}
```

**Score Range**: -1.0 to 1.0
- Positive: Amplifies the vector's effect
- Negative: Inverts the vector's effect
- Zero: Neutral (no effect)

### Bridges

Apply Kindra scores to Δ144 distribution.

```python
from kindras.layer1_delta144_bridge import Layer1Delta144Bridge

bridge = Layer1Delta144Bridge("schema/kindras/kindra_layer1_to_delta144_map.json")
adjusted_dist = bridge.apply(base_distribution, kindra_scores)
```

**Logic**:
- If `score > 0`: Boost states in `boost` list, suppress states in `suppress` list
- If `score < 0`: Invert (boost `suppress` list, suppress `boost` list)
- Impact formula: `new_value = old_value * (1 ± score * impact_factor)`

**Impact Factors**:
- Layer 1: 0.2
- Layer 2: 0.25
- Layer 3: 0.3

### TW369 Integration

```python
from tw369.tw369_integration import TW369Integrator

integrator = TW369Integrator()

# Create TW state
tw_state = integrator.create_state(
    layer1_scores=l1_scores,
    layer2_scores=l2_scores,
    layer3_scores=l3_scores,
    metadata=context
)

# Evolve distribution over time
evolved = integrator.evolve(tw_state, distribution, time_steps=5)
```

## Data Files

### Vector Files
- `schema/kindras/kindra_vectors_layer1_cultural_macro_48.json`
- `schema/kindras/kindra_vectors_layer2_semiotic_media_48.json`
- `schema/kindras/kindra_vectors_layer3_structural_systemic_48.json`

### Mapping Files
- `schema/kindras/kindra_layer1_to_delta144_map.json`
- `schema/kindras/kindra_layer2_to_delta144_map.json`
- `schema/kindras/kindra_layer3_to_delta144_map.json`

## Testing

```bash
# Run all Kindra tests
pytest tests/kindras/ -v

# Run specific test files
pytest tests/kindras/test_loaders.py -v
pytest tests/kindras/test_scorers_bridges.py -v
pytest tests/core/test_pipeline.py -v
```

## Extending the System

### Adding New Vectors

1. Edit the appropriate layer JSON file
2. Add vector with required fields:
   - `id`, `layer`, `domain`, `tw_plane`
   - `scale_type`, `scale_direction`, `weight`
   - `short_name`, `objective_definition`, `examples`, `narrative_role`

### Customizing Scoring Logic

Override the `score()` method in scorer classes:

```python
class CustomLayer1Scorer(Layer1Scorer):
    def score(self, context, vectors):
        scores = super().score(context, vectors)
        
        # Custom logic here
        if context.get("country") == "BR":
            scores["E01"] *= 1.2  # Boost expressiveness for Brazil
        
        return scores
```

### Modifying Impact Factors

Edit the `IMPACT_FACTOR` constant in bridge files:

```python
# In layer1_delta144_bridge.py
IMPACT_FACTOR = 0.3  # Increase from 0.2 to 0.3
```

## Best Practices

1. **Always validate context**: Ensure context dictionaries contain expected keys
2. **Use overrides for testing**: Manual overrides are perfect for debugging
3. **Monitor intermediate distributions**: Use `result["intermediate_distributions"]` to debug
4. **Normalize scores**: Keep scores in [-1.0, 1.0] range for consistency
5. **Document custom logic**: Add comments when extending scorers or bridges

## Troubleshooting

### FileNotFoundError
- Verify `schema_base_path` is correct
- Ensure all JSON files exist in `schema/kindras/`

### Unexpected Distribution Values
- Check intermediate distributions to isolate which layer caused the issue
- Verify mapping files have correct state IDs
- Ensure scores are in valid range

### Import Errors
- Verify `src/` is in Python path
- Check all `__init__.py` files exist

## Next Steps

- Implement actual TW369 drift mathematics
- Populate mapping files with semantic relationships
- Develop AI-based scoring engines
- Create visualization tools for distributions
