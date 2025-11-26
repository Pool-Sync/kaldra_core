# Legacy Migration Guide - Kindra Engine v2.2

## Overview

This document guides developers in migrating from the legacy Kindra implementation (v1.x/v2.0) to the new **Kindra Engine v2.2** architecture.

> [!WARNING]
> The legacy files located in `src/kindras/legacy/` are deprecated and will be removed in v3.0.

## What Changed?

The monolithic `scoring.py` and static `vectors.json` have been replaced by a modular, multi-engine architecture.

| Feature | Legacy (v2.0) | New (v2.2) |
|---------|---------------|------------|
| **Vectors** | `src/kindras/vectors.json` (Partial) | `schema/kindras/vectors.json` (Full 48) |
| **Scoring** | `src/kindras/scoring.py` (Cosine) | **3 Engines**: Rule-Based, LLM, Hybrid |
| **Logic** | Hardcoded Python | Configurable JSON Schemas |
| **Drift** | None | TW369 Integration |

## Migration Steps

### 1. Migrating Vector Definitions

**Old Location**: `src/kindras/vectors.json`
**New Location**: `schema/kindras/vectors.json`

The new schema uses a stricter format. If you added custom vectors to the old file, you must migrate them to the new schema format:

```json
{
  "id": "CUST01",
  "name": "My Custom Vector",
  "layer": 1,
  "polarity": "Positive/Negative",
  "description": "..."
}
```

### 2. Migrating Scoring Logic

**Old Code**:
```python
from src.kindras.scoring import cosine_similarity
score = cosine_similarity(vec_a, vec_b)
```

**New Code (Rule-Based)**:
```python
from src.kindras.scoring_dispatcher import KindraScoringDispatcher
dispatcher = KindraScoringDispatcher(mode="rule_based")
scores = dispatcher.run_all(context, vectors)
```

**New Code (LLM/Hybrid)**:
```python
dispatcher = KindraScoringDispatcher(mode="hybrid", llm_client=client)
scores = dispatcher.run_all(context, vectors)
```

### 3. Pipeline Adaptation

If your pipeline relied on `scoring.py`, replace the import with `src/kindras/scoring_dispatcher.py`. The `KindraScoringDispatcher` is the new single point of entry for all scoring operations.

## Future Implementations

*   **Automated Migration Script**: A script to parse old `vectors.json` and convert it to the new schema format.
*   **Legacy Shim**: A wrapper around the new dispatcher that mimics the old `cosine_similarity` function signature for temporary compatibility.

## Enhancements (Short/Medium Term)

*   **Deprecation Warnings**: Adding runtime warnings (via `warnings` module) if legacy modules are imported.
*   **Static Analysis**: Adding a pre-commit hook to block commits that import from `src/kindras/legacy/`.

## Research Track (Long Term)

*   **CodeMod**: Using AST transformation tools to automatically refactor client codebases to use the new API.

## Known Limitations

*   **Breaking Change**: The new scoring output format is a dictionary of scores `{ID: float}`, whereas the old one might have returned raw cosine values.
*   **Performance**: The new dispatcher has a slight overhead compared to the raw numpy function in the legacy module.
