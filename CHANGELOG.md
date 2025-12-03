# 📜 KALDRA — CHANGELOG
**Status:** Active  
**Maintainer:** 4iam.ai / KALDRA Core Engineering  
**Changelog Standard:** Semantic Versioning (MAJOR.MINOR.PATCH)

---

# 🔵 [3.1.0] — 2025-12-03  
### Codename: **Exoskeleton**  
### Status: **Production Release**

## ✨ Added
### Exoskeleton Layer (Presets + Profiles)
- Added preset system with 4 domain modes: `alpha`, `geo`, `safeguard`, `product`
- Added profiles system with persistent JSON storage
- Added PresetRouter for merging preset + user preferences
- Added CRUD API for profiles
- Added preset listing API

### Meta Engines (Public Output)
- Exposed Nietzsche, Aurelius, Campbell outputs in `meta.*`
- Added MetaSignal mapping to SignalAdapter

### Kindra 3×48 (Public Output)
- Added Layer 1, 2, 3 (48 vectors each)
- Added TW-plane distribution (3/6/9)
- Added top vector aggregation

### API v3.1
- New endpoint: `POST /api/v3.1/analyze`
- New endpoint: `GET /api/v3.1/presets`
- New endpoint: `GET /api/v3.1/profile/{user_id}`
- New endpoint: `PUT /api/v3.1/profile/{user_id}`
- Added schema validation for preset/profile fields

### SignalAdapter v3.1
- Added `meta.*` engines to output
- Added full Kindra 3×48 structure
- Added preset metadata (`preset_used`, `preset_config`)
- Backward compatible with all v2.x/v3.0 clients

### Testing & Validation
- Added 56 Exoskeleton tests
- Added v3.1 E2E test suite
- Added performance benchmarks
- Added consistency verification script

### Documentation
- Added API v3.1 Reference
- Added Presets System docs
- Added Profiles System docs
- Added PresetRouter docs
- Added Release Notes v3.1
- Added Next Steps (Phase 3 Exoskeleton)  

---

## 🛠️ Changed
- Updated SignalAdapter to include nested structures
- Updated UnifiedRouter for preset-aware config resolution
- Improved preset immutability using deep copies
- Improved error-handling across API routes

---

## 🐛 Fixed
- Fixed KindraContext JSON serialization
- Fixed MetaContext null-handling
- Fixed profile overwrite bug
- Fixed preset fallback logic
- Fixed outdated SignalAdapter import paths

---

## ⚠️ Deprecated
### Soft Deprecations:
- Legacy `/analyze` endpoint (still supported, but discouraged)
- Old v2.x/v3.0 signal output without meta/kindra

**Removal Timeline:**
- v3.2: Mark deprecated  
- v3.4: Begin sunset  
- v3.6: Potential removal  

---

## 🔮 Under Development (3.2 → 3.6 Roadmap)
### v3.2 — Temporal Mind
- Story Buffer & Arc Detection  
- TW-Enriched Kindra  
- Timeline Builder

### v3.3 — Multi-Stream
- Multi-source inputs  
- Narrative stream comparison  
- Domain calibration  

### v3.4 — Explainability
- Explanation generator  
- Confidence scoring  
- Justification tree  

### v3.6 — Convergence
- Unified Meta Mind  
- Adaptive presets  
- Learned Δ144 / Kindra mappings  

---

# 🟢 [3.0.0] — 2025-11-30  
### Codename: **Unification Layer**

## ✨ Added
- UnifiedKernel (central orchestrator)  
- ModuleRegistry  
- UnifiedContext  
- Graceful Degradation Framework  
- TW369 v2.4 integration hooks  
- Δ144 engine v2.9 compatibility layer  

## 🔄 Changed
- All v2.x engines now load through unified router  
- Standardized state passing between pipeline stages  

## 🐛 Fixed
- Archetype bleed between Δ144 and modifiers  
- Incorrect fallback behavior when embeddings fail  

---

# 🟢 [2.x.x] — 2025 (Legacy Series)

Major improvements:
- Δ144 archetype engine  
- Archetype modifiers  
- Bias Engine  
- TW369 v2.4  
- Semantic ingestion pipeline  
- Safeguard enhancements  

---

# 📌 Format  
Every release follows:

```
## [X.Y.Z] — YYYY-MM-DD
### Added
### Changed
### Fixed
### Deprecated
### Removed
### Notes
```

---
