# Kindra LLM-Based Scoring

## 1. Overview

The **Kindra LLM-Based Scoring** system replaces rule-based Kindra scoring with contextual LLM inference while maintaining full compatibility with Δ144, TW369, Adaptive Mapping, and Advanced Drift models.

## 2. Architecture

### Components

1. **KindraLLMScorer** (`src/kindras/kindra_llm_scorer.py`)
   - Main LLM scoring engine
   - Handles prompt construction
   - Parses and clamps LLM responses
   - Provides fallback to rule-based scoring

2. **Prompt System** (`src/kindras/prompts/kindra_llm_prompt.json`)
   - Few-shot examples
   - Scoring instructions
   - Output format specification

3. **Integration** (`src/kindras/scoring_dispatcher.py`)
   - Integrated into KindraScoringDispatcher
   - Configurable scoring mode (llm/rule_based)
   - Seamless fallback mechanism

## 3. How It Works

### Input
```python
{
    "text": "A empresa anunciou inovação agressiva...",
    "context": {
        "country": "BR",
        "sector": "Tech",
        "domain": "ALPHA",
        "channel": "news"
    },
    "vectors": {
        "E01": {...},
        "T25": {...},
        "P17": {...}
    }
}
```

### Process
1. **Prompt Construction**: Combines text, context, and vector definitions
2. **LLM Inference**: Sends prompt to LLM client
3. **Response Parsing**: Extracts scores from LLM response
4. **Clamping**: Ensures all scores ∈ [-1, 1]
5. **Fallback**: Uses rule-based scoring if LLM unavailable

### Output
```python
{
    "E01": 0.9,
    "T25": 0.8,
    "P17": -0.2
}
```

## 4. Usage

### Basic Usage

```python
from src.kindras.kindra_llm_scorer import KindraLLMScorer

# Initialize with LLM client
scorer = KindraLLMScorer(
    llm_client=my_llm_client,
    rule_fallback=my_rule_scorer
)

# Score text
scores = scorer.score(
    text="A empresa anunciou inovação agressiva...",
    context={"country": "BR", "sector": "Tech"},
    vectors={"E01": {}, "T25": {}, "P17": {}}
)

# scores = {"E01": 0.9, "T25": 0.8, "P17": -0.2}
```

### Integration with Dispatcher

```python
from src.kindras.scoring_dispatcher import KindraScoringDispatcher

# Initialize dispatcher with LLM
dispatcher = KindraScoringDispatcher(
    llm_client=my_llm_client,
    scoring_mode="llm"
)

# Run all layers (uses LLM scoring)
result = dispatcher.run_all(context, base_vectors)
```

### Fallback to Rule-Based

```python
# Without LLM client
dispatcher = KindraScoringDispatcher(
    llm_client=None,
    scoring_mode="rule_based"
)

# Automatically uses rule-based scoring
result = dispatcher.run_all(context, base_vectors)
```

## 5. Prompt Structure

The LLM prompt includes:

1. **Task Description**: "Score Kindra cultural vectors in [-1, 1]"
2. **Instructions**:
   - Return only numeric scores
   - Clamp results internally
   - Each score represents cultural resonance
   - Do not invent vector IDs
   - Output must be JSON

3. **Few-Shot Examples**:
   ```json
   {
     "context": {"country": "BR", "sector": "Tech"},
     "text": "A empresa anunciou inovação agressiva...",
     "expected_scores": {"E01": 0.9, "T25": 0.8, "P17": -0.2}
   }
   ```

4. **Current Input**: Text + context + vector list

## 6. Fallback Mechanism

The system provides multiple fallback layers:

1. **LLM Available**: Use LLM scoring
2. **LLM Unavailable**: Use rule-based fallback
3. **No Fallback**: Return zeros for all vectors

```python
# Fallback priority:
if llm_client is not None:
    try:
        return llm_scoring(text, context, vectors)
    except Exception:
        return rule_fallback.score(context, vectors)
else:
    if rule_fallback is not None:
        return rule_fallback.score(context, vectors)
    else:
        return {k: 0.0 for k in vectors.keys()}
```

## 7. Compatibility

### Δ144 Integration
- Output format: `{vector_id: score}`
- Scores always in [-1, 1]
- Compatible with all Δ144 bridges

### TW369 Integration
- Scores feed into plane tensions
- Works with all drift models (A, B, C, D)
- Compatible with Adaptive Mapping

### Existing Pipeline
- Drop-in replacement for rule-based scoring
- No changes to downstream components
- Maintains same JSON structure

## 8. Configuration

### Scoring Mode Selection

```python
# LLM mode (default)
dispatcher = KindraScoringDispatcher(
    llm_client=client,
    scoring_mode="llm"
)

# Rule-based mode
dispatcher = KindraScoringDispatcher(
    llm_client=None,
    scoring_mode="rule_based"
)
```

## 9. Testing

Run the test suite:

```bash
pytest tests/kindras/test_llm_scorer.py -v
```

Tests verify:
- Basic LLM scoring
- Score clamping to [-1, 1]
- Fallback when LLM unavailable
- Fallback on LLM errors
- Score parsing
- Output format compatibility

## 10. Examples

### Example 1: Tech Sector (Brazil)

**Input**:
```python
text = "A empresa anunciou inovação agressiva e discurso emocional alto."
context = {"country": "BR", "sector": "Tech"}
```

**Output**:
```python
{
    "E01": 0.9,   # High emotional resonance
    "T25": 0.8,   # Strong innovation signal
    "P17": -0.2   # Low conservatism
}
```

### Example 2: Finance Sector (US)

**Input**:
```python
text = "The bank announced conservative measures and risk mitigation strategies."
context = {"country": "US", "sector": "Finance"}
```

**Output**:
```python
{
    "E01": -0.3,  # Low emotional resonance
    "T25": -0.5,  # Low innovation signal
    "P17": 0.7    # High conservatism
}
```

## 11. Performance Considerations

- **LLM Latency**: Depends on LLM provider (typically 100-500ms)
- **Fallback Speed**: Rule-based fallback is instant
- **Caching**: Consider caching LLM responses for repeated inputs
- **Batch Processing**: Can batch multiple texts for efficiency

## 12. Future Enhancements

1. **Fine-tuning**: Train LLM specifically on Kindra vectors
2. **Multi-language**: Extend prompt for multiple languages
3. **Confidence Scores**: Return confidence alongside scores
4. **Explanation**: Generate explanations for scores
5. **Active Learning**: Improve prompts based on feedback

## 13. References

- Kindra Scoring Dispatcher: `src/kindras/scoring_dispatcher.py`
- LLM Scorer Implementation: `src/kindras/kindra_llm_scorer.py`
- Prompt Template: `src/kindras/prompts/kindra_llm_prompt.json`
- Tests: `tests/kindras/test_llm_scorer.py`
