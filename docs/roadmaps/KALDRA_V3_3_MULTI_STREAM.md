# KALDRA v3.3 — Multi-Stream

**Codename:** "The Multi-Modal Layer"  
**Timeline:** Q3 2026 (12 weeks)  
**Status:** FUTURE  
**Dependencies:** v3.2 Temporal Mind (COMPLETE)

---

## Objective

Extend to **multi-modal, multi-source, multi-stream** analysis.

---

## Core Deliverables

### 1. Multi-Modal Input

**Enhanced InputContext:**
```python
@dataclass
class InputContext:
    text: str
    embedding: np.ndarray
    metadata: Dict[str, Any]  # NEW
    sources: List[str]  # NEW
    structured_data: Optional[Dict]  # NEW
    bias_score: float
    tau_input: TauState
```

---

### 2. Multi-Stream Narratives

**Stream-Aware Events:**
```python
@dataclass
class StoryEvent:
    timestamp: float
    text: str
    archetype: Archetype
    polarities: Dict[str, float]
    stream_id: str  # NEW - "company", "sector", "region"
```

**Cross-Stream Analysis:**
- Compare narratives
- Detect divergence (Kindra, Δ144, TW-regime)
- Identify correlations

---

### 3. Ensemble Embeddings

- Multiple models (OpenAI, local, domain-specific)
- Weighted ensemble
- Fallback chain

---

## Success Criteria

- ✅ Multi-modal input working
- ✅ Multi-stream narratives operational
- ✅ Ensemble embeddings functional

---

**Next:** v3.4 Explainable
