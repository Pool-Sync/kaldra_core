# KALDRA v3.x Roadmap Rebuild — DIFF Report

**Date:** December 1, 2025  
**Type:** Complete Roadmap Reconstruction  
**Status:** COMPLETE

---

## Executive Summary

This document details all changes between the original v3.x roadmap and the rebuilt version, including critical corrections, clarifications, and structural improvements.

---

## Critical Corrections

### 1. Kindra 3×48 Specification ⚠️ CRITICAL

**OLD (INCORRECT):**
```
Kindra 3×48 Full Integration
- Layer 1: Cultural/Macro (16 dimensions)
- Layer 2: Semiotic/Media (16 dimensions)
- Layer 3: Archetypal/Micro (16 dimensions)
- Total: 3 × 16 = 48 dimensions
```

**NEW (CORRECT):**
```
Kindra 3×48 Full Integration
- Layer 1: Cultural/Macro (48 vectors)
- Layer 2: Semiotic/Media (48 vectors)
- Layer 3: Structural/Systemic (48 vectors)
- Total: 3 × 48 = 144 vectors

Note: "16 dimensions" are conceptual groupings for UI/resonance,
NOT the actual vector count. Each layer has 48 distinct vectors.
```

**Impact:** MAJOR - Affects all Kindra integration planning and implementation

**Files Affected:**
- `schema/kindras/kindra_vectors_layer1_cultural_macro_48.json` (48 entries)
- `schema/kindras/kindra_vectors_layer2_semiotic_media_48.json` (48 entries)
- `schema/kindras/kindra_vectors_layer3_structural_systemic_48.json` (48 entries)

---

### 2. Campbell Engine Archetype Normalization ⚠️ CRITICAL

**OLD (INCORRECT):**
```python
CAMPBELL_ARCHETYPES = {
    "WARRIOR": "A03_WARRIOR",  # ❌ Non-canonical
    "CREATOR": "A12_CREATOR",  # ❌ Wrong ID
    "SEEKER": "A05_SEEKER",    # ❌ Non-canonical
    "JESTER": "A11_JESTER",    # ❌ Non-canonical
    ...
}
```

**NEW (CORRECT):**
```python
CAMPBELL_ARCHETYPES = {
    "HERO": "A04_HERO",          # ✅ Normalized from WARRIOR
    "CREATOR": "A01_CREATOR",    # ✅ Correct ID
    "HERALD": "A05_EXPLORER",    # ✅ Normalized from SEEKER
    "TRICKSTER": "A11_TRICKSTER", # ✅ Normalized from JESTER
    ...
}
```

**Impact:** CRITICAL - Ensures Campbell aligns with Δ144 canonical vocabulary

**Normalization Table:**
| Old Name | Correct Δ144 | Rationale |
|----------|--------------|-----------|
| A03_WARRIOR | A04_HERO | Warrior ~ Hero archetype |
| A12_CREATOR | A01_CREATOR | Wrong ID, correct is A01 |
| A05_SEEKER | A05_EXPLORER | Seeker ~ Explorer archetype |
| A11_JESTER | A11_TRICKSTER | Jester ~ Trickster archetype |

---

### 3. Story Timeline Integration Clarity ⚠️ HIGH

**OLD (AMBIGUOUS):**
```
v3.1: Meta Engines + Kindra + Story
v3.2: TW369 Deepening
```

**NEW (CLEAR):**
```
v3.1: Meta Engines + Kindra (Story Stage = PLACEHOLDER)
v3.2: Story Engine + TW369 Topology (Story Stage = OPERATIONAL)
```

**Clarifications:**
- **v3.1:** Story Stage remains placeholder, no StoryContext
- **v3.2:** Full Story implementation:
  - StoryBuffer with persistent events
  - TimelineBuilder for archetypal transitions
  - ArcDetector for narrative structure
  - CoherenceScorer for temporal consistency
  - CampbellEngine v3.2 uses StoryContext

**Impact:** HIGH - Clarifies dependencies and prevents premature Story integration

---

### 4. TW369 Topological Deepening Detail ⚠️ HIGH

**OLD (INCOMPLETE):**
```
TW369 Integration
- Basic drift calculation
- Regime detection
```

**NEW (COMPLETE):**
```
TW369 Topological Deepening
- drift_metric (numerical measure)
- regime (current archetypal regime)
- volatility (regime stability)
- trajectory (historical drift path)
- turning_points (regime transitions)
- Painlevé II smoothing (trajectory filtering)
- Tracy-Widom severity (statistical significance)
- Persistent drift history (sliding window)
```

**Impact:** HIGH - Enables true temporal intelligence

---

### 5. Multi-Stream Narratives Placement ⚠️ MEDIUM

**OLD (INCORRECT):**
```
v3.2: Story + Multi-Stream
```

**NEW (CORRECT):**
```
v3.2: Story (single-stream temporal)
v3.3: Multi-Stream (multi-modal + multi-stream)
```

**Rationale:** Better separation of concerns, clearer version scoping

**Impact:** MEDIUM - Improves version clarity

---

## Structural Changes

### Directory Structure

**OLD:**
```
docs/core/
  KALDRA_V3.X_ROADMAP_HIGHLEVEL.md
  KALDRA_V3.X_ENGINE_EXPANSION_POINTS.md
```

**NEW:**
```
docs/roadmaps/
  README.md (index)
  KALDRA_V3_ROADMAP.md (master)
  KALDRA_V3_1_EXOSKELETON.md
  KALDRA_V3_2_TEMPORAL_MIND.md
  KALDRA_V3_3_MULTI_STREAM.md
  KALDRA_V3_4_EXPLAINABLE.md
  KALDRA_V3_5_CONVERGENCE.md
  DIFF_REPORT_V3_REBUILD.md (this file)
  archive/v2/ (old roadmaps)
```

**Rationale:** Better organization, version-specific documents, clear archive

---

## Content Enhancements

### 1. Campbell Engine v3.1 vs v3.2 Distinction

**NEW CLARITY:**
- **v3.1 (Snapshot Mode):** Static analysis, no temporal context
- **v3.2 (Temporal Mode):** StoryContext integration, transformation arcs

### 2. Kindra Context Structure

**NEW SPECIFICATION:**
```python
@dataclass
class KindraContext:
    layer1: Dict[str, float]  # 48 scores
    layer2: Dict[str, float]  # 48 scores
    layer3: Dict[str, float]  # 48 scores
    tw_plane_distribution: Dict[str, float]
    
    def get_total_vectors(self) -> int:
        return 144  # 3 × 48
```

### 3. Preset System Detail

**NEW PRESETS:**
- Alpha (Financial Analysis)
- Geo (Geopolitical Analysis)
- Safeguard (Safety-First)
- Product (Brand/Marketing)

Each with specific emphasis, thresholds, and output formats.

---

## Documentation Improvements

### 1. Version-Specific Documents

Each version now has dedicated document with:
- Detailed objectives
- Component specifications
- Implementation timeline
- Testing strategy
- Success criteria
- Risk mitigation

### 2. Master Roadmap

Comprehensive overview with:
- All corrections applied
- Clear version progression
- Dependency tracking
- Timeline overview

### 3. README Index

Navigation document linking all roadmap files.

---

## Testing Additions

### NEW Test Requirements

**v3.1:**
- Campbell archetype normalization tests
- Kindra 3×48 integration tests
- Preset/Profile system tests

**v3.2:**
- Story buffer tests
- TW369 topology tests
- Campbell temporal tests

**v3.3–v3.5:**
- Multi-stream tests
- Explanation generation tests
- Learned mapping tests

---

## Implementation Impact

### Immediate (v3.1)

**Must Implement:**
1. Campbell archetype normalization (CRITICAL)
2. Kindra 3×48 scoring (144 vectors, not 48)
3. Story Stage as placeholder (not operational)

**Can Defer:**
1. Story Timeline (v3.2)
2. Multi-Stream (v3.3)
3. Learned Mappings (v3.5)

---

## Files Modified/Created

### Created
- `docs/roadmaps/README.md`
- `docs/roadmaps/KALDRA_V3_ROADMAP.md`
- `docs/roadmaps/KALDRA_V3_1_EXOSKELETON.md`
- `docs/roadmaps/KALDRA_V3_2_TEMPORAL_MIND.md`
- `docs/roadmaps/KALDRA_V3_3_MULTI_STREAM.md`
- `docs/roadmaps/KALDRA_V3_4_EXPLAINABLE.md`
- `docs/roadmaps/KALDRA_V3_5_CONVERGENCE.md`
- `docs/roadmaps/DIFF_REPORT_V3_REBUILD.md` (this file)

### Archived
- `docs/roadmaps/archive/v2/KALDRA_V3.X_ROADMAP_HIGHLEVEL_OLD.md`
- `docs/roadmaps/archive/v2/KALDRA_V3.X_ENGINE_EXPANSION_POINTS_OLD.md`

---

## Validation Checklist

- ✅ Kindra 3×48 specification corrected (144 vectors)
- ✅ Campbell archetypes normalized to Δ144
- ✅ Story Timeline placement clarified (v3.2, not v3.1)
- ✅ TW369 topology detailed
- ✅ Multi-Stream moved to v3.3
- ✅ Version-specific documents created
- ✅ Master roadmap comprehensive
- ✅ Old roadmaps archived
- ✅ README index created
- ✅ All corrections documented

---

## Conclusion

The KALDRA v3.x roadmap has been **completely rebuilt** with:

1. **5 critical corrections** applied
2. **7 new documents** created
3. **Clear version progression** established
4. **Comprehensive specifications** provided
5. **Old roadmaps** properly archived

**The roadmap is accurate, complete, and ready for v3.1 implementation.**

---

**Status:** COMPLETE ✅  
**Next Step:** Begin v3.1 Exoskeleton implementation
