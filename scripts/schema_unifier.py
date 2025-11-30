"""
Schema Unifier for KALDRA v2.9.
Generates unified JSON schemas in schema/unified/.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, List

ROOT_DIR = Path("/Users/niki/Desktop/kaldra_core")
SCHEMA_DIR = ROOT_DIR / "schema"
UNIFIED_DIR = SCHEMA_DIR / "unified"

def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    with open(path, "r") as f:
        return json.load(f)

def save_json(path: Path, data: Any):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Generated: {path}")

def infer_schema_from_list(data: List[Dict], title: str, description: str) -> Dict:
    if not data or not isinstance(data, list):
        return {"type": "array", "items": {}}
    
    # Infer properties from the first item (assuming homogeneity)
    item = data[0]
    properties = {}
    required = []
    
    for key, value in item.items():
        prop_type = "string"
        if isinstance(value, bool):
            prop_type = "boolean"
        elif isinstance(value, int):
            prop_type = "integer"
        elif isinstance(value, float):
            prop_type = "number"
        elif isinstance(value, list):
            prop_type = "array"
        elif isinstance(value, dict):
            prop_type = "object"
            
        properties[key] = {"type": prop_type}
        required.append(key)
        
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": title,
        "description": description,
        "type": "array",
        "items": {
            "type": "object",
            "required": required,
            "properties": properties
        }
    }

def main():
    print("Starting Schema Unification...")
    os.makedirs(UNIFIED_DIR, exist_ok=True)
    
    # 1. Archetypes (Infer)
    archetypes_data = load_json(SCHEMA_DIR / "archetypes/archetypes_12.json")
    if archetypes_data:
        schema = infer_schema_from_list(archetypes_data, "KALDRA Archetypes", "Schema for the 12 primary archetypes.")
        save_json(UNIFIED_DIR / "archetypes.schema.json", schema)
        
    # 2. Modifiers (Infer)
    modifiers_data = load_json(SCHEMA_DIR / "archetypes/archetype_modifiers.json")
    if modifiers_data:
        # Modifiers file might be a dict or list. Let's assume list or check.
        # If it's a dict (e.g. {"modifiers": [...]}), we need to adjust.
        # I'll assume list for now based on typical KALDRA structure, but if it fails I'll check.
        if isinstance(modifiers_data, dict) and "modifiers" in modifiers_data:
             schema = infer_schema_from_list(modifiers_data["modifiers"], "KALDRA Modifiers", "Schema for archetype modifiers.")
        elif isinstance(modifiers_data, list):
             schema = infer_schema_from_list(modifiers_data, "KALDRA Modifiers", "Schema for archetype modifiers.")
        else:
             schema = {"type": "object"} # Fallback
        save_json(UNIFIED_DIR / "modifiers.schema.json", schema)

    # 3. Polarities (Infer)
    polarities_data = load_json(SCHEMA_DIR / "archetypes/polarities.json")
    if polarities_data:
        if isinstance(polarities_data, dict) and "polarities" in polarities_data:
             schema = infer_schema_from_list(polarities_data["polarities"], "KALDRA Polarities", "Schema for polarities.")
        elif isinstance(polarities_data, list):
             schema = infer_schema_from_list(polarities_data, "KALDRA Polarities", "Schema for polarities.")
        else:
             schema = {"type": "object"}
        save_json(UNIFIED_DIR / "polarities.schema.json", schema)

    # 4. Story (Copy)
    story_schema = load_json(SCHEMA_DIR / "story/story_schema.json")
    if story_schema:
        save_json(UNIFIED_DIR / "story.schema.json", story_schema)

    # 5. TW369 (Copy)
    tw369_schema = load_json(SCHEMA_DIR / "tw369/tw369_config_schema.json")
    if tw369_schema:
        save_json(UNIFIED_DIR / "tw369.schema.json", tw369_schema)
        
    # 6. Meta (Generic)
    meta_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "KALDRA Meta Schema",
        "type": "object",
        "properties": {
            "nietzsche_engine": {"type": "object"},
            "aurelius_engine": {"type": "object"},
            "campbell_engine": {"type": "object"}
        }
    }
    save_json(UNIFIED_DIR / "meta.schema.json", meta_schema)

    # 7. Tau (Generic)
    tau_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "KALDRA Tau Schema",
        "type": "object",
        "properties": {
            "tau_config": {"type": "object"},
            "policies": {"type": "array"}
        }
    }
    save_json(UNIFIED_DIR / "tau.schema.json", tau_schema)

    # 8. Safeguard (Generic)
    safeguard_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "KALDRA Safeguard Schema",
        "type": "object",
        "properties": {
            "risk_rules": {"type": "array"},
            "mitigation_strategies": {"type": "object"}
        }
    }
    save_json(UNIFIED_DIR / "safeguard.schema.json", safeguard_schema)
    
    print("Schema Unification Complete.")

if __name__ == "__main__":
    main()
