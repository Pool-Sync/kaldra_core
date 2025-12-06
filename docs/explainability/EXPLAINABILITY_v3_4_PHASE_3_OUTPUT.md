# Explainability v3.4 Phase 3 - Multi-Format Output

**Status:** ✅ IMPLEMENTED  
**Version:** KALDRA v3.4 Phase 3  
**Date:** December 2025

---

## Overview

Phase 3 adds **multi-format output** to KALDRA explainability, enabling explanations to be consumed in Markdown, GraphQL, and Protobuf formats.

**Key Features:**
- Markdown rendering for human-readable reports
- GraphQL types for future API integration
- Protobuf schema for binary serialization

---

## Markdown Output

### Usage

```python
from src.explainability.explanation_generator import ExplanationGenerator

generator = ExplanationGenerator()
explanation = generator.generate(context)

# Render to markdown
markdown = explanation.to_markdown()  # Default variant
compact_md = explanation.to_markdown(variant="compact")

print(markdown)
```

### Templates

Two variants available:
- `default`: Full explanation with all sections
- `compact`: Summary + key points only

**Custom templates:** Pass custom renderer with templates dict.

---

## GraphQL Types

### Types Defined

```python
ComponentConfidenceType
DecisionStepType
ExplanationConfidenceType
ExplanationType
```

### Adapter

```python
from src.api.graphql.resolvers.explainability_resolvers import explanation_to_graphql

graphql_data = explanation_to_graphql(explanation)
# Returns dict compatible with GraphQL types
```

**Note:** Requires `graph ene` library for production use. Backend-only, not exposed in API yet.

---

## Protobuf Support

### Schema

Located at: `proto/explainability/explanation.proto`

**Messages:**
- `ComponentConfidence`
- `DecisionStep`
- `ExplanationConfidence`
- `Explanation`

### Adapters

```python
from src.explainability.proto.explanation_adapters import (
    explanation_to_proto,
    explanation_from_proto
)

# Convert to protobuf
proto_msg = explanation_to_proto(explanation)

# Convert back
explanation_dict = explanation_from_proto(proto_msg)
```

**Note:** Uses mock messages for testing. Generate real stubs via `protoc` for production.

---

## Testing

**Results:** 6 passed, 3 skipped (28/31 total including P1/P2)

```bash
# Markdown tests
PYTHONPATH=. pytest tests/explainability/test_explanation_output_markdown.py -v

# GraphQL tests (skip if graphene not installed)
PYTHONPATH=. pytest tests/explainability/test_explanation_output_graphql.py -v

# Protobuf tests
PYTHONPATH=. pytest tests/explainability/test_explanation_output_protobuf.py -v
```

---

## Limitations

- GraphQL requires `graphene` library (optional dependency)
- Protobuf uses mock messages without `protoc` compilation
- Backend-only (not exposed via REST API yet)
- Markdown templates are basic (extensible)

---

## Related Documentation

- [Phase 1: NL Explanations](file:///Users/niki/Desktop/kaldra_core/docs/explainability/EXPLAINABILITY_v3_4_PHASE_1.md)
- [Phase 2: Confidence & Tracing](file:///Users/niki/Desktop/kaldra_core/docs/explainability/EXPLAINABILITY_v3_4_PHASE_2_CONFIDENCE.md)
