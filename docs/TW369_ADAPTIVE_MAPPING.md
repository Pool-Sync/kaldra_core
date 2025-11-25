# Adaptive State-Plane Mapping

This document describes the **Adaptive State-Plane Mapping** system, which dynamically adjusts the influence of TW369 planes on Δ144 states based on context.

## 1. Rationale

In a static system, Plane 6 (Structure) might always contribute 50% to the score of a "Ruler" state. However, in a "Crisis" context, Structure becomes more critical. Adaptive Mapping allows the system to recognize this context and boost the influence of Plane 6 to, say, 80%.

## 2. Mechanism

The system uses a set of rules defined in `schema/tw369/tw369_adaptive_mapping.json`.

### 2.1. Triggers
Triggers are conditions based on the input context.
- **Sector**: e.g., "Finance", "Tech".
- **Region**: e.g., "LATAM", "APAC".
- **Mode**: e.g., "Crisis", "Growth".

### 2.2. Weights
When a trigger is active, it applies a set of weight multipliers to the planes.
- `plane_3_weight`: Multiplier for Action plane.
- `plane_6_weight`: Multiplier for Structure plane.
- `plane_9_weight`: Multiplier for Metanoia plane.

## 3. Example

### Scenario: Financial Crisis

**Context**: `{"sector": "Finance", "mode": "Crisis"}`

**Rule**:
```json
{
  "trigger": {"mode": "Crisis"},
  "weights": {
    "plane_3": 0.5,  // Reduce Action (too risky)
    "plane_6": 1.5,  // Boost Structure (stability needed)
    "plane_9": 1.0   // Neutral
  }
}
```

**Effect**:
- States heavily reliant on Plane 6 (e.g., `Ruler`, `Guardian`) receive a score boost.
- States heavily reliant on Plane 3 (e.g., `Warrior`, `Hero`) receive a score penalty.
- The system naturally drifts towards "Protective/Structural" states.

## 4. Interaction with Drift

Adaptive Mapping also influences how drift is interpreted.
- In a **High Structure** context (boosted Plane 6), drift in Plane 6 is penalized more severely than drift in Plane 3.
- This ensures that the system is sensitive to the *relevant* instabilities for the current context.

## 5. Configuration

Adaptive Mapping can be enabled/disabled in `schema/tw369/tw369_config_schema.json`.

```json
{
  "adaptive_mapping_enabled": true
}
```

## 6. Future Implementations

*   **Hierarchical Triggers**: Supporting nested triggers (e.g., "Finance" -> "Crypto" -> "Crash") with inheritance.
*   **Temporal Triggers**: Rules that activate based on time (e.g., "Election Year" boosts Plane 3).
*   **User-Defined Rules**: API endpoint for users to upload custom mapping rules at runtime.
*   **Conflict Resolution**: Advanced logic for handling multiple conflicting triggers (currently simple averaging).

## 7. Enhancements (Short/Medium Term)

*   **Fuzzy Matching**: Allowing triggers to match based on semantic similarity (e.g., "Downturn" matches "Crisis").
*   **Weight Normalization**: Automatically normalizing weights to ensure total energy remains constant.
*   **Rule Visualization**: Generating a graph of active rules and their net effect on plane weights.
*   **Simulation Mode**: Testing how different contexts would affect the outcome of a specific input.

## 8. Research Track (Long Term)

*   **Contextual Embeddings**: Using vector embeddings of the context to generate weights dynamically (no hardcoded rules).
*   **Meta-Learning**: The system learning new mapping rules by observing user feedback on state accuracy.
*   **Causal Mapping**: Inferring the causal link between context and plane dynamics (e.g., *why* does Crisis boost Structure?).
*   **Dynamic Topology**: Changing not just the weights but the *connections* between planes based on context.

## 9. Known Limitations

*   **Binary Triggers**: Triggers are currently boolean (on/off); no support for "partial" activation (e.g., 0.7 Crisis).
*   **Manual Tuning**: The weights in `tw369_adaptive_mapping.json` must be manually tuned by experts.
*   **Complexity**: As the number of rules grows, predicting the system's behavior becomes increasingly difficult.
*   **Static Context**: The context dictionary is assumed to be static for the duration of the request.
