# Explainability v3.4 Phase 1 - Natural Language Explanations

**Status:** ✅ IMPLEMENTED  
**Version:** KALDRA v3.4 Phase 1  
**Date:** December 2025  
**Component:** Explainability Layer

---

## Overview

Phase 1 of the KALDRA Explainability Layer introduces **natural language explanation generation** for KALDRA signals. This foundational capability enables the system to articulate *why* it reached certain conclusions, making KALDRA's analysis transparent and interpretable.

### Key Features

- **LLM-Powered Generation**: Optional integration with language models for rich explanations
- **Template-Based Fallback**: Deterministic explanation generation when LLM unavailable
- **Barebones Fallback**: Always-working minimal explanation as last resort
- **Modular Design**: Standalone module, ready for pipeline integration in Phase 2

### Importance in Explainable AI

Explainability is critical for:
- **Trust**: Users must understand how KALDRA reaches conclusions
- **Debugging**: Developers need insight into signal generation
- **Compliance**: Regulated industries require interpretability
- **Improvement**: Explanations reveal areas for enhancement

---

## Architecture

### Component Overview

```
ExplanationGenerator
    ├─ LLM Integration (optional)
    ├─ Template Engine
    ├─ Fact Extractor
    └─ Fallback Chain
```

### Data Flow

```
UnifiedContext
    ↓
Fact Extraction
    ├─ Delta144 state
    ├─ Polarities
    ├─ Journey stage
    ├─ Drift regime
    └─ Divergence metrics
    ↓
Generation (3-tier fallback)
    ├─ LLM → if available
    ├─ Template → if LLM fails
    └─ Barebones → always works
    ↓
Explanation
    ├─ summary: str
    ├─ details: Dict
    └─ raw_facts: Dict
```

---

## LLM Flow

### With LLM Available

1. **Extract Facts**: Pull relevant data from `UnifiedContext`
2. **Build Prompt**: Construct structured prompt with facts
3. **Call LLM**: Send to language model (e.g., OpenAI API)
4. **Parse Response**: Extract summary and details
5. **Return Explanation**: Wrap in `Explanation` object

### Example LLM Prompt

```
Generate a natural language explanation for the following KALDRA signal:

- Delta144 State: threshold
- Polarities: {"order": 0.65, "chaos": 0.35}
- Journey Stage: Call to Adventure
- Drift Regime: STABLE
- Divergence: N/A

Provide a concise summary and detailed breakdown.
```

---

## Templates

### Base Template Structure

Located at: `src/explainability/templates/base_template.md`

```markdown
# KALDRA Explanation Template

## Explanation Summary
{{summary}}

## Key Drivers
{{drivers}}

## Archetype Influence
{{archetypes}}

## Polarity Context
{{polarities}}

## Narrative Dynamics
{{narrative}}
```

### Template Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{{summary}}` | Generated from facts | High-level overview |
| `{{drivers}}` | Meta scores, divergence | Key contributing factors |
| `{{archetypes}}` | Delta12, Delta144 | Archetypal influences |
| `{{polarities}}` | Polarity scores | Polarity distribution |
| `{{narrative}}` | Journey, drift | Narrative context |

### Customization

To create custom templates:

1. Create new template file in `templates/`
2. Pass to `ExplanationGenerator`:

```python
generator = ExplanationGenerator(templates={"custom": custom_template})
```

---

## Fallback Logic

### Three-Tier Fallback Chain

```python
try:
    # Tier 1: LLM
    return llm.generate(prompt)
except:
    try:
        # Tier 2: Template
        return template.fill(facts)
    except:
        # Tier 3: Barebones
        return "The signal indicates notable narrative activity..."
```

### Mode: LLM

**When**: LLM is configured and available  
**Pros**: Rich, natural explanations  
**Cons**: Requires API, costs money, can fail

### Mode: Template

**When**: LLM fails or unavailable  
**Pros**: Deterministic, always consistent  
**Cons**: Less natural, template-restricted

### Mode: Barebones

**When**: Both LLM and template fail  
**Pros**: Never fails, minimal dependencies  
**Cons**: Very basic, minimal information

---

## Usage Examples

### Basic Usage (No LLM)

```python
from src.explainability.explanation_generator import ExplanationGenerator
from src.unification.states.unified_state import UnifiedContext

# Initialize generator (no LLM)
generator = ExplanationGenerator()

# Generate explanation
context = UnifiedContext(...)  # From pipeline
explanation = generator.generate(context)

# Access results
print(explanation.summary)
print(explanation.details["drivers"])
print(explanation.raw_facts)
```

### With LLM Integration

```python
# Mock LLM (replace with actual implementation)
class MyLLM:
    def generate(self, prompt):
        # Call OpenAI, Anthropic, etc.
        return {
            "summary": "Analysis shows...",
            "details": {...}
        }

# Initialize with LLM
generator = ExplanationGenerator(llm=MyLLM())
explanation = generator.generate(context)
```

### Custom Templates

```python
custom_template = """
## Analysis
{{summary}}

## Factors
{{drivers}}
"""

generator = ExplanationGenerator(templates={"custom": custom_template})
```

---

## Testing

### Test Coverage

**10 comprehensive tests** covering all scenarios:

1. ✅ Basic explanation generation
2. ✅ LLM usage (mocked)
3. ✅ LLM fallback on error
4. ✅ Template sections validation
5. ✅ Summary field presence
6. ✅ Archetype extraction
7. ✅ Polarity extraction
8. ✅ Journey stage extraction
9. ✅ Minimal context handling
10. ✅ Graceful degradation on invalid signal

### Running Tests

```bash
PYTHONPATH=/Users/niki/Desktop/kaldra_core pytest tests/explainability/test_explanation_generator.py -v
```

### Test Results

All tests pass with comprehensive coverage of:
- Generation modes (LLM, template, barebones)
- Fact extraction from all context types
- Error handling and graceful degradation
- Edge cases (empty context, malformed data)

---

## API Reference

### Explanation Class

```python
class Explanation:
    summary: str           # High-level explanation
    details: Dict[str, Any]  # Detailed breakdown
    raw_facts: Dict[str, Any]  # Extracted facts
    
    def to_dict() -> Dict[str, Any]
```

### ExplanationGenerator Class

```python
class ExplanationGenerator:
    def __init__(
        llm: Optional[Any] = None,
        templates: Optional[Dict[str, str]] = None
    )
    
    def generate(context: UnifiedContext) -> Explanation
```

**Methods:**
- `generate(context)`: Main entry point for explanation generation
- `_extract_facts(context)`: Extract relevant facts from context
- `_generate_with_llm(facts)`: LLM-based generation
- `_generate_with_template(facts)`: Template-based generation
- `_generate_barebones(facts)`: Minimal fallback

---

## Future Phases

### Phase 2: Confidence Breakdown

- Per-component confidence scores
- Uncertainty visualization
- Alternative interpretations

### Phase 3: Multi-Format Output

- JSON format for programmatic access
- Markdown for documentation
- HTML for web display
- Voice-friendly format for audio

### Phase 4: Interactive Explanations

- User Q&A ("Why did you say X?")
- Drill-down into specific components
- Counterfactual explanations ("What if...?")

---

## Limitations

### Current Phase (1)

- No pipeline integration yet (standalone only)
- No API exposure
- LLM integration is mock-ready but not implemented
- Single template only (base_template.md)
- No confidence scores
- English-only

### Design Constraints

- Requires `UnifiedContext` as input
- Fact extraction depends on context completeness
- Template fallback is static (not dynamic)

---

## Related Documentation

- [KALDRA v3.4 Roadmap](file:///Users/niki/Desktop/kaldra_core/docs/roadmaps/KALDRA_V3_4_EXPLAINABLE.md)
- [Multi-Stream Integration (v3.3)](file:///Users/niki/Desktop/kaldra_core/docs/multistream/MULTI_STREAM_INTEGRATION_v3_3_PHASE_3.md)
- [Story Engine (v3.2)](file:///Users/niki/Desktop/kaldra_core/docs/story/STORY_ENGINE_PRIMITIVES_v3_2.md)

---

## Summary

Explainability Phase 1 provides the **foundation for interpretable AI** in KALDRA:

✅ **Natural Language Generation**: LLM-powered explanations  
✅ **Robust Fallback**: Template and barebones modes  
✅ **Comprehensive Fact Extraction**: All context types supported  
✅ **Well-Tested**: 10/10 tests passing  
✅ **Standalone**: Ready for Phase 2 pipeline integration  
✅ **Extensible**: Easy to add custom templates and LLMs

Future phases will integrate this into the pipeline, add confidence breakdowns, and expand to multi-format output.
