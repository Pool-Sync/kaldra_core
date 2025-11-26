# TW369 Adaptive State-Plane Mapping

This document details the **Adaptive State-Plane Mapping** system, which dynamically adjusts the influence of the three TW369 planes (3, 6, 9) on the final Δ144 state based on context.

## 1. Concept

In a static system, Plane 3 might always contribute 33% to the final decision. In KALDRA v2.2, this contribution is dynamic.

**Why?**
In a "War" context, **Plane 3 (Action)** should matter more than **Plane 9 (Metanoia)**.
In a "Financial Crisis" context, **Plane 6 (Structure)** should be the dominant factor.

## 2. Fixed vs. Adaptive

### 2.1. Fixed Mapping (Baseline)
Defined in `schema/tw369/tw369_adaptive_mapping.json` under `default`.
*   Plane 3: 1.0
*   Plane 6: 1.0
*   Plane 9: 1.0

### 2.2. Adaptive Mapping
Overrides the baseline weights based on the input `context`.

## 3. Rules and Logic

The mapping engine evaluates the `context` object against a set of rules.

### 3.1. Domain Rules
*   **Domain: ALPHA (Finance)**
    *   Boost **Plane 6 (Structure)** by 1.5x.
    *   Suppress **Plane 9 (Metanoia)** by 0.8x.
    *   *Rationale*: Finance requires stability and structure; transcendence is less relevant.

*   **Domain: GEO (Geopolitics)**
    *   Boost **Plane 3 (Action)** by 1.4x.
    *   Boost **Plane 6 (Structure)** by 1.2x.
    *   *Rationale*: Geopolitics is driven by action and power structures.

*   **Domain: PRODUCT (Innovation)**
    *   Boost **Plane 3 (Action)** by 1.3x.
    *   Boost **Plane 9 (Metanoia)** by 1.4x.
    *   *Rationale*: Innovation requires action and transformative thinking.

### 3.2. Severity Rules
*   **Severity: HIGH / CRITICAL**
    *   Boost **Plane 6 (Structure)** by 2.0x.
    *   *Rationale*: In a crisis, the system naturally seeks stability and order (Contractive states).

## 4. Dumping and Feedback

### 4.1. Tension Dumping
If a plane's tension exceeds a critical threshold (e.g., > 0.9), the system may "dump" this energy into another plane to prevent collapse.
*   **Excess Plane 3 -> Plane 6**: Action solidifies into Structure.
*   **Excess Plane 6 -> Plane 9**: Structure collapses into Metanoia.
*   **Excess Plane 9 -> Plane 3**: Metanoia inspires new Action.

### 4.2. Drift Feedback
High drift values can trigger a global "dampening" of all plane weights to simulate system hesitation or confusion.

## 5. Δ144 Influence

The final weights determine which group of Δ144 states is most likely to be selected.

*   **High Plane 3 Weight** -> Favors **Expansive** states (Hero, Creator, Rebel).
*   **High Plane 6 Weight** -> Favors **Contractive** states (Ruler, Guardian, Orphan).
*   **High Plane 9 Weight** -> Favors **Transcendent** states (Sage, Magician, Jester).

## 6. Future Implementations

*   **Learned Weights**: Using Reinforcement Learning to optimize the weights based on user feedback (e.g., "This state was wrong").
*   **Temporal Adaptation**: Adjusting weights based on the *time of day* or *market session* (e.g., higher volatility tolerance at market open).
*   **User Personalization**: Allowing users to define their own weight profiles (e.g., "I care more about structural risks").
*   **Narrative Arc Mapping**: Changing weights automatically as a story progresses (Beginning = P3, Middle = P6, End = P9).

## 7. Enhancements (Short/Medium Term)

*   **Visual Config Editor**: A UI tool to adjust weights and see the effect on state probability in real-time.
*   **Rule Engine Upgrade**: Moving from simple `if/else` logic to a proper rule engine (e.g., generic JSON logic).
*   **Weight Normalization**: Ensuring that the sum of weights always equals a constant to prevent energy inflation.
*   **Context Expansion**: Supporting more granular context keys (e.g., "sub-sector", "author_intent").

## 8. Research Track (Long Term)

*   **Dynamic Topology**: Instead of just weighting planes, actually warping the geometry of the state space.
*   **Quantum Probability**: Using quantum amplitudes instead of scalar weights to model interference patterns between planes.
*   **Semantic Weighting**: Using LLMs to determine the "semantic weight" of a context on the fly, without hardcoded rules.
*   **Game Theory**: Modeling the planes as agents in a game, competing for dominance.

## 9. Known Limitations

*   **Rule Complexity**: As rules multiply, interactions can become unpredictable.
*   **Binary Context**: Current logic often treats context as binary (is_crisis vs not_crisis), missing nuance.
*   **Manual Tuning**: The weights currently require manual tuning by domain experts.
*   **Overfitting**: There is a risk of overfitting the weights to specific test cases.
