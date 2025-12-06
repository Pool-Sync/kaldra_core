# KALDRA v3.1 — Exoskeleton (Detailed Specification)

**Codename:** "The Philosophical Layer"  
**Timeline:** Q1 2026 (16 weeks)  
**Status:** IN PROGRESS (Phases 1-3 COMPLETE, Phase 4 REMAINING)  
**Dependencies:** v3.0 Unification Layer (COMPLETE)

---

## Objective

Transform KALDRA from a unified engine into a **philosophically-aware, semantically-intelligent system** by adding:

1. **3 Meta Engines** - Nietzsche, Aurelius, Campbell (philosophical lenses)
2. **Kindra 3×48** - Full semantic intelligence (144 vectors)
3. **Exoskeleton** - Preset/Profile system for domain-specific configurations
4. **Frontend Integration** - 4iam.ai API and UI

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  EXOSKELETON LAYER (v3.1)                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Presets    │───▶│   Profiles   │───▶│PresetRouter  │ │
│  │ (Alpha/Geo)  │    │ (User Prefs) │    │  (Config)    │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│                                                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              UNIFICATION LAYER (v3.0)                       │
│  Kernel → Router → Orchestrator → Pipeline                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                ENHANCED STAGES (v3.1)                       │
│  Input → Core (+ Kindra 3×48) → Meta (+ 3 Engines) →       │
│  Story (placeholder) → Safeguard → Output                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Deliverable 1: Meta Engines

### 1.1 NietzscheEngine (Integrate & Refine)

**Status:** ✅ COMPLETE - v3.1 integrated

**Location:** `src/meta/nietzsche.py`

**Enhancements:**
- ✅ Integrate with Kindra 3×48 (all 144 vectors)
- ✅ Add TW369 basic integration (drift awareness)
- ✅ Refine MetaSignal output format
- ✅ Add morality type classification (master/slave/mixed)
- ✅ Add transcendence calculation
- ✅ Create comprehensive test suite (25 tests)
- ✅ Create documentation at `docs/meta/nietzsche_engine.md`

**Output:**
```python
@dataclass
class NietzscheSignal(MetaSignal):
    will_to_power: float  # [0, 1]
    morality_type: str  # "master" | "slave" | "mixed"
    eternal_return: float  # Cyclical pattern strength
    transcendence: float  # Übermensch markers
```

---

### 1.2 AureliusEngine (Integrate & Refine)

**Status:** ✅ COMPLETE - v3.1 integrated

**Location:** `src/meta/aurelius.py`

**Enhancements:**
- ✅ Integrate with Kindra 3×48
- ✅ Add TW369 basic integration
- ✅ Refine MetaSignal output format
- ✅ Add virtue scoring (wisdom, courage, justice, temperance)
- ✅ Add dichotomy of control classification
- ✅ Create comprehensive test suite (25 tests)
- ✅ Create documentation at `docs/meta/aurelius_engine.md`

**Output:**
```python
@dataclass
class AureliusSignal(MetaSignal):
    dichotomy_of_control: Dict[str, float]  # controllable vs not
    virtue_scores: Dict[str, float]  # wisdom, courage, justice, temperance
    memento_mori: float  # Urgency awareness
    amor_fati: float  # Acceptance of fate
```

---

### 1.3 CampbellEngine v3.1 (NEW - Snapshot Mode)

**Status:** ✅ COMPLETE - v3.1 implemented

**Location:** `src/meta/campbell_engine.py`

**Archetype Normalization (CRITICAL):**
```python
CAMPBELL_ARCHETYPES = {
    "HERO": "A04_HERO",          # ✅ was A03_WARRIOR
    "MENTOR": "A02_SAGE",
    "THRESHOLD_GUARDIAN": "A07_RULER",
    "HERALD": "A05_EXPLORER",    # ✅ was A05_SEEKER
    "SHAPESHIFTER": "A03_MAGICIAN",
    "SHADOW": "A08_REBEL",
    "ALLY": "A06_CAREGIVER",
    "TRICKSTER": "A11_TRICKSTER", # ✅ was A11_JESTER
    "CREATOR": "A01_CREATOR",    # ✅ was A12_CREATOR
    "LOVER": "A09_LOVER",
    "INNOCENT": "A10_INNOCENT",
    "ORACLE": "A12_ORACLE"
}
```

**Journey Stages:**
```python
JOURNEY_STAGES = [
    "ORDINARY_WORLD",
    "CALL_TO_ADVENTURE",
    "REFUSAL_OF_CALL",
    "MEETING_MENTOR",
    "CROSSING_THRESHOLD",
    "TESTS_ALLIES_ENEMIES",
    "APPROACH_INMOST_CAVE",
    "ORDEAL",
    "REWARD",
    "ROAD_BACK",
    "RESURRECTION",
    "RETURN_WITH_ELIXIR"
]
```

**Input:**
```python
@dataclass
class MetaInput:
    text: str
    embedding: np.ndarray
    kindra: KindraContext  # 3×48 = 144 vectors
    archetypes: ArchetypeContext  # Δ144 state
    drift: DriftContext  # TW369 basic
    polarities: Dict[str, float]
```

**Output:**
```python
@dataclass
class CampbellSignal(MetaSignal):
    journey_stage: str  # Current stage (snapshot)
    archetypal_roles: Dict[str, str]  # Δ144 → Campbell mapping
    transformation_potential: float  # Growth potential [0, 1]
    mythic_resonance: float  # Universal pattern match [0, 1]
    active_archetypes: List[str]  # Top 3 Campbell archetypes
```

**Note:** v3.1 is **snapshot-only** (no temporal context). Temporal features come in v3.2.

---

## Deliverable 2: Kindra 3×48 Full Integration

### 2.1 Corrected Specification

**Status:** ✅ COMPLETE - v3.1 implemented

**CRITICAL CORRECTION:**
- **NOT** "3 layers × 16 dimensions = 48 total"
- **IS** "3 layers × 48 vectors = 144 total"

**Files:**
- `schema/kindras/kindra_vectors_layer1_cultural_macro_48.json` (48 entries)
- `schema/kindras/kindra_vectors_layer2_semiotic_media_48.json` (48 entries)
- `schema/kindras/kindra_vectors_layer3_structural_systemic_48.json` (48 entries)

**Maps (Already Normalized):**
- `schema/kindras/kindra_layer1_to_delta144_map.json` (48 entries, canonical archetypes)
- `schema/kindras/kindra_layer2_to_delta144_map.json` (48 entries, canonical archetypes)
- `schema/kindras/kindra_layer3_to_delta144_map.json` (48 entries, canonical archetypes)

---

### 2.2 Implementation

**KindraEngine:**
```python
class KindraEngine:
    def score_all_layers(
        self,
        text: str,
        embedding: np.ndarray,
        delta12: Delta12Vector,
        polarities: Dict[str, float]
    ) -> KindraContext:
        """
        Score all 3 layers (144 total vectors).
        
        Returns:
            KindraContext with 48 scores per layer
        """
        layer1 = self._score_layer1(text, embedding)  # 48 scores
        layer2 = self._score_layer2(text, embedding)  # 48 scores
        layer3 = self._score_layer3(text, delta12, polarities)  # 48 scores
        
        tw_plane_dist = self._compute_tw_plane_distribution(
            layer1, layer2, layer3
        )
        
        return KindraContext(
            layer1=layer1,
            layer2=layer2,
            layer3=layer3,
            tw_plane_distribution=tw_plane_dist
        )
```

**KindraContext:**
```python
@dataclass
class KindraContext:
    layer1: Dict[str, float]  # 48 cultural/macro scores
    layer2: Dict[str, float]  # 48 semiotic/media scores
    layer3: Dict[str, float]  # 48 structural/systemic scores
    tw_plane_distribution: Dict[str, float]  # {"3": x, "6": y, "9": z}
    
    def get_total_vectors(self) -> int:
        return len(self.layer1) + len(self.layer2) + len(self.layer3)  # = 144
    
    def get_top_vectors(self, n: int = 10) -> List[Tuple[str, float]]:
        """Get top N vectors across all layers."""
        all_scores = {
            f"L1_{k}": v for k, v in self.layer1.items()
        } | {
            f"L2_{k}": v for k, v in self.layer2.items()
        } | {
            f"L3_{k}": v for k, v in self.layer3.items()
        }
        return sorted(all_scores.items(), key=lambda x: x[1], reverse=True)[:n]
```

---

### 2.3 Integration into CoreStage

**Enhanced CoreStage:**
```python
class CoreStage:
    def execute(self, context: UnifiedContext) -> UnifiedContext:
        # ... existing code ...
        
        # NEW: Kindra 3×48 scoring
        if self.registry.has_module("kindra"):
            kindra_engine = self.registry.get("kindra")
            kindra_ctx = kindra_engine.score_all_layers(
                text=context.input_ctx.text,
                embedding=context.input_ctx.embedding,
                delta12=context.archetype_ctx.delta12,
                polarities=context.archetype_ctx.polarity_scores
            )
            context.kindra_ctx = kindra_ctx
        
        return context
```

---

## Deliverable 3: Exoskeleton Layer

**Status:** ✅ COMPLETE - v3.1 implemented

### 3.1 Presets

**File:** `src/unification/exoskeleton/presets.py`

**Preset Definitions:**
```python
PRESETS = {
    "alpha": PresetConfig(
        name="Alpha (Financial Analysis)",
        mode="full",
        emphasis=["kindra.layer1", "story", "meta.nietzsche"],
        thresholds={"risk": 0.3},
        output_format="financial_brief",
        description="Optimized for earnings reports and financial narratives"
    ),
    "geo": PresetConfig(
        name="Geo (Geopolitical Analysis)",
        mode="story",
        emphasis=["kindra.layer1", "drift", "meta.aurelius"],
        thresholds={"risk": 0.4},
        output_format="geopolitical_brief",
        description="Optimized for geopolitical events and regional analysis"
    ),
    "safeguard": PresetConfig(
        name="Safeguard (Safety-First)",
        mode="safety-first",
        emphasis=["safeguard", "tau", "bias"],
        thresholds={"risk": 0.2},
        output_format="safety_report",
        description="Optimized for high-risk content moderation"
    ),
    "product": PresetConfig(
        name="Product (Brand/Marketing)",
        mode="full",
        emphasis=["kindra.layer2", "meta.campbell", "polarities"],
        thresholds={"risk": 0.35},
        output_format="brand_brief",
        description="Optimized for brand narratives and marketing content"
    )
}
```

---

### 3.2 Profiles

**File:** `src/unification/exoskeleton/profiles.py`

**Profile Management:**
```python
class ProfileManager:
    def create_profile(
        self,
        user_id: str,
        preferences: Dict[str, Any]
    ) -> UserProfile:
        """Create user profile with preferences."""
        
    def get_profile(self, user_id: str) -> UserProfile:
        """Retrieve user profile."""
        
    def update_profile(
        self,
        user_id: str,
        preferences: Dict[str, Any]
    ) -> UserProfile:
        """Update user preferences."""
```

---

### 3.3 PresetRouter

**File:** `src/unification/exoskeleton/preset_router.py`

**Routing Logic:**
```python
class PresetRouter:
    def route_with_preset(
        self,
        text: str,
        preset_name: str,
        profile: Optional[UserProfile] = None
    ) -> PipelineConfig:
        """Route based on preset and optional user profile."""
        preset = PRESETS[preset_name]
        
        # Merge preset with profile preferences
        config = self._merge_config(preset, profile)
        
        return config
```

---

## Deliverable 4: Frontend Integration

**Status:** ⏳ IN PROGRESS - Phase 4 (Weeks 13-16)

### 4.1 API Endpoints

**New Endpoints:**
```
POST /api/v3.1/analyze
  Body: {text, preset, profile_id}
  Returns: Enhanced signal with meta + kindra

GET /api/v3.1/presets
  Returns: Available presets

GET /api/v3.1/profile/{user_id}
  Returns: User profile

PUT /api/v3.1/profile/{user_id}
  Body: {preferences}
  Updates: User profile
```

---

### 4.2 Enhanced Signal Format

**v3.1 Signal:**
```json
{
  "version": "3.1",
  "request_id": "uuid",
  "timestamp": 1234567890.0,
  "preset": "alpha",
  "mode": "full",
  "input": {...},
  "kindra": {
    "layer1": {...},  // 48 scores
    "layer2": {...},  // 48 scores
    "layer3": {...},  // 48 scores
    "total_vectors": 144,
    "top_vectors": [...]  // Top 10
  },
  "archetypes": {...},
  "drift": {...},
  "meta": {
    "nietzsche": {...},
    "aurelius": {...},
    "campbell": {...}
  },
  "risk": {...},
  "summary": {...}
}
```

---

## Implementation Timeline (16 weeks)

### Weeks 1-4: Meta Engines
- Week 1: Refine NietzscheEngine integration
- Week 2: Refine AureliusEngine integration
- Week 3-4: Implement CampbellEngine v3.1 (snapshot)

### Weeks 5-8: Kindra 3×48
- Week 5-6: Implement KindraEngine (3×48 scoring)
- Week 7: Integrate into CoreStage
- Week 8: Testing and calibration

### Weeks 9-12: Exoskeleton
- Week 9-10: Implement Presets and Profiles
- Week 11: Implement PresetRouter
- Week 12: Integration testing

### Weeks 13-16: Frontend & Polish
- Week 13-14: API endpoints and frontend integration
- Week 15: End-to-end testing
- Week 16: Documentation and release

---

## Testing Strategy

### Unit Tests
- `tests/meta/test_nietzsche_engine.py`
- `tests/meta/test_aurelius_engine.py`
- `tests/meta/test_campbell_engine.py`
- `tests/kindras/test_kindra_engine.py`
- `tests/unification/test_exoskeleton.py`

### Integration Tests
- `tests/integration/test_v3_1_meta_integration.py`
- `tests/integration/test_v3_1_kindra_integration.py`
- `tests/integration/test_v3_1_presets.py`

### End-to-End Tests
- `tests/e2e/test_v3_1_end_to_end.py`

---

## Success Criteria

### Phase 1-3 (COMPLETE) ✅
- ✅ 3 meta engines operational and integrated
- ✅ Kindra 3×48 (144 vectors) scoring functional
- ✅ 4 presets working (Alpha, Geo, Safeguard, Product)
- ✅ Profile system operational
- ✅ All unit & integration tests passing
- ✅ Documentation complete

### Phase 4 (REMAINING) ⏳
- ⏳ Frontend integration complete
- ⏳ API endpoints deployed
- ⏳ End-to-end testing complete
- ⏳ Performance validated: <300ms for full mode
- ⏳ Release tagged: v3.1.0

---

## Risks & Mitigation

### Risk 1: Kindra LLM Scoring Latency
**Mitigation:** Implement caching, batch processing, async execution

### Risk 2: Campbell Archetype Mapping Complexity
**Mitigation:** Use normalized Δ144 vocabulary, extensive testing

### Risk 3: Frontend Integration Delays
**Mitigation:** Start API work early, parallel development

---

## Dependencies

### Internal
- v3.0 Unification Layer (COMPLETE)
- Normalized Kindra→Δ144 maps (COMPLETE)

### External
- OpenAI API (for LLM scoring)
- 4iam.ai frontend team coordination

---

**Next:** v3.2 Temporal Mind (Story + TW369)
