# KALDRA v2.4 — Release Notes

**Release Date**: November 28, 2025  
**Version**: 2.4.0  
**Codename**: Mathematical Deepening & Drift Memory

---

## Overview

KALDRA v2.4 completes the mathematical foundation by replacing heuristic approximations with rigorous statistical methods, adding persistent drift tracking, and establishing explicit Δ12 representation for archetype-aware behavior.

### Key Achievements

- ✅ **Tracy-Widom Real Statistics** - Lookup tables for severity calculation
- ✅ **Painlevé Schema-Driven** - Configurable solver with regime calibration
- ✅ **Drift Memory** - Persistent state tracking with sliding window
- ✅ **Δ12 Explicit** - Base archetypal layer representation
- ✅ **100% Backward Compatible** - All features optional, v2.3 preserved

---

## What Changed

### 1. Tracy-Widom Real Statistics

**Problem**: Severity calculation used exponential heuristic, not real statistics.

**Solution**: Implemented Tracy-Widom lookup tables with real CDF values.

**Files Added**:
- `schema/tw369/tracy_widom_lookup.json` - Lookup tables for β=1,2,4
- `schema/tw369/tw_parameters.json` - TW configuration
- `src/tw369/tracy_widom.py` - TW module with fallback

**Files Modified**:
- `src/tw369/tw369_integration.py` - Uses `severity_from_index()`

**Configuration**:
```json
{
  "enabled": false,  // Default: disabled (uses legacy)
  "beta": 2,
  "use_lookup": true
}
```

### 2. Painlevé Configuration

**Problem**: Painlevé solver had hardcoded parameters.

**Solution**: Schema-driven configuration with regime-specific calibration.

**Files Added**:
- `schema/tw369/painleve_config.json` - Solver parameters
- `schema/tw369/regime_calibration.json` - Archetype-specific alpha
- `src/tw369/config_loader.py` - Config loading utilities

**Files Modified**:
- `src/tw369/painleve/painleve2_solver.py` - Added `build_default_solver()`

**Usage**:
```python
from src.tw369.painleve.painleve2_solver import build_default_solver

solver = build_default_solver(archetype_id="A07_RULER")
```

### 3. Drift Memory

**Problem**: No persistence of drift history, purely stateless.

**Solution**: DriftState tracking with sliding window memory.

**Files Added**:
- `schema/tw369/drift_state_schema.json` - State schema
- `src/tw369/drift_state.py` - DriftState dataclass
- `src/tw369/drift_memory.py` - Memory management

**Files Modified**:
- `src/tw369/tw369_integration.py` - Tracks drift in `compute_drift()`

**Usage**:
```python
from src.tw369.tw369_integration import get_drift_history

history = get_drift_history()  # List[DriftState]
```

### 4. Delta12Vector (Δ12 Explicit)

**Problem**: Δ12 was implicit, not exposed as a first-class entity.

**Solution**: Explicit Delta12Vector with projection from plane scores.

**Files Added**:
- `src/archetypes/delta12_vector.py` - Delta12Vector class
- `schema/tw369/archetype_regimes.json` - TW369 regime mapping
- `src/tw369/regime_utils.py` - Regime utilities

**Files Modified**:
- `src/archetypes/delta144_engine.py` - Added `compute_delta12()`

**Usage**:
```python
engine = Delta144Engine.from_default_files()

delta12 = engine.compute_delta12(
    plane_scores={"3": 0.2, "6": 0.6, "9": 0.2},
    profile_scores={"EXPANSIVE": 0.1, "CONTRACTIVE": 0.7, "TRANSCENDENT": 0.2}
)

dominant_id, prob = delta12.dominant()  # ("A07_RULER", 0.35)
```

---

## Backward Compatibility

**All v2.4 features are optional and disabled by default.**

- Tracy-Widom: `enabled: false` → uses legacy heuristic
- DriftMemory: Non-blocking, never fails drift calculation
- Painlevé config: Falls back to defaults if schema missing
- Delta12: Only computed when explicitly called

**No breaking changes to v2.3 behavior.**

---

## Test Coverage

**10/10 v2.4 tests passing**:
- Tracy-Widom: 5/5 ✅
- DriftMemory: 5/5 ✅

All v2.3 tests continue to pass.

---

## Migration Guide

### For Existing Users

**No action required**. v2.4 is fully backward compatible.

### To Enable v2.4 Features

1. **Tracy-Widom**: Edit `schema/tw369/tw_parameters.json`:
   ```json
   {"enabled": true, "beta": 2}
   ```

2. **Drift History**: Access via `get_drift_history()` (always active, non-blocking)

3. **Delta12**: Call `engine.compute_delta12()` when needed

---

## Next Steps (v2.5+)

- Meta-Engine "Soul" & Routing
- Story Aggregation & Narrative Arcs
- Apps Specialization (Alpha/Geo/Product)

---

**KALDRA v2.4 - Mathematical Foundation Complete** 🎯
