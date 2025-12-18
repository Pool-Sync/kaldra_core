# Kindra Scoring Overview

This document provides a comprehensive overview of the scoring mechanisms within the **Kindra Engine v2.2**.

## 1. Scoring Engines

Kindra v2.2 supports three distinct scoring engines, configurable via `schema/kindras/kindra_config.json`.

### 1.1. Option A: Rule-Based (Deterministic)
*   **Logic**: Uses keyword dictionaries and regex patterns to score vectors.
*   **Pros**: Fast, deterministic, free, easy to debug.
*   **Cons**: Lacks nuance, misses context, requires manual dictionary maintenance.
*   **Use Case**: High-throughput streams, initial baseline, fallback.

### 1.2. Option B: LLM-Based (Contextual)
*   **Logic**: Sends text + context + vector definitions to an LLM (e.g., GPT-4).
*   **Pros**: Highly nuanced, understands irony/sarcasm, zero-shot capability.
*   **Cons**: Slow (latency), expensive (API costs), non-deterministic.
*   **Use Case**: Deep analysis, low-volume high-value content.

### 1.3. Option C: Hybrid (Best of Both)
*   **Logic**: Computes a weighted average of Rule-Based and LLM scores.
*   **Formula**: `Final = alpha * LLM + (1 - alpha) * Rule`
*   **Pros**: Balances speed/cost with accuracy.
*   **Cons**: Complexity in tuning `alpha`.
*   **Use Case**: Production default.

## 2. Pipeline Flow

```ascii
[INPUT TEXT]
     |
     v
+----------------+
| Dispatcher     |
+----------------+
     |
     +---> [Rule Scorer] --+
     |                     |
     +---> [LLM Scorer] ---+
                           |
                           v
                    +--------------+
                    | Hybrid Mixer |
                    +--------------+
                           |
                           v
                    [FINAL SCORES]
```

## 3. Configuration

Configuration is managed in `schema/kindras/kindra_config.json`.

```json
{
  "scoring_mode": "hybrid",
  "hybrid_config": {
    "default_alpha": 0.7,
    "layer_overrides": {
      "1": 0.8,  // Trust LLM more for Macro
      "2": 0.6,
      "3": 0.5   // Trust Rules more for Structure
    }
  }
}
```

## 4. Fallback Modes

The system is designed for resilience.

1.  **Primary**: Attempt configured mode (e.g., Hybrid).
2.  **LLM Failure**: If LLM API fails or times out:
    *   Log error.
    *   **Fallback**: Switch to **Rule-Based** instantly.
    *   Alert: "Downgraded to Rule-Based due to LLM outage."
3.  **Rule Failure**: If dictionaries are missing (catastrophic):
    *   Return neutral scores (0.0).

## 5. Future Implementations

*   **Fine-Tuned LLM**: Replacing generic models (e.g., GPT-4) with a fine-tuned Llama 3 model specialized in Kindra vectors.
*   **Vector Embeddings**: Using semantic similarity (cosine distance) between input text and vector definitions as a third scoring signal.
*   **Batch Scoring**: Optimizing the LLM scorer to handle batches of inputs in a single API call.
*   **Confidence Scoring**: Returning a confidence interval for each score, not just a point estimate.

## 6. Enhancements (Short/Medium Term)

*   **Prompt Engineering**: Iterating on the few-shot examples in `kindra_llm_prompt.json` to reduce hallucinations.
*   **Caching**: Implementing a Redis cache for LLM responses to save costs on repeated inputs.
*   **Alpha Decay**: Automatically reducing `alpha` (trust in LLM) if the LLM's latency spikes.
*   **Explainability**: Asking the LLM to output a short "reasoning" string alongside the score.

## 7. Research Track (Long Term)

*   **Multi-Agent Debate**: Using two LLMs (one arguing for high score, one for low) to reach a more robust conclusion.
*   **Active Learning**: A loop where human experts review low-confidence scores to retrain the system.
*   **Neuromorphic Scoring**: Exploring Spiking Neural Networks for ultra-low-power scoring on edge devices.
*   **Quantum Scoring**: Theoretical exploration of using quantum states to represent vector superposition.

## 8. Known Limitations

*   **Cost**: LLM scoring is expensive at scale compared to rule-based.
*   **Latency**: LLM calls add significant latency (hundreds of ms) to the pipeline.
*   **Hallucination**: LLMs can sometimes invent justifications for scores that don't exist in the text.
*   **Drift**: The underlying LLM behavior may change over time (model updates), affecting score consistency.
