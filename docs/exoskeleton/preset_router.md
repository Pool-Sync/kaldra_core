# PresetRouter Integration — Technical Documentation

## Overview
The **PresetRouter** bridges the Exoskeleton Layer (Presets + Profiles) with the Unification Layer, resolving preset configurations with user profile overrides into executable pipeline configurations.

---

## Architecture

### PresetResolvedConfig
Final configuration after merging preset + profile:

```python
@dataclass
class PresetResolvedConfig:
    name: str                           # Preset identifier
    mode: str                           # Execution mode
    emphasis: Dict[str, float]          # Stage/engine weighting
    thresholds: Dict[str, float]        # Risk, confidence limits
    output_format: str                  # Response format
    metadata: Dict[str, Any]            # Additional config
```

### PresetRouter
Resolves preset + profile into final configuration:

```python
class PresetRouter:
    def resolve_preset(preset_name, user_id) -> PresetResolvedConfig
    def get_default_config() -> PresetResolvedConfig
```

---

## Resolution Flow

```
1. Load Preset (PresetManager)
   ↓
2. Load Profile (ProfileManager, optional)
   ↓
3. Merge Configuration
   - Base: preset settings
   - Override: profile.risk_tolerance → thresholds["risk"]
   - Override: profile.output_format → output_format
   - Add: profile.depth → metadata["depth"]
   ↓
4. Return PresetResolvedConfig
```

---

## Usage

### Basic Resolution

```python
from src.unification.exoskeleton import PresetRouter

router = PresetRouter()

# Preset only
config = router.resolve_preset("alpha")

# Preset + Profile
config = router.resolve_preset("geo", user_id="analyst_123")
```

### Profile Overrides

```python
# Create profile with custom settings
pm = ProfileManager()
pm.create_profile("user_1", {
    "risk_tolerance": 0.9,
    "output_format": "detailed_report",
    "depth": "deep"
})

# Resolve with overrides
router = PresetRouter(profile_manager=pm)
config = router.resolve_preset("alpha", user_id="user_1")

# Resulting config:
# - thresholds["risk"] = 0.9 (from profile)
# - output_format = "detailed_report" (from profile)
# - metadata["depth"] = "deep" (from profile)
# - metadata["user_id"] = "user_1"
```

### Emphasis Weighting

```python
config = router.resolve_preset("geo")

# Emphasis converted to dict with weights
# {
#   "kindra.layer1": 1.0,
#   "kindra.tw_plane": 1.0,
#   "meta.aurelius": 1.0,
#   "core.archetypes": 1.0
# }
```

---

## Override Priority

1. **Base Configuration**: From preset
2. **Profile Overrides**:
   - `risk_tolerance` → `thresholds["risk"]`
   - `output_format` → `output_format`
   - `depth` → `metadata["depth"]`
   - Custom preferences → `metadata["user_preferences"]`

---

## Integration with UnifiedRouter

### Future Integration (Phase 3.C Complete)

```python
# In UnifiedRouter
def route_with_preset(self, context, preset_name, user_id=None):
    resolved = self.preset_router.resolve_preset(
        preset_name=preset_name,
        user_id=user_id
    )
    
    # Apply to context
    context.pipeline_config.mode = resolved.mode
    context.pipeline_config.thresholds = resolved.thresholds
    context.pipeline_config.emphasis = resolved.emphasis
    # ...
```

### UnifiedKaldra Entry Point

```python
# Future API
kaldra = UnifiedKaldra()
result = kaldra.analyze(
    text="Analysis text",
    preset="geo",
    profile="analyst_123"
)
```

---

## Examples

### Financial Analysis (Alpha)

```python
config = router.resolve_preset("alpha")
# mode: "full"
# emphasis: kindra.layer1, meta.nietzsche, core.archetypes
# thresholds: risk=0.30, confidence_min=0.60
# output_format: "financial_brief"
```

### Geopolitical Analysis (Geo)

```python
config = router.resolve_preset("geo")
# mode: "story"
# emphasis: kindra.layer1, kindra.tw_plane, meta.aurelius
# thresholds: risk=0.40, confidence_min=0.55
# output_format: "geopolitical_brief"
```

### Safety-First Analysis (Safeguard)

```python
config = router.resolve_preset("safeguard")
# mode: "safety-first"
# emphasis: safeguard, tau, bias, kindra.layer2
# thresholds: risk=0.20, confidence_min=0.70
# output_format: "safety_report"
```

---

## Testing

**Test Suite:** `tests/unification/test_preset_router.py`
- 15 comprehensive tests
- Coverage: resolution, overrides, metadata, emphasis, edge cases

**Run tests:**
```bash
pytest tests/unification/test_preset_router.py -v
```

**Full Exoskeleton Suite:**
```bash
pytest tests/unification/test_exoskeleton_presets.py \
       tests/unification/test_profiles.py \
       tests/unification/test_preset_router.py -v
# 11 + 13 + 15 = 39 tests
```

---

## Future Enhancements

### Short-Term (v3.2)
- Weighted pipeline execution using emphasis values
- Preset validation schema
- Fallback preset on failure
- Usage logging

### Medium-Term (v3.3)
- Multi-preset fusion ("alpha+geo")
- Preset AI optimizer based on usage patterns
- Analytics dashboard for preset usage
- REST API endpoints

### Long-Term (v3.4+)
- Preset embeddings for similarity mapping
- Reinforcement learning for auto-tuning
- Adaptive presets based on text type
- Preset explainability system

---

## Limitations (v3.1)

1. **Simple Merging** — Direct override, no weighted blending
2. **No Pipeline Effect** — Emphasis weights not yet used by pipeline
3. **Local Storage** — Profile persistence via JSON only
4. **Static Presets** — No runtime adaptation

---

## Next Steps

1. **UnifiedRouter Integration** — Implement `route_with_preset()`
2. **UnifiedKaldra API** — Add preset/profile parameters
3. **REST API** — Expose preset selection endpoints
4. **Frontend UI** — Preset selector in 4iam.ai dashboard
