# LLM SCORING API DESIGN

## 1. Purpose

This document defines the internal API for LLM-based Kindra scoring.

The goal is to provide a stable contract between:
- KALDRA Core (Kindra, TW369, Δ144), and
- any scoring backend (rule-based, real LLM, hybrid).

## 2. Core Types

Implemented in:
- `src/kindras/scoring/llm_types.py`
- `src/kindras/scoring/llm_client_base.py`

### LLMScoringRequest

Fields:
- `layer`: Kindra layer (1, 2, 3)
- `text`: raw input text
- `context`: metadata (country, sector, channel, sentiment, etc.)
- `mode`: prompt/strategy identifier
- `max_vectors`: optional limit for number of vectors

### LLMScoringResponse

Fields:
- `scores`: `{vector_id: score}` in [-1.0, 1.0]
- `metadata`: `{model, prompt_version, backend, latency_ms, ...}`
- `error`: optional error message

## 3. LLMScoringClient Protocol

Any backend that wants to implement LLM-based scoring must implement:

```python
class LLMScoringClient(Protocol):
    def score(self, request: LLMScoringRequest) -> LLMScoringResponse:
        ...
```

This hides the details of the provider (OpenAI, other) from KALDRA Core.

## 4. Dummy Implementation (Rule-Backed)

`DummyLLMScoringClient`:
- Uses the existing rule-based Kindra scoring engine
- Ignores `text` for now
- Respects the API contract
- Clamps all scores to [-1.0, 1.0]
- Used for local development and testing

## 5. High-Level Services

### LLMScoringService

Location: `src/kindras/scoring/llm_scoring_service.py`

Provides:
- `score_layer(layer, text, context, mode, max_vectors)`
- `score_all_layers(text, context, mode_prefix, max_vectors_per_layer)`

### LLMToTWStateService

Location: `src/kindras/scoring/llm_twstate_service.py`

Provides:
- `build_twstate_from_text(text, context, max_vectors_per_layer)`

This method:
- calls `score_all_layers`
- maps layer 1/2/3 into TWState planes 3/6/9
- attaches metadata about scoring

## 6. Usage Examples

### Basic Scoring

```python
from src.kindras.scoring.llm_scoring_service import LLMScoringService

service = LLMScoringService()
response = service.score_layer(
    layer=1,
    text="Tech company narrative from Brazil.",
    context={"country": "BR", "sector": "tech"},
    mode="kindra_layer1_v1"
)

print(response.scores)  # {'E01': 0.6, 'P17': -0.2, ...}
print(response.metadata)  # {'backend': 'dummy_rule_based', ...}
```

### Text to TWState

```python
from src.kindras.scoring.llm_twstate_service import LLMToTWStateService

service = LLMToTWStateService()
tw_state = service.build_twstate_from_text(
    text="Earnings call with regulatory uncertainty.",
    context={
        "country": "US",
        "sector": "energy",
        "media_tone": "analytical",
        "institutional_strength": 0.7,
        "power_concentration": 0.6,
        "regulatory_stability": 0.5
    }
)

# Ready for TW369 engine
print(tw_state.plane3_cultural_macro)  # Layer 1 scores
print(tw_state.plane6_semiotic_media)  # Layer 2 scores
print(tw_state.plane9_structural_systemic)  # Layer 3 scores
```

## 7. Future: Real LLM Integration (Option B / C)

In future sprints:

### Option B: Real LLM Client

Implement `RealLLMScoringClient(LLMScoringClient)` that:
- Builds prompts from `text + context`
- Calls an external LLM provider (OpenAI, Anthropic, etc.)
- Parses scores and returns `LLMScoringResponse`

### Option C: Hybrid Client

Implement `HybridScoringClient` that:
- Combines Cultural Database, LLM, and Rule-based fallback
- Still exposes the same API: `score(request: LLMScoringRequest) -> LLMScoringResponse`

### Key Benefit

The KALDRA Core should never need to change:
it will only call the internal API.

## 8. Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│         KALDRA Core Pipeline                    │
│  (Kindra, TW369, Δ144 - unchanged)             │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│      LLMScoringService                          │
│      LLMToTWStateService                        │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│      LLMScoringClient (Protocol)                │
│                                                 │
│  ┌──────────────┐  ┌──────────────┐           │
│  │ Dummy Client │  │ Real LLM     │           │
│  │ (Rule-based) │  │ Client       │           │
│  └──────────────┘  └──────────────┘           │
│                                                 │
│  ┌──────────────┐                              │
│  │ Hybrid       │                              │
│  │ Client       │                              │
│  └──────────────┘                              │
└─────────────────────────────────────────────────┘
```

## 9. Testing

All implementations must pass the same test suite:

```bash
pytest tests/core/test_llm_dummy_scoring_client.py \
       tests/core/test_llm_scoring_service.py \
       tests/integration/test_llm_to_twstate_service.py -v
```

Current status: ✅ 7/7 tests passing

## 10. Benefits

1. **Decoupling**: KALDRA Core doesn't depend on any specific LLM provider
2. **Testability**: Dummy client allows full end-to-end testing without external APIs
3. **Flexibility**: Easy to swap implementations (rule-based → LLM → hybrid)
4. **Consistency**: All implementations return the same data structure
5. **Safety**: All scores guaranteed to be clamped to [-1.0, 1.0]
