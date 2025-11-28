# KALDRA-Product App — Specification v1.0

**Status:** v1.0  
**Modules:** `src/apps/product/product_kindra_mapping.py`

## 1. Overview
KALDRA-Product analyzes product and brand narratives using Kindra cultural modulation layers. It processes customer reviews, social media feedback, and support interactions to map text to multi-layered Kindra vectors, revealing cultural and narrative patterns in product perception.

**Key Capabilities:**
- Kindra layer extraction (Layer 1: Cultural Macro, Layer 2: Narrative Modulation, Layer 3: Fine-grained)
- Product-specific archetype analysis
- Channel-aware processing (reviews, social, support)
- Brand drift detection (future)

## 2. Architecture

```mermaid
graph LR
    Input[Product Text] -->|ProductNarrativeInput| Mapper[map_text_to_product_kindra]
    Mapper -->|EmbeddingRouter| Embed[Fallback Embeddings]
    Embed -->|Vector| Master[Master Engine V2]
    Master -->|KaldraSignal| Extract[Kindra Layer Extraction]
    Extract -->|ProductKindraMapping| Output[Kindra Vectors]
```

## 3. API

### Product Kindra Mapping
```python
from src.apps.product.product_kindra_mapping import map_text_to_product_kindra
from src.core.kaldra_master_engine import KaldraMasterEngineV2

engine = KaldraMasterEngineV2(d_ctx=256)
mapping = map_text_to_product_kindra(
    text="This product exceeded my expectations!",
    engine=engine,
    product_id="PROD-123",
    category="electronics"
)
```

### ProductKindraMapping Structure
- `kindra_layer1`: Cultural macro vectors (dict)
- `kindra_layer2`: Narrative modulation (dict)
- `kindra_layer3`: Fine-grained adjustments (dict)
- `dominant_vectors`: Primary cultural vectors
- `archetype_top_indices`: Top archetype indices

## 4. Future Implementations
- **Direct Kindra Exposure**: Once KaldraSignal exposes Kindra metadata, extract real layer values
- **Product Taxonomy**: Hierarchical product categorization
- **Sentiment Correlation**: Map Kindra vectors to sentiment scores
- **Competitive Analysis**: Compare Kindra profiles across competing products

## 5. Enhancements (Short/Medium Term)
- **Channel-Specific Weights**: Different Kindra interpretations for reviews vs. social vs. support
- **Temporal Tracking**: Track Kindra drift over product lifecycle
- **Anomaly Detection**: Flag unusual Kindra patterns (e.g., sudden cultural shift)
- **Recommendation Engine**: Suggest product improvements based on Kindra gaps

## 6. Research Track (Long Term)
- **Cultural Market Segmentation**: Cluster customers by Kindra profiles
- **Predictive Churn**: Identify churn risk from Kindra pattern changes
- **Cross-Product Narrative Transfer**: Detect narrative spillover between product lines
- **Generative Product Positioning**: Use Kindra to generate optimal marketing copy

## 7. Known Limitations
- **Placeholder Kindra Layers**: v1.0 uses simplified archetype-to-vector mapping; real Kindra extraction pending
- **No Historical Tracking**: Each analysis is independent; no time-series support
- **Single-Text Input**: Does not aggregate multiple reviews automatically
- **English-Only**: No multi-lingual support

## 8. Testing
**Location**: `tests/apps/product/`
**Files**:
- `test_product_kindra_mapping.py`: Mapping logic and structure validation

**Command**: `pytest tests/apps/product -v`

## 9. Next Steps
- [ ] Integrate real Kindra layer extraction from KaldraSignal
- [ ] Add temporal tracking for brand drift detection
- [ ] Implement channel-specific weighting
- [ ] Create Product dashboard with Kindra visualizations

## 10. Related Documentation
- `docs/apps/ALPHA_APP_SPEC.md`
- `docs/core/MASTER_ENGINE_AND_DATALAB_OVERVIEW.md`
- `docs/kindras/` (Kindra scoring documentation)

## 11. Version History
- **v1.0** (2025-11-27): Initial implementation with placeholder Kindra layers
