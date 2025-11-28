# KALDRA-GEO App — Specification v1.0

**Status:** v1.0  
**Modules:** `src/apps/geo/geo_signals.py`, `src/apps/geo/geo_risk_engine.py`

## 1. Overview
KALDRA-GEO provides geopolitical narrative signal analysis and risk assessment. It processes text from news sources, reports, and social media to identify narrative archetypes, detect TW (Tracy-Widom) anomalies, and assign risk levels based on geopolitical context.

**Key Capabilities:**
- Region-specific narrative analysis
- Risk level classification (low/medium/high/critical)
- TW anomaly detection for geopolitical events
- Integration with KALDRA Master Engine V2

## 2. Architecture

```mermaid
graph LR
    Input[Text + Region] -->|GeoSignalInput| Engine[GeoRiskEngine]
    Engine -->|EmbeddingRouter| Embed[Fallback Embeddings]
    Embed -->|Vector| Master[Master Engine V2]
    Master -->|KaldraSignal| Convert[build_geo_signal_from_kaldra]
    Convert -->|GeoSignal| Output[Risk Assessment]
```

## 3. API

### GeoRiskEngine
```python
engine = GeoRiskEngine(config=GeoRiskEngineConfig(d_ctx=256))
signal = engine.analyze_text(
    text="Geopolitical tensions rising...",
    region="APAC",
    source="news"
)
```

### GeoSignal Structure
- `top_archetypes`: Top-k narrative archetypes with probabilities
- `tw_triggered`: Boolean TW anomaly flag
- `risk_level`: "low" | "medium" | "high" | "critical"
- `extras`: Region, source, epistemic status

## 4. Future Implementations
- **Real-time News Integration**: Auto-ingest from Reuters, AP, Bloomberg APIs
- **Story Aggregation**: Multi-document narrative tracking per region
- **Historical Comparison**: Compare current signals to historical baselines
- **Multi-lingual Support**: Process non-English geopolitical content

## 5. Enhancements (Short/Medium Term)
- **Region Taxonomy**: Structured region hierarchy (continent → country → city)
- **Source Credibility Scoring**: Weight signals by source reliability
- **Temporal Tracking**: Track risk evolution over time windows
- **Alert System**: Configurable thresholds for critical risk notifications

## 6. Research Track (Long Term)
- **Predictive Geopolitical Modeling**: Forecast risk escalation using time-series analysis
- **Cross-Regional Correlation**: Detect narrative spillover between regions
- **Causal Inference**: Identify narrative drivers of geopolitical events
- **Integration with Economic Indicators**: Correlate narrative risk with market data

## 7. Known Limitations
- **Fallback Embeddings**: Current implementation uses deterministic fallback (SHA256-based) which lacks semantic richness
- **No Persistence**: Risk assessments are not stored; each analysis is stateless
- **Single-Document**: Does not aggregate multiple sources automatically
- **English-Only**: No multi-lingual support in v1.0

## 8. Testing
**Location**: `tests/apps/geo/`
**Files**:
- `test_geo_signals.py`: Signal construction and conversion
- `test_geo_risk_engine.py`: End-to-end risk analysis

**Command**: `pytest tests/apps/geo -v`

## 9. Next Steps
- [ ] Integrate with real news APIs (Reuters, Bloomberg)
- [ ] Add Story Aggregation for multi-document tracking
- [ ] Implement region taxonomy and credibility scoring
- [ ] Create GEO-specific dashboard widgets

## 10. Related Documentation
- `docs/apps/ALPHA_APP_SPEC.md`
- `docs/core/MASTER_ENGINE_AND_DATALAB_OVERVIEW.md`
- `docs/core/STORY_AGGREGATION_SPEC.md`

## 11. Version History
- **v1.0** (2025-11-27): Initial implementation
