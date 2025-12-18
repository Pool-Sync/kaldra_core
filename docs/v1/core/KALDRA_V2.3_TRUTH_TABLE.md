# KALDRA v2.3 — Truth Table

**Data**: 28 de Novembro de 2025
**Contexto**: Análise de reconciliação para preparação do Roadmap v2.3.

| Componente / Feature | Presença no Código | Presença na Documentação | Status | Ação Recomendada |
| :--- | :--- | :--- | :--- | :--- |
| **Master Engine** | `src/core/kaldra_master_engine.py` (Orchestrator) | `docs/core/README_MASTER_ENGINE_V2.md` | **FULL_MATCH** | Manter e evoluir. |
| **Delta144 Engine** | `src/archetypes/delta144_engine.py` (Inference + State) | `docs/math/DELTA144_INFERENCE.md` | **FULL_MATCH** | Substituir embeddings simulados por reais (v2.3). |
| **Kindra 3x48 (Scoring)** | `src/kindras/` (Loaders, Scorers, Bridges) | `docs/math/KINDRA_SCORING_OVERVIEW.md` | **FULL_MATCH** | Refinar regras e integrar LLM. |
| **Kindra Mappings** | `schema/kindras/*.json` (Populados) | `docs/math/KINDRA_SCORING_RULES.md` | **CODE > DOCS** | Atualizar docs para refletir que mappings já existem. |
| **TW369 (Drift)** | `src/tw369/drift.py`, `integration.py` | `docs/math/TW369_ENGINE_SPEC.md` | **FULL_MATCH** | Implementar persistência de estado (v2.4). |
| **Painlevé II Solver** | `src/tw369/painleve/` (Solver + Filter) | `docs/math/TW369_ADVANCED_DRIFT_MODELS.md` | **CODE > DOCS** | Documentar a implementação numérica real existente. |
| **Tracy-Widom Dist.** | `src/tw369/integration.py` (Heurística) | `docs/math/TW369_ENGINE_SPEC.md` | **PARTIAL** | Implementar estatística real (v2.4). |
| **Bias Engine** | `src/bias/detector.py` (Heurístico/Placeholder) | `docs/core/BIAS_ENGINE_SPEC.md` | **FULL_MATCH** | Implementar conectores reais (Perspective/Detoxify) na v2.3. |
| **Meta-Engines** | `src/meta/` (Router, Nietzsche stub) | `docs/guides/META_ENGINE_ROUTING.md` | **PARTIAL** | Implementar lógica real nos filósofos (v2.5). |
| **LLM Scorer** | `src/kindras/kindra_llm_scorer.py` (Sem client) | `docs/math/KINDRA_LLM_SCORING.md` | **FULL_MATCH** | Injetar `KaldraLLMClient` real (v2.3). |
| **Embeddings (Delta144)** | `src/archetypes/delta144_engine.py` (Real embeddings) | `docs/math/DELTA144_INFERENCE.md` | **FULL_MATCH** | EmbeddingGenerator com múltiplos providers. |
| **Apps (Alpha/Geo/etc)** | `src/apps/` (Estrutura de classes) | `docs/apps/*.md` | **PARTIAL** | Implementar lógica de negócio específica (v2.7). |
| **Data Lab Workers** | `src/datalab/` (Estrutura básica) | `docs/DATALAB_WORKERS.md` | **DOCS > CODE** | Implementar workers reais de ingestão. |
| **Frontend** | `4iam_frontend/` (Next.js app) | `docs/frontend/` | **FULL_MATCH** | Manter alinhado com API. |
| **Tau Layer** | `src/core/epistemic_limiter.py` | `docs/core/README_TAU_LAYER.md` | **FULL_MATCH** | Refinar granularidade por domínio (v2.8). |

---
**Legenda:**
- **FULL_MATCH**: Código e Docs alinhados.
- **CODE > DOCS**: Funcionalidade existe mas docs dizem que é "futuro" ou não detalham.
- **DOCS > CODE**: Docs prometem features que são apenas stubs/placeholders no código.
- **PARTIAL**: Implementação iniciada mas incompleta.
