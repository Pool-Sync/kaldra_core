# KALDRA Architecture v2.2

This document provides a high-level overview of the KALDRA Core v2.2 architecture, detailing the data flow, module interactions, and system layers.

## 1. Macro Architecture

The system is designed as a unidirectional pipeline with feedback loops for state persistence and drift accumulation.

```ascii
[Input Data]
     |
     v
[Ingestion Layer] -> [Preprocessing]
     |
     v
[Scoring Layer] (Kindra Engine)
     |
     +---> [LLM Scorer] --+
     |                    |--> [Hybrid Mixer]
     +---> [Rule Scorer] -+
     |
     v
[Dynamics Layer] (TW369 Engine)
     |
     +---> [Drift Calculation] -> [Painlevé Filter]
     |
     v
[Mapping Layer] (Adaptive Mapping)
     |
     v
[State Layer] (Δ144 Engine)
     |
     v
[Output Layer] -> [Final State & Metrics]
```

## 2. System Layers

### 2.1. Ingestion & Preprocessing
- **Responsibility**: Receive raw text and metadata (context). Clean and normalize inputs.
- **Components**: `MasterEngine.process()` entry point.

### 2.2. Scoring Layer (Kindra)
- **Responsibility**: Convert text into 48 cultural vector scores.
- **Components**: `KindraEngine`, `KindraLLMScorer`, `KindraHybridScorer`.
- **Docs**: `docs/KINDRA_SCORING_OVERVIEW.md`, `docs/CULTURAL_VECTORS_48.md`.

### 2.3. Dynamics Layer (TW369)
- **Responsibility**: Calculate system tension, drift, and evolution.
- **Components**: `TW369Engine`, `PainleveFilter`, `AdvancedDriftModels`.
- **Docs**: `docs/TW369_ENGINE_SPEC.md`.

### 2.4. Mapping Layer (Adaptive)
- **Responsibility**: Translate Kindra scores and TW369 drift into Δ144 state weights, adapting to context.
- **Components**: `AdaptiveMapping`.
- **Docs**: `docs/TW369_ADAPTIVE_MAPPING.md`, `docs/KINDRA_DELTA144_BRIDGE.md`.

### 2.5. State Layer (Δ144)
- **Responsibility**: Determine the discrete narrative state of the system.
- **Components**: `Delta144Engine`.
- **Docs**: `schema/delta144/delta144_states.json`.

### 2.6. Output Layer
- **Responsibility**: Format and return the final results.
- **Outputs**: `FinalState`, `DriftMetrics`, `VectorScores`, `Confidence`.

## 3. Module Interactions

- **Kindra -> TW369**: Vector scores provide the raw "energy" that drives the TW369 planes.
- **Kindra -> Δ144**: Vector scores directly boost/suppress specific Δ144 states via the Bridge.
- **TW369 -> Δ144**: Drift and Plane values modulate the probability of state transitions (e.g., high drift favors "Crisis" states).
- **Context -> Adaptive Mapping**: Metadata (e.g., "Sector: Finance") adjusts the weights in the Mapping Layer.

## 4. Cross-References

- **Master Engine**: `docs/core/README_MASTER_ENGINE_V2.md`
- **Repository Structure**: `docs/REPOSITORY_STRUCTURE.md`
- **Roadmap**: `docs/core/KALDRA_CORE_MASTER_ROADMAP_V2.2.md`

## 5. Future Implementations

*   **Event-Driven Architecture**: Decoupling modules via an event bus (e.g., Kafka) for asynchronous processing.
*   **Microservices Split**: Breaking the monolith into `kaldra-kindra`, `kaldra-tw369`, and `kaldra-core` services.
*   **Data Lake Integration**: Automatically dumping all inputs and outputs to a data lake (e.g., S3 + Parquet) for analysis.
*   **Real-Time Dashboard**: A WebSocket server to stream engine state to a frontend visualization.

## 6. Enhancements (Short/Medium Term)

*   **Logging Standardization**: Implementing structured JSON logging across all modules for better observability.
*   **Config Hot-Reloading**: Watching `schema/` files for changes and reloading them without restarting the process.
*   **Circuit Breakers**: Protecting the system from cascading failures if the LLM provider goes down.
*   **Metrics Collection**: Exposing Prometheus metrics (latency, throughput, drift levels).

## 7. Research Track (Long Term)

*   **Federated Learning**: Training local Kindra models on user devices to preserve privacy.
*   **Homomorphic Encryption**: Processing sensitive data without ever decrypting it in memory.
*   **Self-Healing Architecture**: An engine that can detect its own drift and automatically re-calibrate its parameters.
*   **Neuromorphic Hardware**: Exploring the use of spiking neural networks for the TW369 dynamics layer.

## 8. Known Limitations

*   **Latency**: The sequential pipeline adds latency at each step; total round-trip time can be high.
*   **Single Point of Failure**: The Master Engine is currently a single process; if it crashes, the whole system stops.
*   **State Persistence**: State is currently ephemeral; if the process restarts, the "narrative arc" is lost.
*   **Scalability**: Vertical scaling is limited by Python's GIL; horizontal scaling requires architectural changes.
