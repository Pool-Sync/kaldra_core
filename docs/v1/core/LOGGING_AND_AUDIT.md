# KALDRA Core — Structured Logging & Audit Trail (v2.3)

**Version:** 2.3  
**Status:** Production-Ready  
**Last Updated:** 2025-11-26  

---

## 1. Overview

This document defines the official specification for KALDRA's structured logging system and the v2.3 audit trail subsystem.  

Both systems are **non-blocking**, **fully structured**, and **zero-dependency** (stdlib only).

Logging and audit trails never modify engine behavior. They exist as **observability layers**: introspection without interference.

### Design Principles

1. **Best-Effort**: Logging failures never propagate to the inference pipeline
2. **Structured**: All events are JSON-formatted for machine parsing
3. **Timestamped**: Every event includes Unix timestamp for temporal analysis
4. **Traceable**: Request IDs link related events across the pipeline
5. **Backward Compatible**: Optional parameters preserve existing API contracts

---

## 2. Modules

### 2.1 `kaldra_logger.py`

**Location**: `src/core/kaldra_logger.py`

Defines the `KALDRALogger` class, responsible for:

- Structured JSON logging  
- Timestamped, event-typed messages  
- Pipeline diagnostics  
- Best-effort operation  
- No exceptions propagate upward  

#### JSON Event Format

```json
{
  "ts": 1764152756.205615,
  "event": "inference_start",
  "request_id": "a6594026ee714d3796ad888d39a97153",
  "embedding_shape": "(256,)",
  "has_tw_window": false,
  "d_ctx": 256,
  "tau": 0.65
}
```

#### Key Properties

- `enabled`: Global on/off switch (default: `True`)
- `logger_name`: Internal namespace (default: `"kaldra.core"`)
- `level`: Logging level (default: `logging.INFO`)
- Automatically configures a stream handler
- Always emits **pure JSON lines**

#### Class Definition

```python
@dataclass
class KALDRALogger:
    logger_name: str = "kaldra.core"
    enabled: bool = True
    level: int = logging.INFO
    _logger: logging.Logger = field(init=False, repr=False)
```

#### Methods

**`log_event(event_type: str, payload: Optional[Dict[str, Any]] = None)`**

Logs a structured event with:
- Automatic timestamp (`ts`)
- Event type identifier (`event`)
- Optional payload dictionary

Never raises exceptions. Silently fails if logging encounters errors.

---

### 2.2 `audit_trail.py`

**Location**: `src/core/audit_trail.py`

Defines `AuditTrailRecord` and `AuditTrail`.

Audit trail is:

- In-memory
- Serializable
- Exportable via JSONL
- Explicitly triggered (no automatic persistence)

#### Record Structure

```python
@dataclass
class AuditTrailRecord:
    timestamp: float
    request_id: str
    context: Dict[str, Any]
    summary: Dict[str, Any]
```

#### JSONL Export Format

One record per line:

```json
{"timestamp": 1764152756.223584, "request_id": "a6594026ee714d3796ad888d39a97153", "context": {"d_ctx": 256, "tau": 0.65}, "summary": {"max_prob": 0.00718, "max_index": 98, "epistemic_status": "INCONCLUSIVO", "tw_trigger": false, "has_delta_state": true}}
```

#### Methods

**`record_inference(request_id, context, summary, timestamp=None)`**

Records a single inference event with:
- Unique request identifier
- Execution context (engine parameters)
- Result summary (probabilities, decisions)
- Optional custom timestamp

**`to_dicts() -> List[Dict[str, Any]]`**

Converts all records to dictionaries for serialization.

**`export_jsonl(path: str | Path)`**

Exports all records to a JSONL file. Creates parent directories if needed.

---

## 3. Integration Points

### 3.1 Master Engine

Instrumentation added to `KaldraMasterEngineV2`:

**New Parameters** (backward compatible):
```python
def __init__(
    self,
    delta_engine: Optional[Delta144Engine] = None,
    d_ctx: int = 256,
    tau: float = 0.65,
    tw_config: Optional[TWConfig] = None,
    logger: Optional[KALDRALogger] = None,      # NEW
    audit_trail: Optional[AuditTrail] = None,   # NEW
):
```

**New Methods**:
- `_log_inference_start(request_id, embedding_shape, has_tw_window)`
- `_log_inference_end(request_id, signal)`

**Modified Method**:
- `infer_from_embedding()` - instrumented with logging calls

### 3.2 Instrumented Fields

The logging system captures:

**Input Metadata**:
- Request UUID (generated per inference)
- Embedding shape
- TW window presence
- Engine configuration (`d_ctx`, `tau`)

**Output Summary**:
- Max archetype probability
- Max archetype index
- Epistemic decision status
- TW trigger state
- Delta144 state presence

These fields form the **minimum audit signature**.

---

## 4. Lifecycle of a Logged Inference

### Event 1 — `inference_start`

**Triggered**: At the beginning of `infer_from_embedding()`

**Contains**:
```json
{
  "ts": 1764152756.205615,
  "event": "inference_start",
  "request_id": "a6594026ee714d3796ad888d39a97153",
  "embedding_shape": "(256,)",
  "has_tw_window": false,
  "d_ctx": 256,
  "tau": 0.65
}
```

### Event 2 — `inference_end`

**Triggered**: After `KaldraSignal` is created, before return

**Contains**:
```json
{
  "ts": 1764152756.223584,
  "event": "inference_end",
  "request_id": "a6594026ee714d3796ad888d39a97153",
  "summary": {
    "max_prob": 0.007185772527009249,
    "max_index": 98,
    "epistemic_status": "INCONCLUSIVO",
    "tw_trigger": false,
    "has_delta_state": true
  }
}
```

### Event 3 — (Optional) Audit Trail Record

**Triggered**: If `AuditTrail` instance is provided to engine

**Created**: During `_log_inference_end()`

**Stored**: In-memory until explicitly exported

---

## 5. Usage Examples

### 5.1 Default Logging (Enabled)

```python
from src.core.kaldra_master_engine import KaldraMasterEngineV2
import numpy as np

engine = KaldraMasterEngineV2(d_ctx=256)
embedding = np.random.randn(256).astype(np.float32)

# Logs automatically to stdout as JSON
result = engine.infer_from_embedding(embedding)
```

**Output** (stdout):
```json
{"ts": 1764152756.205615, "event": "inference_start", ...}
{"ts": 1764152756.223584, "event": "inference_end", ...}
```

### 5.2 Disable Logging

```python
from src.core.kaldra_logger import KALDRALogger

logger = KALDRALogger(enabled=False)
engine = KaldraMasterEngineV2(d_ctx=256, logger=logger)

# No logs produced
result = engine.infer_from_embedding(embedding)
```

### 5.3 Using Audit Trail

```python
from src.core.audit_trail import AuditTrail

audit = AuditTrail()
engine = KaldraMasterEngineV2(d_ctx=256, audit_trail=audit)

# Run multiple inferences
for i in range(100):
    emb = np.random.randn(256).astype(np.float32)
    result = engine.infer_from_embedding(emb)

# Export audit trail
audit.export_jsonl("logs/audit_2025-11-26.jsonl")
print(f"Recorded {len(audit.records)} inferences")
```

### 5.4 Custom Logger Configuration

```python
import logging
from src.core.kaldra_logger import KALDRALogger

logger = KALDRALogger(
    logger_name="kaldra.production",
    level=logging.DEBUG,
    enabled=True
)

engine = KaldraMasterEngineV2(d_ctx=256, logger=logger)
```

### 5.5 Both Logger and Audit Trail

```python
from src.core.kaldra_logger import KALDRALogger
from src.core.audit_trail import AuditTrail

logger = KALDRALogger(logger_name="kaldra.app")
audit = AuditTrail()

engine = KaldraMasterEngineV2(
    d_ctx=256,
    tau=0.7,
    logger=logger,
    audit_trail=audit
)

# Logs to stdout AND records in audit trail
result = engine.infer_from_embedding(embedding)

# Later: export audit
audit.export_jsonl("/var/log/kaldra/audit.jsonl")
```

---

## 6. Future Implementations (Roadmap v2.4–v3.0)

### 6.1 Persistent Audit Trail

**Database Backends**:
- PostgreSQL storage with indexed request_id
- MongoDB document store for flexible querying
- TimescaleDB for time-series analysis
- Redis for real-time audit access

**Object Storage**:
- S3/GCS JSONL cold-storage
- Partitioned by date (e.g., `s3://bucket/audit/2025/11/26/`)
- Expiring retention policies (e.g., 90 days hot, 1 year cold)

### 6.2 Log Aggregation

**ELK Stack**:
- Elasticsearch for log indexing
- Kibana dashboards for visualization
- Logstash for log transformation

**Cloud Solutions**:
- Datadog log ingestion with APM
- AWS CloudWatch Logs integration
- Google Cloud Logging
- Azure Monitor

**Features**:
- Structured search over request IDs
- Correlation of start/end events
- Latency distribution analysis
- Error rate monitoring

### 6.3 Metrics via Prometheus

**Expose Metrics Endpoint**:
```python
# /metrics endpoint
kaldra_inference_duration_seconds{quantile="0.5"} 0.018
kaldra_inference_duration_seconds{quantile="0.95"} 0.045
kaldra_inference_duration_seconds{quantile="0.99"} 0.082

kaldra_epistemic_decisions_total{status="OK"} 1234
kaldra_epistemic_decisions_total{status="INCONCLUSIVO"} 567

kaldra_tw_triggers_total 42
kaldra_archetype_max_prob_histogram_bucket{le="0.01"} 890
```

**Metrics to Track**:
- Inference latency buckets
- Drift severity histograms
- Epistemic decision counters
- TW trigger frequency
- Archetype distribution entropy

### 6.4 OpenTelemetry Support

**Distributed Tracing**:
```python
from opentelemetry import trace

tracer = trace.get_tracer("kaldra.core")

with tracer.start_as_current_span("kaldra.inference") as span:
    span.set_attribute("request_id", request_id)
    span.set_attribute("d_ctx", d_ctx)
    
    with tracer.start_as_current_span("delta144.infer"):
        result = self.delta.infer_from_vector(embedding)
    
    with tracer.start_as_current_span("kindra.modulate"):
        modulated = self.kindra_mod(probs_t, ctx)
```

**Benefits**:
- Distributed context propagation
- Cross-service tracing
- Performance bottleneck identification
- KALDRA Observability Specification

---

## 7. Enhancements (v2.3+)

### 7.1 Per-Module Toggles

```python
logger = KALDRALogger(
    enabled_modules=["tw369", "kindra"],  # Only log these
    disabled_modules=["delta144"]         # Skip this
)
```

### 7.2 Structured Error Logs

```python
{
  "ts": 1764152800.0,
  "event": "inference_error",
  "request_id": "...",
  "error_type": "ValueError",
  "error_message": "Invalid embedding shape",
  "stack_trace": "..."
}
```

### 7.3 Latency Breakdown

```python
{
  "ts": 1764152756.223584,
  "event": "inference_end",
  "request_id": "...",
  "latency_breakdown": {
    "delta144_ms": 5.2,
    "kindra_ms": 8.1,
    "tw369_ms": 2.3,
    "epistemic_ms": 0.8,
    "total_ms": 18.0
  }
}
```

### 7.4 Custom Formatters

Support for:
- **NDJSON** (Newline Delimited JSON)
- **ECS** (Elastic Common Schema)
- **OpenTelemetry-JSON**
- **CloudEvents** format

### 7.5 Async Logging Backend

```python
import asyncio

class AsyncKALDRALogger:
    async def log_event(self, event_type, payload):
        await self.queue.put((event_type, payload))
```

Benefits:
- Non-blocking I/O
- Batch log writes
- Reduced inference latency

---

## 8. Research Track

### 8.1 Narrative Stability Metrics

**Derived from Logs**:
- Δ144 entropy over time
- TW drift variance across inferences
- State-plane adaptive mapping shifts

**Analysis**:
```python
# Calculate entropy from logged max_prob values
import numpy as np

probs = [record["summary"]["max_prob"] for record in audit.records]
entropy = -np.sum(probs * np.log(probs + 1e-10))
```

### 8.2 Embedding Traceability

**Future Logging**:
```json
{
  "event": "inference_start",
  "embedding_hash": "sha256:abc123...",
  "embedding_source": "openai:text-embedding-ada-002",
  "semantic_drift": 0.042
}
```

**Use Cases**:
- Track embedding model changes
- Detect semantic drift over time
- Correlate embedding quality with epistemic decisions

### 8.3 Story-Level Aggregation Logs

**Multi-Turn Tracking**:
```json
{
  "event": "story_turn",
  "story_id": "story_uuid",
  "turn_number": 3,
  "request_id": "inference_uuid",
  "narrative_coherence": 0.87,
  "archetype_evolution": [98, 102, 105]
}
```

**Analysis**:
- Narrative coherence over conversation
- Archetype transitions
- Drift accumulation patterns

---

## 9. Known Limitations

### 9.1 Logging Limitations

**No Batch Compression**:
- Each event logged individually
- No automatic log rotation
- No compression (gzip, zstd)

**No Multi-Process Safety**:
- Concurrent writes from multiple processes may interleave
- No file locking mechanism
- Recommend process-specific log files

**Synchronous Only**:
- Logging is blocking (minimal overhead)
- No async logging backend (yet)
- May add ~1-2ms per inference

### 9.2 Audit Trail Limitations

**In-Memory Only**:
- All records stored in RAM
- No automatic persistence
- Memory usage grows linearly with inference count

**No Query Language**:
- No SQL-like queries
- No filtering by timestamp/status
- Must export and process externally

**No Incremental Export**:
- `export_jsonl()` writes all records
- No append mode
- No partial exports

### 9.3 Performance Considerations

**Logging Overhead**:
- Adds ~1-2ms per inference (JSON serialization)
- Synchronous I/O to stdout
- Negligible for most use cases

**Audit Trail Memory**:
- ~500 bytes per record (typical)
- 1M inferences = ~500MB RAM
- Recommend periodic exports for long-running processes

**No Sampling**:
- All inferences logged (if enabled)
- No probabilistic sampling
- May generate large log volumes in production

---

## 10. File Summary

This document formalizes:

- **The structure**: JSON event format, audit record schema
- **The lifecycle**: Start/end events, audit trail creation
- **The integration**: Master engine instrumentation
- **The future evolution**: Persistent storage, metrics, tracing

of KALDRA's observability layer.

### Related Files

- **Implementation**: `src/core/kaldra_logger.py`, `src/core/audit_trail.py`
- **Integration**: `src/core/kaldra_master_engine.py`
- **Tests**: `tests/integration/test_full_pipeline.py` (demonstrates logging)
- **Walkthrough**: `walkthrough.md` (implementation details)

### Version History

- **v2.3** (2025-11-26): Initial implementation
  - Structured JSON logging
  - In-memory audit trail
  - Master engine integration
  - Backward compatible API

---

**This document reflects the v2.3 implementation exactly as delivered.**

**Document Status**: Complete and Production-Ready  
**Location**: `docs/LOGGING_AND_AUDIT.md`
