# Exoskeleton Presets System — Technical Documentation

## Overview
The **Exoskeleton Presets System** provides domain-specific analysis modes for KALDRA v3.1, allowing users to select optimized configurations for different use cases.

---

## Architecture

### PresetConfig
Dataclass defining how KALDRA operates for a specific context:

```python
@dataclass
class PresetConfig:
    name: str                           # Unique identifier
    description: str                    # Human-readable description
    mode: str                           # Execution mode
    emphasis: List[str]                 # Prioritized modules
    thresholds: Dict[str, float]        # Risk/confidence limits
    output_format: str                  # Response format
    metadata: Dict[str, Any]            # Frontend/API info
```

### PresetManager
Manages preset retrieval and listing:
- `get_preset(name)` → Returns deep copy of PresetConfig
- `list_presets()` → Returns all presets (deep copies)
- `has_preset(name)` → Checks existence

**Immutability:** All methods return deep copies to prevent external modification.

---

## Default Presets

### Alpha (Financial Analysis)
- **Mode:** `full`
- **Emphasis:** `kindra.layer1`, `meta.nietzsche`, `core.archetypes`, `story`
- **Thresholds:** `risk=0.30`, `confidence_min=0.60`
- **Output:** `financial_brief`
- **Use Case:** Earnings narratives, financial reporting

### Geo (Geopolitical Analysis)
- **Mode:** `story`
- **Emphasis:** `kindra.layer1`, `kindra.tw_plane`, `meta.aurelius`, `core.archetypes`
- **Thresholds:** `risk=0.40`, `confidence_min=0.55`
- **Output:** `geopolitical_brief`
- **Use Case:** Political narratives, regime analysis

### Safeguard (Safety-First)
- **Mode:** `safety-first`
- **Emphasis:** `safeguard`, `tau`, `bias`, `kindra.layer2`
- **Thresholds:** `risk=0.20`, `confidence_min=0.70`
- **Output:** `safety_report`
- **Use Case:** Content moderation, risk mitigation

### Product (Brand/Marketing)
- **Mode:** `full`
- **Emphasis:** `kindra.layer2`, `meta.campbell`, `core.polarities`, `core.archetypes`
- **Thresholds:** `risk=0.35`, `confidence_min=0.60`
- **Output:** `brand_brief`
- **Use Case:** Brand narratives, market resonance

---

## Usage

```python
from src.unification.exoskeleton import PresetManager

# Initialize manager
mgr = PresetManager()

# Get specific preset
alpha_preset = mgr.get_preset("alpha")

# List all presets
all_presets = mgr.list_presets()

# Check existence
if mgr.has_preset("custom"):
    preset = mgr.get_preset("custom")
```

### Custom Presets

```python
custom = PresetConfig(
    name="custom",
    description="Custom analysis mode",
    mode="full",
    emphasis=["custom.module"],
    thresholds={"risk": 0.25}
)

mgr = PresetManager(extra_presets={"custom": custom})
```

---

## Integration Points

### Future: Preset Router (Phase 3 Step 2)
```python
# Next implementation step
UnifiedKaldra.analyze(text, preset="alpha")
```

### Future: User Profiles (Phase 3.b)
- Persistent user preferences
- Override preset thresholds
- Customization per tenant/workspace

---

## Testing

**Test Suite:** `tests/unification/test_exoskeleton_presets.py`
- 11 comprehensive tests
- Coverage: structure, validation, immutability, domain specifics

**Run tests:**
```bash
pytest tests/unification/test_exoskeleton_presets.py -v
```

---

## Limitations (v3.1)

1. **Static Configuration** — Presets are hard-coded, not adaptive
2. **No Router Integration** — Not yet connected to UnifiedKaldra entry point
3. **Semantic Emphasis** — `emphasis` fields require convention adherence
4. **No Persistence** — Presets exist only in-memory

---

## Future Enhancements

### Short-Term
- Add `enabled_stages` field for granular stage control
- Add `kindra_weighting` for layer-specific weights
- Export presets via API endpoint

### Medium-Term
- Per-domain preset customization (Alpha in Geo vs Alpha in Product)
- Workspace/tenant-specific presets
- Preset override system

### Long-Term
- A/B testing of preset configurations
- Adaptive presets based on usage patterns
- Auto-Preset-Tuning via ML
