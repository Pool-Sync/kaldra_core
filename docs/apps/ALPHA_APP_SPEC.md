# KALDRA-Alpha App — Specification v1.0

## 1. Overview
KALDRA-Alpha is the specialized application module for **Earnings Call Analysis**. 
It orchestrates the ingestion of earnings transcripts (PDF/HTML/Text), processes them through the KALDRA Master Engine via the Data Lab pipeline, and produces domain-specific financial narrative signals.

**Modules:**
- `earnings_ingest.py`: Data loading and normalization.
- `earnings_pipeline.py`: End-to-end processing (Text -> Embedding -> Signal).
- `earnings_analyzer.py`: Financial domain interpretation of signals.

## 2. Architecture

```mermaid
graph LR
    Source[Earnings Source] -->|PDF/HTML/Text| Ingest[earnings_ingest]
    Ingest -->|Cleaned Text| Router[EmbeddingRouter]
    Router -->|Vector| Engine[Master Engine V2]
    Engine -->|KaldraSignal| Analyzer[earnings_analyzer]
    Analyzer -->|Alpha Payload| Dashboard[Dashboards]
```

## 3. Core Components

### 3.1 Earnings Ingest (`earnings_ingest.py`)
- **`EarningsSource`**: Dataclass defining the input (path, type, ticker, quarter).
- **`load_earnings_text`**: Dispatches to `kaldra_data` loaders based on source type.
- **`normalize_earnings_text`**: Standardizes text (whitespace collapsing) for embedding.

### 3.2 Earnings Pipeline (`earnings_pipeline.py`)
- **`run_earnings_pipeline`**: The main entry point.
  1. Loads text.
  2. Generates embedding (supports fallback).
  3. Infers signal using `KaldraMasterEngineV2`.
  4. Returns `EarningsPipelineResult`.

### 3.3 Earnings Analyzer (`earnings_analyzer.py`)
- **`summarize_archetypes`**: Calculates entropy and extracts top-k archetypes.
- **`build_alpha_signal_payload`**: Formats the result for frontend/dashboard consumption, including TW triggers and epistemic status.

## 4. Usage Examples

### Running the Pipeline
```python
from src.apps.alpha.earnings_ingest import EarningsSource
from src.apps.alpha.earnings_pipeline import run_earnings_pipeline
from src.core.kaldra_master_engine import KaldraMasterEngineV2

# 1. Setup
source = EarningsSource(
    source_type="text", 
    path_or_url="path/to/transcript.txt", 
    ticker="NVDA", 
    quarter="Q3 2025"
)
engine = KaldraMasterEngineV2() # Injected dependency

# 2. Run
result = run_earnings_pipeline(source, engine)

# 3. Analyze
from src.apps.alpha.earnings_analyzer import build_alpha_signal_payload
payload = build_alpha_signal_payload(result)
print(payload["top_archetypes"])
```

## 5. Future Implementations
- **Story Aggregation**: Link multiple quarters of earnings calls into a single `Story` to track narrative evolution over time.
- **Bias Integration**: Fully expose bias scores in the Alpha payload.
- **Multi-Modal**: Support ingestion of earnings slides (images) alongside text.

## 6. Enhancements (Short/Medium Term)
- **Advanced Cleaning**: Regex-based removal of "Operator" instructions and Q&A boilerplate.
- **Metadata Enrichment**: Auto-fetch stock price reaction to correlate with signal.
- **Multi-Language**: Support non-English earnings calls via translation layer.

## 7. Research Track (Long Term)
- **Predictive Alpha**: Correlate specific archetype shifts (e.g., "Builder" -> "Protector") with subsequent stock performance.
- **Sector Analysis**: Aggregate signals across a sector (e.g., "Tech") to find macro trends.

## 8. Known Limitations
- **Fallback Embeddings**: If SentenceTransformers is not installed, fallback embeddings are deterministic but semantically void.
- **Single Document**: Currently processes one document at a time; does not merge Transcript + Q&A automatically.

## 9. Testing
- **Location**: `tests/apps/alpha/`
- **Coverage**:
  - `test_earnings_ingest.py`: Loading and normalization logic.
  - `test_earnings_pipeline.py`: End-to-end flow with mocks.
  - `test_earnings_analyzer.py`: Math verification for entropy and summaries.
- **Command**: `pytest tests/apps/alpha -v`

## 10. Next Steps
- [ ] Integrate with 4iam.ai dashboards.
- [ ] Connect with real earnings PDFs in Data Lab.
- [ ] Add story-level aggregation per ticker.

## 11. Related Documentation
- `docs/core/MASTER_ENGINE_AND_DATALAB_OVERVIEW.md`
- `docs/core/STORY_AGGREGATION_SPEC.md`

## 12. Version History
- **v1.0** (2025-11-27): Initial implementation (Ingest + Pipeline + Analyzer).
