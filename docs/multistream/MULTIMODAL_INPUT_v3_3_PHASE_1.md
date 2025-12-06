# Multi-Modal Input v3.3 Phase 1

## Overview

**Multi-Modal Input** is the first phase of the KALDRA v3.3 "Multi-Modal Layer". It enables the pipeline to ingest, normalize, and process diverse data types beyond raw text, including JSON, tables, and multi-stream inputs.

### Key Features

1.  **Rich Metadata**: `InputMetadata` tracks source, content type, timestamps, and extra fields.
2.  **Structured Data**: Native support for JSON and tables via `StructuredNormalizer`.
3.  **Multi-Source Support**: `UnifiedContext` can now hold multiple `InputContext` objects (`input_ctx_list`).
4.  **Ensemble Embeddings**: `EnsembleEmbedder` merges embeddings from different modalities.

---

## Architecture

### Data Structures

#### InputMetadata
```python
@dataclass
class InputMetadata:
    source: Optional[str] = None      # e.g., "twitter", "api"
    stream_id: Optional[str] = None   # Unique ID
    content_type: str = "text"        # "text", "json", "table"
    language: str = "en"
    timestamp: Optional[float] = None
    extra: Dict[str, Any] = ...
```

#### InputContext (Enhanced)
```python
@dataclass
class InputContext:
    text: str
    metadata: InputMetadata           # Strongly typed
    structured: Optional[Dict] = None # JSON/Table data
    # ... existing fields
```

### Ingestion Pipeline

1.  **Ingestion Modules** (`src/data/ingestion/`):
    - `APIIngest`: JSON → InputContext
    - `HTMLIngest`: HTML Tables → InputContext
    - `TextIngest`: Text (with JSON detection) → InputContext

2.  **Normalization** (`src/data/normalizer/`):
    - `StructuredNormalizer`: Standardizes JSON and tables.

3.  **Orchestration** (`src/unification/pipeline/`):
    - `PipelineOrchestrator`: Detects `input_ctx_list` and forks execution (stub implementation).

---

## Usage Examples

### 1. Ingesting JSON from API

```python
from src.data.ingestion.api_ingest import APIIngest

ingestor = APIIngest()
data = {"user": "alice", "action": "login"}
context = ingestor.ingest(data, source="auth_service")

print(context.metadata.content_type)  # "json"
print(context.structured)             # {'user': 'alice', ...}
```

### 2. Ingesting HTML Table

```python
from src.data.ingestion.html_ingest import HTMLIngest

ingestor = HTMLIngest()
rows = [{"id": 1, "val": 10}, {"id": 2, "val": 20}]
context = ingestor.ingest_table(rows, source="report_page")

print(context.metadata.content_type)  # "table"
```

### 3. Merging Embeddings

```python
from src.embeddings.ensemble_embedder import EnsembleEmbedder
import numpy as np

embedder = EnsembleEmbedder()
emb1 = embedder.embed_text("Hello")
emb2 = embedder.embed_structured({"key": "value"})

merged = embedder.merge_embeddings([emb1, emb2], weights=[0.7, 0.3])
```

---

## Backward Compatibility

- **InputContext**: Can still be initialized with a `dict` for metadata. The `__post_init__` method automatically converts it to `InputMetadata`.
- **UnifiedContext**: `input_ctx_list` is optional. If missing, the pipeline behaves as a single-stream system (v3.2 behavior).

---

## Future Work (Phase 2)

1.  **Parallel Execution**: Implement true parallel processing in `PipelineOrchestrator`.
2.  **Advanced Embeddings**: Replace random stubs with real transformer models.
3.  **Intelligent Merging**: Use attention mechanisms for ensemble embeddings.
