"""
Kindra → Δ144 Map Normalization Script

Normalizes the 3 Kindra layer maps to use only the 12 canonical archetypes
from Δ144, replacing 16 symbolic names with canonical vocabulary.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # Points to kaldra_core/

# Normalization table: 16 symbolic names → 12 canonical archetypes
ARCHETYPE_NORMALIZATION = {
    # Already canonical
    "Creator":   "Creator",
    "Sage":      "Sage",
    "Magician":  "Magician",
    "Hero":      "Hero",
    "Explorer":  "Explorer",
    "Caregiver": "Caregiver",
    "Ruler":     "Ruler",
    "Lover":     "Lover",
    "Innocent":  "Innocent",
    "Trickster": "Trickster",
    
    # Synonyms / archetypal echoes → canonical
    "Outlaw":    "Rebel",      # Outlaw ~ Rebel
    "Jester":    "Trickster",  # Jester ~ Trickster (subversive fool)
    "Everyman":  "Innocent",   # Everyman ~ Innocent/Common Orphan
    "Guardian":  "Caregiver",  # Guardian ~ protective caregiver
    "Hermit":    "Sage",       # Hermit ~ isolated wisdom
    "Judge":     "Ruler",      # Judge ~ Ruler/Authority
}

# Canonical set (11 used in maps, Oracle exists but not referenced)
CANONICAL_SET = set(ARCHETYPE_NORMALIZATION.values())

# Files to normalize
FILES = [
    ROOT / "schema" / "kindras" / "kindra_layer1_to_delta144_map.json",
    ROOT / "schema" / "kindras" / "kindra_layer2_to_delta144_map.json",
    ROOT / "schema" / "kindras" / "kindra_layer3_to_delta144_map.json",
]


def normalize_entry(entry: dict) -> dict:
    """
    Normalize boost/suppress lists in a single entry.
    
    Args:
        entry: Map entry with boost/suppress lists
        
    Returns:
        Normalized entry
    """
    for key in ("boost", "suppress"):
        names = entry.get(key, [])
        normalized = []
        
        for name in names:
            if name not in ARCHETYPE_NORMALIZATION:
                raise ValueError(
                    f"Archetype '{name}' not in ARCHETYPE_NORMALIZATION table. "
                    f"Entry ID: {entry.get('id', 'unknown')}"
                )
            
            mapped = ARCHETYPE_NORMALIZATION[name]
            normalized.append(mapped)
        
        # Remove duplicates while maintaining order
        seen = set()
        dedup = []
        for n in normalized:
            if n not in seen:
                seen.add(n)
                dedup.append(n)
        
        entry[key] = dedup
    
    return entry


def main():
    """Main normalization process."""
    print("=" * 60)
    print("KINDRA → Δ144 MAP NORMALIZATION")
    print("=" * 60)
    print()
    
    for path in FILES:
        if not path.exists():
            print(f"[ERROR] File not found: {path}")
            continue
        
        print(f"Processing: {path.name}")
        
        # Load data
        data = json.loads(path.read_text(encoding="utf-8"))
        
        # Normalize each entry
        for entry in data:
            normalize_entry(entry)
        
        # Final validation
        for entry in data:
            for key in ("boost", "suppress"):
                for name in entry.get(key, []):
                    if name not in CANONICAL_SET:
                        raise AssertionError(
                            f"{path.name}: archetype '{name}' not canonical. "
                            f"Entry ID: {entry.get('id', 'unknown')}"
                        )
        
        # Verify entry count
        if len(data) != 48:
            print(f"  [WARNING] Expected 48 entries, found {len(data)}")
        
        # Write back
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=4) + "\n",
            encoding="utf-8"
        )
        
        print(f"  ✓ Normalized {len(data)} entries")
        print(f"  ✓ All archetypes canonical")
        print()
    
    print("=" * 60)
    print("✅ NORMALIZATION COMPLETE")
    print("=" * 60)
    print()
    print("Canonical archetypes used:")
    for arch in sorted(CANONICAL_SET):
        print(f"  - {arch}")
    print()
    print("Note: Oracle is canonical but not referenced in current maps.")


if __name__ == "__main__":
    main()
