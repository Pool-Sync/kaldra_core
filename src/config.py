"""
KALDRA Configuration
====================
Centralized configuration for all KALDRA core modules.
"""

from pathlib import Path

# Project root (kaldra_core/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Main directories
SRC_DIR = PROJECT_ROOT / "src"
SCHEMA_DIR = PROJECT_ROOT / "schema"
DOCS_DIR = PROJECT_ROOT / "docs"

# Schema subdirs
ARCHETYPES_SCHEMA = SCHEMA_DIR / "archetypes"
KINDRAS_SCHEMA = SCHEMA_DIR / "kindras"
TW369_SCHEMA = SCHEMA_DIR / "tw369"

# Data files
POLARITIES_FILE = ARCHETYPES_SCHEMA / "polarities.json"
DELTA144_STATES_FILE = ARCHETYPES_SCHEMA / "delta144_states.json"
ARCHETYPES_12_FILE = ARCHETYPES_SCHEMA / "archetypes_12.json"
MODIFIERS_FILE = ARCHETYPES_SCHEMA / "archetype_modifiers.json"

KINDRAS_48_FILE = KINDRAS_SCHEMA / "kindra_vectors_48.json"
