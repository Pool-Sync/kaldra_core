# Kindra Scoring Overview

This document provides an overview of the three scoring options available in the Kindra Engine: Rule-Based (Option A), LLM-Based (Option B), and Hybrid (Option C).

## 1. Option A: Rule-Based Scoring

**Status**: Implemented
**Objective**: Deterministic, keyword-based scoring.

### Mechanism
- Uses dictionaries of keywords and patterns for each of the 48 vectors.
- Calculates scores based on frequency and intensity of matches.
- **Pros**: Fast, deterministic, explainable.
- **Cons**: Lacks context awareness, brittle to nuance.

### Usage
```python
dispatcher = KindraScoringDispatcher(scoring_mode="rule_based")
```

## 2. Option B: LLM-Based Scoring

**Status**: Implemented
**Objective**: Context-aware scoring using Large Language Models.

### Mechanism
- Sends text + context + vector definitions to an LLM.
- LLM returns scores for all vectors in `[-1, 1]`.
- **Pros**: Highly context-aware, handles nuance and subtext.
- **Cons**: Slower, nondeterministic (unless temperature=0), requires API key.

### Usage
```python
dispatcher = KindraScoringDispatcher(
    llm_client=client,
    scoring_mode="llm"
)
```

## 3. Option C: Hybrid Scoring

**Status**: Implemented
**Objective**: Combine the stability of rules with the nuance of LLMs.

### Mechanism
- Calculates both Rule-Based and LLM scores.
- Mixes them using a configurable alpha parameter:
  `score = clamp(alpha * LLM + (1-alpha) * Rule)`
- **Pros**: Balanced approach, tunable, robust fallback.

### Configuration (`schema/kindras/kindra_hybrid_config.json`)
- `alpha_global`: Default mixing ratio (0.0 to 1.0).
- `alpha_layers`: Overrides for specific layers (L1, L2, L3).

### Usage
```python
dispatcher = KindraScoringDispatcher(
    llm_client=client,
    scoring_mode="hybrid",
    hybrid_config={"alpha_global": 0.5}
)
```

## 4. Fallback Logic

The system is designed to be robust.

1.  **Hybrid Mode**: If LLM fails, `alpha` effectively becomes 0 (pure Rule-Based).
2.  **LLM Mode**: If LLM fails, falls back to Rule-Based.
3.  **Rule-Based Mode**: Always available.

## 5. Pipeline Integration

```ascii
Input Text
    |
    v
[Scoring Dispatcher]
    |
    +---> [LLM Scorer] --+
    |                    |
    +---> [Rule Scorer] -+--> [Hybrid Mixer] -> [Final Scores]
                                                     |
                                                     v
                                             [TW369 & Δ144]
```

## 6. Future Implementations

*   **Fine-Tuned LLM**: Replacing generic models (e.g., GPT-4) with a fine-tuned Llama 3 model specialized in Kindra vectors.
*   **Vector Embeddings**: Using semantic similarity (cosine distance) between input text and vector definitions as a third scoring signal.
*   **Batch Scoring**: Optimizing the LLM scorer to handle batches of inputs in a single API call.
*   **Confidence Scoring**: Returning a confidence interval for each score, not just a point estimate.

## 7. Enhancements (Short/Medium Term)

*   **Prompt Engineering**: Iterating on the few-shot examples in `kindra_llm_prompt.json` to reduce hallucinations.
*   **Caching**: Implementing a Redis cache for LLM responses to save costs on repeated inputs.
*   **Alpha Decay**: Automatically reducing `alpha` (trust in LLM) if the LLM's latency spikes.
*   **Explainability**: Asking the LLM to output a short "reasoning" string alongside the score.

## 8. Research Track (Long Term)

*   **Multi-Agent Debate**: Using two LLMs (one arguing for high score, one for low) to reach a more robust conclusion.
*   **Active Learning**: A loop where human experts review low-confidence scores to retrain the system.
*   **Neuromorphic Scoring**: Exploring Spiking Neural Networks for ultra-low-power scoring on edge devices.
*   **Quantum Scoring**: Theoretical exploration of using quantum states to represent vector superposition.

## 9. Known Limitations

*   **Cost**: LLM scoring is expensive at scale compared to rule-based.
*   **Latency**: LLM calls add significant latency (hundreds of ms) to the pipeline.
*   **Hallucination**: LLMs can sometimes invent justifications for scores that don't exist in the text.
*   **Drift**: The underlying LLM behavior may change over time (model updates), affecting score consistency.
