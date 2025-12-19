"""
Test Kindra → Δ144 maps alignment with canonical archetypes.

Validates that all 3 Kindra layer maps use only the 12 canonical
archetypes from Δ144, with no legacy symbolic names.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Canonical archetypes (11 used in maps, Oracle exists but not referenced)
CANONICAL = {
    "Creator", "Sage", "Magician", "Hero", "Explorer",
    "Caregiver", "Ruler", "Rebel", "Lover", "Innocent", "Trickster"
}

# Legacy names that should NOT appear
LEGACY_NAMES = {
    "Outlaw", "Jester", "Everyman", "Guardian", "Hermit", "Judge"
}

FILES = [
    ROOT / "schema" / "kindras" / "kindra_layer1_to_delta144_map.json",
    ROOT / "schema" / "kindras" / "kindra_layer2_to_delta144_map.json",
    ROOT / "schema" / "kindras" / "kindra_layer3_to_delta144_map.json",
]


def test_kindra_maps_use_canonical_archetypes_only():
    """Test that all Kindra maps use only canonical archetypes."""
    for path in FILES:
        assert path.exists(), f"File not found: {path}"
        
        data = json.loads(path.read_text(encoding="utf-8"))
        
        # Check entry count
        assert len(data) == 48, f"{path.name} must have 48 entries, found {len(data)}"
        
        # Check each entry
        for entry in data:
            assert "id" in entry, f"{path.name}: entry missing 'id'"
            
            for key in ("boost", "suppress"):
                names = entry.get(key, [])
                
                for name in names:
                    # Must be canonical
                    assert name in CANONICAL, \
                        f"{path.name} entry {entry['id']}: invalid archetype '{name}' in {key}"
                    
                    # Must NOT be legacy
                    assert name not in LEGACY_NAMES, \
                        f"{path.name} entry {entry['id']}: legacy archetype '{name}' in {key}"


def test_kindra_maps_no_legacy_names():
    """Test that no legacy archetype names remain."""
    for path in FILES:
        content = path.read_text(encoding="utf-8")
        
        for legacy in LEGACY_NAMES:
            assert f'"{legacy}"' not in content, \
                f"{path.name} contains legacy archetype name: {legacy}"


def test_kindra_maps_structure():
    """Test basic structure of Kindra maps."""
    for path in FILES:
        data = json.loads(path.read_text(encoding="utf-8"))
        
        # Check all entries have required fields
        for entry in data:
            assert "id" in entry, f"{path.name}: entry missing 'id'"
            assert "boost" in entry or "suppress" in entry, \
                f"{path.name} entry {entry['id']}: must have boost or suppress"
            
            # Check boost/suppress are lists
            if "boost" in entry:
                assert isinstance(entry["boost"], list), \
                    f"{path.name} entry {entry['id']}: boost must be a list"
            
            if "suppress" in entry:
                assert isinstance(entry["suppress"], list), \
                    f"{path.name} entry {entry['id']}: suppress must be a list"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
