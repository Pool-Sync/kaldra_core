# KALDRA Core Repository Structure

This document outlines the structure of the KALDRA Core monorepo, detailing the purpose of each directory and key files.

## Root Directory

```
kaldra_core/
├── docs/                   # Documentation
├── schema/                 # JSON Schemas and Configuration
├── src/                    # Source Code
├── tests/                  # Unit and Integration Tests
├── .gitignore
├── README.md
└── requirements.txt
```

## 1. Documentation (`docs/`)

Contains all technical and architectural documentation.

```
docs/
├── archetypes/             # Documentation for archetypes and polarities
│   └── README_POLARITIES.md
├── core/                   # Core engine documentation
│   ├── KALDRA_CORE_MASTER_ROADMAP_V2.2.md
│   ├── KALDRA_CORE_MASTER_TASKLIST.md
│   └── README_MASTER_ENGINE_V2.md
├── kindras/                # Kindra engine documentation
│   └── LEGACY_MIGRATION_GUIDE.md
├── ARCHITECTURE_V2.md      # High-level architecture overview
├── BIAS_ENGINE_SPEC.md     # Specification for Bias Engine
├── CULTURAL_VECTORS_48.md  # Detailed guide to 48 cultural vectors
├── KINDRA_DELTA144_BRIDGE.md # Bridge between Kindra and Δ144
├── KINDRA_HYBRID_SCORING.md # Hybrid scoring documentation
├── KINDRA_LLM_SCORING.md   # LLM scoring documentation
├── KINDRA_SCORING_OVERVIEW.md # Overview of all scoring methods
├── REPOSITORY_STRUCTURE.md # This file
├── TW369_ADAPTIVE_MAPPING.md # Adaptive State-Plane Mapping docs
└── TW369_ENGINE_SPEC.md    # TW369 Engine specification
```

## 2. Schemas (`schema/`)

Contains JSON schemas and configuration files that drive the engines.

```
schema/
├── archetypes/             # Archetype definitions
│   └── polarities.json     # The 48 immutable polarities
├── delta144/               # Δ144 Engine schemas
│   ├── delta144_states.json # Definitions of 144 states
│   └── modifiers.json      # Modifier definitions
├── kindras/                # Kindra Engine schemas
│   ├── kindra_config.json  # General Kindra config
│   ├── kindra_hybrid_config.json # Hybrid scoring config
│   └── vectors.json        # Definitions of 48 cultural vectors
└── tw369/                  # TW369 Engine schemas
    ├── drift_parameters.json # Drift model parameters
    ├── tw369_adaptive_mapping.json # Adaptive mapping rules
    ├── tw369_config_schema.json # TW369 configuration schema
    └── tw369_state_schema.json # TWState definition
```

## 3. Source Code (`src/`)

The core logic of the KALDRA platform.

```
src/
├── core/                   # Core utilities and base classes
│   └── master_engine.py    # Main entry point
├── delta144/               # Δ144 Engine logic
│   ├── delta144_engine.py  # State machine logic
│   └── delta144_loader.py  # Schema loader
├── kindras/                # Kindra Engine logic
│   ├── legacy/             # Deprecated legacy modules
│   │   ├── vectors.json
│   │   └── scoring.py
│   ├── kindra_engine.py    # Main Kindra engine
│   ├── kindra_hybrid_scorer.py # Hybrid scoring logic
│   ├── kindra_llm_scorer.py # LLM scoring logic
│   ├── scoring_dispatcher.py # Orchestrates scoring layers
│   ├── layer1_cultural_macro_scoring.py
│   ├── layer2_semiotic_media_scoring.py
│   ├── layer3_structural_systemic_scoring.py
│   └── prompts/            # LLM prompts
│       └── kindra_llm_prompt.json
├── tw369/                  # TW369 Engine logic
│   ├── tw369_engine.py     # Main TW369 engine
│   ├── tw369_integration.py # Integration logic
│   ├── advanced_drift_models.py # Models B, C, D
│   ├── adaptive_mapping.py # Adaptive mapping logic
│   └── painleve_filter.py  # Painlevé II filter
└── utils/                  # Shared utilities
    └── math_utils.py
```

## 4. Tests (`tests/`)

Comprehensive test suite for all components.

```
tests/
├── core/                   # Core engine tests
│   ├── test_advanced_drift_models.py
│   ├── test_painleve_filter.py
│   └── test_tw369_adaptive_mapping.py
├── integration/            # Integration tests
│   └── test_tw369_advanced_drift_selection.py
├── kindras/                # Kindra engine tests
│   ├── test_hybrid_scorer.py
│   └── test_llm_scorer.py
└── tw369/                  # TW369 engine tests
```

## Module Relationships

1.  **Master Engine** orchestrates **Kindra**, **TW369**, and **Δ144**.
2.  **Kindra** feeds vector scores to **TW369** and **Δ144**.
3.  **TW369** calculates drift and feeds it to **Δ144** via **Adaptive Mapping**.
4.  **Δ144** consumes all inputs to determine the final state.
5.  **Schemas** define the data structures and rules for all engines.

## Future Implementations

*   **`src/safeguard/`**: Directory for the upcoming Safeguard Engine (v2.4).
*   **`src/bias/`**: Directory for the upcoming Bias Engine (v2.3).
*   **`kaldra_api/`**: Future home for the FastAPI/gRPC interface layer.
*   **`docker/`**: Containerization scripts for distributed deployment.

## Enhancements (Short/Medium Term)

*   **Schema Validation CI**: Automated GitHub Action to validate all JSON files against a meta-schema.
*   **Type Hinting Coverage**: Increasing `mypy` strictness across `src/`.
*   **Docstring Standardization**: Enforcing Google-style docstrings for all public methods.
*   **Test Coverage Reports**: Integration of `pytest-cov` for visibility.

## Research Track (Long Term)

*   **Monorepo vs. Microservices**: Evaluating the split of Kindra and TW369 into separate services for independent scaling.
*   **Rust Extensions**: Rewriting `src/tw369/painleve_filter.py` in Rust for performance.
*   **Graph Database Integration**: Moving from JSON schemas to Neo4j for complex relationship mapping.
*   **Versioning Strategy**: Implementing semantic versioning for individual modules within the monorepo.

## Known Limitations

*   **Flat Structure**: The current `src/` structure may become unwieldy as the codebase grows; further nesting may be required.
*   **Local-Only**: No built-in support for cloud storage (S3/GCS) of artifacts.
*   **Config Fragmentation**: Configuration is split across multiple JSON files; a unified config loader is needed.
*   **No Hot-Reload**: Changes to `src/` require a full restart of the Python process.
