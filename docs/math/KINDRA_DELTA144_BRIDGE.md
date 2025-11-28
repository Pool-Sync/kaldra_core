# Kindra-Δ144 Bridge Specification

This document details how the **Kindra Engine** (Cultural Vectors) communicates with and influences the **Δ144 Engine** (State Machine).

## 1. Rationale

The Kindra Engine provides granular, multi-layered analysis of the input text (48 vectors). The Δ144 Engine defines discrete states of the system (144 states). The Bridge translates continuous vector scores into discrete state activations (Boost/Suppress).

## 2. Mechanism

The bridge operates by mapping specific Kindra vectors (or combinations of vectors) to specific Δ144 states or state groups.

### 2.1. Activation Logic
- **Boost**: If a vector score is positive and high, it "boosts" associated states (increases their probability).
- **Suppress**: If a vector score is negative or low, it "suppresses" associated states (decreases their probability).

### 2.2. TW369 Influence
The bridge is modulated by the TW369 Engine.
- **Plane 3 Dominance**: Amplifies L2 (Semiotic) vector influence.
- **Plane 6 Dominance**: Amplifies L3 (Structural) vector influence.
- **Plane 9 Dominance**: Amplifies L1 (Macro) vector influence.

## 3. Layer Mappings

### 3.1. Layer 1 (Macro) -> Transcendent States
L1 vectors (e.g., `E14 Spiritual Seeking`, `E05 Innovation Drive`) map primarily to **Plane 9** and **Transcendent** Δ144 states (e.g., `Sage`, `Magician`).

| Kindra Vector | Δ144 Target Group | Effect |
|---------------|-------------------|--------|
| E14 (Seeking) | Sage_9_xx | Boost |
| E05 (Innovation)| Magician_9_xx | Boost |
| E02 (Anxiety) | Ruler_6_xx | Boost (Defensive) |

### 3.2. Layer 2 (Semiotic) -> Expansive States
L2 vectors (e.g., `S05 Viral Potential`, `S12 Hero Archetype`) map primarily to **Plane 3** and **Expansive** Δ144 states (e.g., `Hero`, `Creator`).

| Kindra Vector | Δ144 Target Group | Effect |
|---------------|-------------------|--------|
| S12 (Hero) | Hero_3_xx | Boost |
| S05 (Viral) | Jester_3_xx | Boost |
| S08 (Urgency) | Warrior_3_xx | Boost |

### 3.3. Layer 3 (Structural) -> Contractive States
L3 vectors (e.g., `T01 Hierarchical Power`, `T08 Boundary Rigidity`) map primarily to **Plane 6** and **Contractive** Δ144 states (e.g., `Ruler`, `Guardian`).

| Kindra Vector | Δ144 Target Group | Effect |
|---------------|-------------------|--------|
| T01 (Hierarchy) | Ruler_6_xx | Boost |
| T08 (Rigidity) | Guardian_6_xx | Boost |
| T03 (Fragility) | Orphan_6_xx | Boost |

## 4. Example Flow

1.  **Input**: "The market is crashing, we need to protect our assets."
2.  **Kindra Scores**:
    *   `E02 Collective Anxiety`: 0.9 (High)
    *   `T03 Systemic Fragility`: 0.8 (High)
    *   `S08 Urgency Framing`: 0.7 (High)
3.  **Bridge Logic**:
    *   `E02` -> Boosts `Ruler_6` (Order needed) and `Orphan_6` (Fear).
    *   `T03` -> Boosts `Orphan_6` (Vulnerability).
    *   `S08` -> Boosts `Warrior_3` (Action needed).
4.  **TW369 Modulation**:
    *   Context implies Crisis -> Plane 6 boosted.
    *   Bridge amplifies `Ruler_6` and `Orphan_6` signals.
5.  **Result**: Δ144 State `Guardian_6_05` (Protective Stance) or `Ruler_6_02` (Emergency Order).

## 5. Implementation

The bridge logic is implemented in `src/kindras/layerX_delta144_bridge.py` files.

## 6. Future Implementations

*   **Dynamic Bridge Weights**: Allowing the bridge to learn optimal weights from feedback (Reinforcement Learning).
*   **Negative Feedback Loops**: Implementing "Damping" where high Kindra scores suppress *opposite* states (e.g., High Trust suppresses Paranoia).
*   **Vector Bundling**: Mapping pre-defined clusters of vectors (e.g., "Revolutionary Bundle") to complex state transitions.
*   **Temporal Bridging**: Allowing past vector scores to influence current state probability (hysteresis).

## 7. Enhancements (Short/Medium Term)

*   **JSON-Based Mapping**: Moving hardcoded Python logic into `schema/bridge_mappings.json` for easier editing.
*   **Visualization**: Generating a Sankey diagram showing the flow of energy from Vectors -> Planes -> States.
*   **Debug Mode**: Detailed logging of *why* a specific state was boosted (traceability).
*   **Threshold Tuning**: Calibrating the activation thresholds for "Boost" vs. "Suppress" based on real-world data.

## 8. Research Track (Long Term)

*   **Neural Bridge**: Replacing the rule-based bridge with a small neural network trained on expert annotations.
*   **Semantic Resonance**: Using vector embeddings to find "hidden" connections between Kindra vectors and Δ144 state descriptions.
*   **Bridge Evolution**: Allowing the bridge to evolve its mappings over time as the cultural context shifts.
*   **Multi-Bridge Arbitration**: Using multiple bridge strategies and voting on the final state boost.

## 9. Known Limitations

*   **Hardcoded Logic**: Currently, much of the bridge logic is hardcoded in Python, making it hard to tweak without code changes.
*   **Linearity**: The bridge assumes a linear relationship between vector score and state boost, which may not always hold.
*   **Complexity**: The interaction between 48 vectors and 144 states creates a combinatorial explosion that is hard to fully test.
*   **Context Sensitivity**: The bridge is not yet fully context-aware (e.g., "Hero" might mean something different in Finance vs. Politics).
