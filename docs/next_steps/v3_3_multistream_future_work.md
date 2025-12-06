# KALDRA v3.3 — Multi-Stream Layer Future Work & Enhancements (Post-Phase 3)

**Version:** v3.3  
**Component:** Multi-Modal Layer → Multi-Stream Narratives  
**Status:** Phase 1–3 Complete  
**Document Purpose:** Registrar tudo que ainda falta, melhorias futuras, riscos técnicos e pontos de integração pendentes.

---

## 1. Overview

As três fases do Multi-Stream Layer v3.3 foram concluídas com sucesso:

- **Phase 1** — Multi-Modal Input ✅
- **Phase 2** — Multi-Stream Narrative Engine ✅
- **Phase 3** — Pipeline Integration ✅

Este documento descreve **tudo que ficou pendente por design**, além de otimizações e integrações futuras necessárias para transformar o Multi-Stream Layer em um sistema completo, escalável, observável e pronto para API exposure no v3.4/v3.5.

---

## 2. Work Remaining (High Priority)

### 2.1 Automatic Stream Detection in Pipeline (NOT IMPLEMENTED)

Hoje, `stream_id` só flui para StoryEvent **se o InputMetadata já contiver um stream_id**.

Mas o pipeline não:
- Deduz automaticamente a origem
- Não identifica múltiplas fontes em um único documento
- Não propaga stream_id para eventos subsequentes

#### Required Improvements

- Implementar módulo: `src/unification/pipeline/stream_resolver.py`
- Inferência automática:
  - Via URL
  - Via domínio
  - Via headers
  - Via tags internas
- Preencher stream_id quando ausente, com classificação heurística

---

### 2.2 MultiStreamStage → Full Pipeline Wiring (PARTIAL)

Embora MultiStreamStage esteja implementado e testado, ele ainda **não está ligado oficialmente ao Master Pipeline**.

#### Required Improvements

- Integrar MultiStreamStage logo após StoryStage
- Criar chave de configuração global: `"multistream.enabled": true | false`
- Criar wrapper no Orchestrator
- Validar impacto de performance quando habilitado

---

### 2.3 Cross-Stream → StoryStage Alignment (NOT COMPLETED)

Atualmente MultiStreamStage analisa apenas eventos agregados, mas StoryStage:
- Não entrega múltiplos eventos por execução
- Não extrai automaticamente janelas por stream

#### Required Enhancements

- StoryStage deve enviar eventos para MultiStreamBuffer de maneira incremental
- Criar método: `story_stage.get_events_by_stream()`

---

## 3. Future Features (Medium Priority)

### 3.1 StoryArc Divergence Metric (PLANNED — NOT IMPLEMENTED)

Hoje divergência é apenas:
- Archetype divergence
- Polarity divergence

Mas um dos maiores objetivos do sistema é: **Comparar padrões narrativos entre streams**, detectando se diferentes fontes estão em diferentes partes da Jornada do Herói.

#### Required Features

- Novo módulo: `stream_arc_analyzer.py`
- Inputs necessários:
  - `StoryTimeline` por stream
  - `StoryArc` por stream
- Métrica planejada: `stage_divergence ∈ [0, 1]`
- Atualizar StreamComparisonResult com estágio real: `stage_divergence: float`

---

### 3.2 Multi-Stream Context Exposure in API (NOT IMPLEMENTED)

Nenhum dado do Multi-Stream Layer aparece no SignalAdapter ou API v3.1+.

Por design, o backend está pronto, mas o frontend e API não sabem que isso existe.

#### Required API Additions

To be done in v3.4:

**Campos novos no sinal:**

```json
"multi_stream": {
  "active_streams": [...],
  "pairwise_divergence": {...},
  "max_divergence": 0.84,
  "convergent": false
}
```

**Endpoints:**

- `GET /api/v3.x/multistream/summary`
- `GET /api/v3.x/multistream/stream/{id}`

---

### 3.3 Performance Optimization (NOT COMPLETED)

O algoritmo atual tem:
- **Buffer O(N)**
- **Comparação O(N²)**

Em 10 streams → ok  
Em 50 streams → borderline  
Em 100 streams → inviável

#### Required Optimizations

- Introduzir caching para janelas inalteradas
- Paralelizar comparação via multiprocessing
- Substituir comparação total por amostragem
- Adicionar threshold para ignorar pares com baixa relevância
- Criar módulo: `parallel_stream_comparator.py`

---

### 3.4 Historical Tracking (NOT IMPLEMENTED)

Atualmente tudo é in-memory.

Nenhum histórico é mantido para:
- Análise longitudinal
- Timeseries de divergência
- Detecção de convergência/divergência ao longo do tempo
- Persistência para auditoria

#### Required Enhancements

- Criar `MultiStreamHistory`
- Persistência opcional (SQLite, parquet, Redis)
- Acoplamento com StoryStage para sincronizar eventos históricos

---

## 4. Testing Gaps (Future Work)

Apesar da excelente cobertura (29 testes passando), alguns testes futuros são necessários:

### 4.1 Stress Testing

- Simular 20 streams × 1000 eventos
- Medir latência do comparator
- Medir overflow do buffer

### 4.2 Parallel Comparator Tests (after implementation)

### 4.3 Integration with StoryStage real-time window updates

### 4.4 Integration with CampbellEngine temporal metrics (v3.4)

---

## 5. Limitations to Address

These are **known technical limitations** from this phase:

1. No API exposure
2. No frontend usage
3. No timestamp alignment between streams
4. No narrative arc divergence
5. No persistence layer
6. O(N²) divergence computation
7. StoryStage still single-stream for most operations
8. Stream detection is manual, not inferred

---

## 6. Next Versions — Official Placement of Work

| Version | Feature |
|---------|---------|
| **v3.4** | API Exposure + Stage Divergence |
| **v3.4** | Pipeline full wiring |
| **v3.5** | Persistence & Historical Multi-Stream Memory |
| **v3.5** | Parallel divergence computation |
| **v3.6** | Predictive multi-stream evolution ("Narrative Vector Field") |

---

## 7. Final Summary

This Future Work document defines everything still pending for the Multi-Stream Layer.

Phase 1, Phase 2 e Phase 3 estão **completamente concluídas**, mas a evolução natural do sistema exige:

### 🔥 HIGH PRIORITY (Next Sprint)

- Auto stream detection
- Pipeline full wiring
- Arc divergence metric
- API exposure

### 🧠 MEDIUM PRIORITY

- Temporal alignment
- StoryStage multi-stream extraction

### 🐉 LONG TERM

- Persistent multi-stream memory
- Predictive convergence/divergence
- Parallel computation scaling

---

## Related Documentation

- [Multi-Modal Input (Phase 1)](file:///Users/niki/Desktop/kaldra_core/docs/multistream/MULTIMODAL_INPUT_v3_3_PHASE_1.md)
- [Multi-Stream Narratives (Phase 2)](file:///Users/niki/Desktop/kaldra_core/docs/multistream/MULTI_STREAM_NARRATIVES_v3_3_PHASE_2.md)
- [Multi-Stream Integration (Phase 3)](file:///Users/niki/Desktop/kaldra_core/docs/multistream/MULTI_STREAM_INTEGRATION_v3_3_PHASE_3.md)
- [KALDRA v3.3 Roadmap](file:///Users/niki/Desktop/kaldra_core/docs/roadmaps/KALDRA_V3_3_MULTI_STREAM.md)
