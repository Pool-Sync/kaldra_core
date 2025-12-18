# KALDRA v2.3 — Clean Structure Proposal

**Data**: 28 de Novembro de 2025
**Objetivo**: Definir a estrutura de diretórios canônica para a v2.3 e além.

Esta proposta consolida a limpeza iniciada na Fase Z e define o padrão para novos desenvolvimentos.

## 1. Estrutura de Documentação (`docs/`)

A estrutura atual (pós-Fase Z) deve ser mantida e reforçada:

```text
docs/
├── core/               # Governança, Roadmap, Arquitetura Central
│   ├── KALDRA_CORE_MASTER_ROADMAP_V2.3_V2.9.md
│   ├── KALDRA_V2.3_TRUTH_TABLE.md
│   ├── KALDRA_V2.3_RECONCILIATION_REPORT.md
│   └── README_MASTER_ENGINE_V2.md
├── math/               # Especificações Matemáticas (TW369, Kindra, Delta144)
│   ├── TW369_ENGINE_SPEC.md
│   ├── KINDRA_SCORING_OVERVIEW.md
│   └── DELTA144_INFERENCE.md
├── archetypes/         # Definições Arquetípicas
├── apps/               # Especificações de Apps (Alpha, Geo, etc.)
├── backend/            # Infraestrutura, API, Deploy
├── frontend/           # Documentação do Frontend (Next.js)
└── archive/            # Histórico (NÃO APAGAR, apenas mover para cá)
    ├── v2.1_execution_reports/
    ├── v2.1_full_inventory/
    └── legacy_misc/
```

**Ação Recomendada**: Manter rigorosamente esta separação. Novos docs devem ir para a pasta correta, não para a raiz de `docs/`.

## 2. Estrutura de Código Fonte (`src/`)

A estrutura atual é sólida, mas requer preenchimento de conteúdo:

```text
src/
├── core/               # Master Engine, Pipeline, Orchestrator
├── archetypes/         # Delta144 Engine (Inference)
├── kindras/            # Scoring Engines (L1, L2, L3) + LLM Scorer
├── tw369/              # Drift Engine, Painlevé Solver
├── bias/               # Bias Detector (Precisa de implementação real)
├── meta/               # Meta-Router, Philosophers (Precisa de lógica real)
├── apps/               # App Logic (Alpha, Geo, etc.)
└── datalab/            # Workers (Precisa de implementação real)
```

**Ação Recomendada**:
1.  **`src/datalab/`**: Formalizar estrutura para workers de ingestão.
2.  **`src/bias/`**: Criar subpastas para providers (`src/bias/providers/perspective.py`, etc.).
3.  **`src/kindras/`**: Separar lógica de LLM (`src/kindras/llm/`).

## 3. Estrutura de Schemas (`schema/`)

Manter como está. É a fonte da verdade para mappings.

```text
schema/
├── archetypes/         # Definições JSON dos 12 arquétipos e 144 estados
├── kindras/            # Mappings JSON (L1->Delta, L2->Delta, etc.)
└── tw369/              # Configs de Drift e Painlevé
```

## 4. Limpeza Final (Pós-v2.3)

Após a implementação da v2.3 (LLM real + Embeddings reais), recomenda-se:

1.  **Arquivar** códigos de simulação (ex: gerador de embeddings aleatórios) em uma pasta `src/legacy/simulation/` ou remover completamente.
2.  **Remover** stubs de documentação na raiz de `docs/` se eles não forem mais necessários como redirecionamento.

---
**Conclusão**: A estrutura física do repositório está 90% pronta para a v2.3. O trabalho principal é preencher os "espaços vazios" (stubs) com código real, mantendo a disciplina de onde cada arquivo deve residir.
