# KALDRA Production Architecture Overview

**Version**: 1.0  
**Last Updated**: 2025-11-24  
**Status**: Production

---

## 🌍 Ecosystem Overview

The KALDRA ecosystem is a distributed architecture designed to analyze global narratives through symbolic AI and semantic inference. In its current production state (v2.1), it consists of four main pillars:

1. **Frontend**: The user interface (4iam.ai) for interaction and visualization.
2. **API Gateway**: The central nervous system exposing the KALDRA Master Engine.
3. **Master Engine**: The core logic library performing symbolic inference (Δ144, TW369).
4. **Data Lab**: The ingestion engine responsible for gathering raw data from the world.

---

## 🔄 Request Flow: User Interaction

This flow describes how a user interacts with the system to generate KALDRA signals.

```mermaid
graph LR
    User[User (Browser)] -->|HTTPS| Frontend[4iam.ai Frontend\n(Vercel)]
    Frontend -->|REST API| Gateway[KALDRA API Gateway\n(Render / Docker)]
    Gateway -->|Inference| Engine[Master Engine V2\n(Python Library)]
    Engine -->|Symbolic Logic| Components[Δ144 / TW369 / Kindras]
    Components -->|Result| Engine
    Engine -->|JSON Response| Gateway
    Gateway -->|Signal Data| Frontend
```

1. **User** initiates a request (e.g., "Analyze this text") on the 4iam.ai frontend.
2. **Frontend** sends a secure POST request to the API Gateway.
3. **API Gateway** validates the request and routes it to the Master Engine.
4. **Master Engine** performs semantic inference using Δ144 states and TW369 filters.
5. **Response** containing the KALDRA Signal (Archetype, Risk, Bias) is returned to the user.

---

## 🔄 Data Flow: Workers & Data Lab

This flow describes how the system ingests and processes background data to build historical context.

```mermaid
graph LR
    Cron[Render Cron Jobs] -->|Trigger| Worker[News Ingest Worker]
    Worker -->|Fetch| APIs[External APIs\n(MediaStack / GNews)]
    APIs -->|Raw Data| Worker
    Worker -->|Normalize| DataLab[KALDRA Data Lab]
    DataLab -->|Save .jsonl| Storage[Local Storage / Data Lake]
    Storage -.->|Future Feed| Engine[Master Engine]
```

1. **Cron Jobs** on Render trigger specific workers (e.g., `news_ingest_worker`) on a schedule.
2. **Workers** fetch data from external providers (MediaStack, GNews).
3. **Data Lab** normalizes the raw data into standard KALDRA schemas.
4. **Storage**: Data is currently saved to local ephemeral storage (container), with plans for S3 integration.

---

## 🏗️ Core Components

### 1. `kaldra_api/` (The Gateway)
- **Technology**: FastAPI (Python).
- **Role**: Handles HTTP requests, authentication, validation, and routing.
- **Key Files**: `main.py`, `routers/`, `dependencies.py`.

### 2. `src/` (The Brain)
- **Technology**: Pure Python.
- **Role**: Contains the Master Engine, Δ144 logic, TW369 oracles, and bias detectors.
- **Key Files**: `core/kaldra_master_engine.py`, `archetypes/delta144_engine.py`.

### 3. `kaldra_data/` (The Lab)
- **Technology**: Python Scripts & Clients.
- **Role**: Ingestion, preprocessing, and pipeline management.
- **Key Files**: `workers/`, `ingestion/`.

### 4. `4iam_frontend/` (The Face)
- **Technology**: Next.js, TypeScript, TailwindCSS.
- **Role**: User interface, visualization, and client-side logic.
- **Key Files**: `app/`, `lib/api/kaldra_client.ts`.

### 5. Infrastructure
- **Dockerfile**: Multi-stage build for production-ready Python environment.
- **render.yaml**: Infrastructure as Code definition for Render deployment.

---

## 📊 Observability & Logging

### Current State
- **Application Logs**: Standard Python `logging` module outputting to stdout/stderr.
- **Access Logs**: Uvicorn access logs capturing HTTP request details.
- **Worker Logs**: Execution summaries (articles fetched, duration) logged by workers.

### Future Improvements
- **Centralized Logging**: Integration with Render's log streams or external services (Datadog/LogDNA).
- **Metrics**: Prometheus endpoint for tracking request latency, error rates, and inference times.
- **Tracing**: OpenTelemetry for end-to-end request tracing across microservices.

---

**Maintained by**: 4IAM.AI Engineering Team
