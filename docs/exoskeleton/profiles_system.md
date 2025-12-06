# User Profiles System — Technical Documentation

## Overview
The **User Profiles System** provides persistent user preferences for KALDRA v3.1, allowing customization of analysis modes, thresholds, and output formats.

---

## Architecture

### UserProfile
Dataclass representing persistent user preferences:

```python
@dataclass
class UserProfile:
    user_id: str                        # Unique identifier
    preferred_preset: str = "alpha"     # Default preset
    risk_tolerance: float = 0.5         # Risk level [0, 1]
    output_format: str = "json"         # Response format
    depth: str = "standard"             # Analysis depth
    preferences: Dict[str, Any]         # Custom fields
```

**Depth Options:**
- `fast` — Quick analysis, minimal depth
- `standard` — Balanced analysis (default)
- `deep` — Comprehensive analysis
- `exploratory` — Maximum depth, experimental features

### ProfileManager
Manages profile persistence with JSON file storage:

```python
class ProfileManager:
    def create_profile(user_id, preferences) -> UserProfile
    def get_profile(user_id) -> Optional[UserProfile]
    def update_profile(user_id, preferences) -> UserProfile
    def save_profile(profile) -> None
    def delete_profile(user_id) -> bool
    def list_profiles() -> List[str]
```

**Storage:** Local JSON files in `kaldra_profiles/` directory
**Future:** Pluggable with PostgreSQL or other databases

---

## Usage

### Creating a Profile

```python
from src.unification.exoskeleton import ProfileManager

mgr = ProfileManager()

# Create with defaults
profile = mgr.create_profile("user_123")

# Create with custom preferences
profile = mgr.create_profile("user_456", {
    "preferred_preset": "geo",
    "risk_tolerance": 0.7,
    "depth": "deep"
})
```

### Retrieving a Profile

```python
profile = mgr.get_profile("user_123")
if profile:
    print(f"Preferred preset: {profile.preferred_preset}")
    print(f"Risk tolerance: {profile.risk_tolerance}")
```

### Updating a Profile

```python
# Update existing fields
mgr.update_profile("user_123", {
    "risk_tolerance": 0.8,
    "output_format": "brief"
})

# Add custom preferences
mgr.update_profile("user_123", {
    "custom_field": "value",
    "favorite_domains": ["finance", "geo"]
})
```

### Deleting a Profile

```python
success = mgr.delete_profile("user_123")
```

### Listing All Profiles

```python
user_ids = mgr.list_profiles()
```

---

## Serialization

### to_json()
```python
profile = UserProfile(user_id="test", risk_tolerance=0.9)
data = profile.to_json()
# {"user_id": "test", "risk_tolerance": 0.9, ...}
```

### from_json()
```python
profile = UserProfile.from_json(data)
```

---

## Storage Format

**File Location:** `kaldra_profiles/{user_id}.json`

**Example File:**
```json
{
    "user_id": "user_123",
    "preferred_preset": "alpha",
    "risk_tolerance": 0.7,
    "output_format": "json",
    "depth": "deep",
    "preferences": {
        "custom_field": "value",
        "domains": ["finance", "geo"]
    }
}
```

---

## Integration with Presets

Profiles work alongside Presets:

```python
# Get user's preferred preset
profile = mgr.get_profile("user_123")
preset = preset_mgr.get_preset(profile.preferred_preset)

# Adjust thresholds based on user risk tolerance
adjusted_risk = preset.thresholds["risk"] * profile.risk_tolerance
```

---

## Testing

**Test Suite:** `tests/unification/test_profiles.py`
- 13 comprehensive tests
- Coverage: CRUD operations, serialization, persistence, validation

**Run tests:**
```bash
pytest tests/unification/test_profiles.py -v
```

---

## Future Enhancements

### Short-Term (v3.1)
- Field validation (risk_tolerance ∈ [0, 1])
- Profile caching for performance
- Profile templates

### Medium-Term (v3.2)
- Database backend (PostgreSQL)
- API endpoints:
  - `GET /api/v3/profile/{user_id}`
  - `PUT /api/v3/profile/{user_id}`
  - `DELETE /api/v3/profile/{user_id}`
- Profile inheritance from presets
- User profile analytics

### Long-Term (v3.3+)
- Profile clustering (persona maps)
- Auto-tuning based on usage patterns
- Multi-tenant profile management
- Profile encryption for sensitive data

---

## Limitations (v3.1)

1. **Local Storage Only** — JSON files, not database
2. **No Validation** — Fields accept any values (validation planned v3.2)
3. **No Router Integration** — Not yet connected to UnifiedKaldra
4. **No Encryption** — Profile data stored in plain text
5. **No Versioning** — Profile schema changes not managed

---

## Next Steps

1. **Preset Router Integration** — Connect profiles to analysis pipeline
2. **API Endpoints** — Expose profile management via REST API
3. **Frontend UI** — User preferences panel in 4iam.ai
4. **Database Migration** — Move from JSON to PostgreSQL
