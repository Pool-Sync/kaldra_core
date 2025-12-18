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

KINDRAS_48_FILE = KINDRAS_SCHEMA / "kindra_vectors_layer1_cultural_macro_48.json"

# TW369 Configuration
TW_ORACLE_CONFIG_FILE = TW369_SCHEMA / "tw369_planes.json"


# =============================================================================
# LLM & AI Configuration (v2.3)
# =============================================================================
import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# LLM Settings
KALDRA_LLM_PROVIDER = os.getenv("KALDRA_LLM_PROVIDER", "dummy")  # dummy, openai
KALDRA_LLM_API_KEY = os.getenv("KALDRA_LLM_API_KEY", "")
KALDRA_LLM_MODEL = os.getenv("KALDRA_LLM_MODEL", "gpt-4-turbo-preview")

# Embedding Settings
KALDRA_EMBEDDINGS_MODE = os.getenv("KALDRA_EMBEDDINGS_MODE", "LEGACY")  # LEGACY, REAL
KALDRA_EMBEDDINGS_API_KEY = os.getenv("KALDRA_EMBEDDINGS_API_KEY", "")
KALDRA_EMBEDDINGS_MODEL = os.getenv("KALDRA_EMBEDDINGS_MODEL", "text-embedding-3-small")

# Bias Provider
KALDRA_BIAS_PROVIDER = os.getenv("KALDRA_BIAS_PROVIDER", "heuristic")  # "heuristic" or "perspective"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "")

# Meta-Engine Routing (v2.5)
KALDRA_META_ROUTING_ENABLED = os.getenv("KALDRA_META_ROUTING_ENABLED", "false").lower() in ("true", "1", "yes")

# v2.7: Polarity & Modifier Flags
KALDRA_TW_POLARITY_ENABLED = os.getenv("KALDRA_TW_POLARITY_ENABLED", "false").lower() in ("true", "1", "yes")
KALDRA_DELTA12_POLARITY_ENABLED = os.getenv("KALDRA_DELTA12_POLARITY_ENABLED", "false").lower() in ("true", "1", "yes")
