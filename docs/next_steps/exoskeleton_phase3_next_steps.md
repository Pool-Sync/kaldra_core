# 📘 **KALDRA v3.1 — Exoskeleton Layer — NEXT STEPS DOCUMENT**

**Status:** COMPLETE (Phase 3 Finished)  
**Date:** 2025-12-02

---

## ✅ Overview

A Phase 3 do v3.1 ("Exoskeleton Layer") foi concluída com sucesso:

* **Preset System** completo
* **Profile System** completo
* **PresetRouter** integrado
* **Integração com UnifiedRouter** estável
* **56 testes passando**
* Nenhuma regressão — pipeline intacto
* Infraestrutura pronta para conexão com frontend 4iam.ai

Este documento registra:

* Próximas melhorias
* Refinamentos esperados
* Itens para v3.2, v3.3, v3.4 e v3.6 (unificação final)
* O que falta testar manualmente
* Pontos de atenção para o GEM (UI/UX + Architect)

---

## 🚀 **Future Implementations (High Priority)**

### 1. **Preset Weight Propagation (para Orchestrator)**

Hoje os presets definem `emphasis`, mas essa ênfase ainda não cria pesos reais nos estágios do pipeline.
É necessário:

* Criar `EngineWeightConfig`
* Integrar no Orchestrator para modificar:
  * MetaStage weight
  * Kindra weight
  * Δ144 weight
  * TW369 sensitivity
* Gerar `PipelineWeights` no `UnifiedContext`

➡️ Migrar isso para v3.2–v3.3.

---

### 2. **Persistência Real de Profiles (DB)**

Atualmente:

* JSON local
* Sem versionamento
* Sem migração
* Sem sync com API

Precisamos:

* Conectar com modelo **User** do backend (FastAPI)
* Permitir perfis multi-dispositivo
* Registrar histórico de presets usados

➡️ Mover para v3.4 (junto com Explainability e API 2.0).

---

### 3. **Preset Overrides Avançados**

Faltam:

* Regras condicionais (`if drift > threshold → apply X`)
* Emphasis dinâmica por domínio (finance, geo, brand)
* Overlays predefinidos (e.g., "High-Volatility Mode")

➡️ Mover para v3.3–v3.6.

---

### 4. **Exoskeleton → StoryStage integration (v3.2)**

Para a phase 4 TW369 + StoryStage:

* Exoskeleton deve fornecer:
  * Heurísticas temporais
  * Sensibilidade a drift
  * Profundidade narrativa

Necessário sincronizar com:

* Story Buffer
* Arc Detector
* Timeline Builder

➡️ Dependência direta com v3.2.

---

### 5. **Preset Recomender (v3.6)**

Utilizando:

* Perfil do usuário
* Histórico de narrativas
* Temperatura emocional do input
* Domínio (finance, geo, product)

Calcular automaticamente:

* Melhor preset
* Melhor weight distribution
* Modo ideal (signal/full/story)

➡️ Planejado apenas para v3.6 (Convergence Layer).

---

## 🔧 **Enhancements (Short Term)**

### 1. Normalize Profile Keys

Garantir padronização:

* `risk_tolerance`
* `preferred_preset`
* `output_format`
* `depth`
* `emphasis_overrides`

### 2. Add Validation Layers

Para:

* Thresholds fora de range
* Emphasis inválida
* Preset inexistente
* Perfil incompleto

### 3. Add Preset Versioning

Permitir:

```json
{
  "preset": "alpha",
  "version": "3.1.0"
}
```

Facilita retrocompatibilidade.

---

## 🔧 **Enhancements (Medium Term)**

### 1. Snapshot-based Preset Diff Viewer

Ajuda no debugging:

* Comparar presets antes/depois
* Mostrar overrides do usuário

### 2. Dynamic Preset Parameters

Permitir presets que reagem ao input:

* Drift elevado → reforçar Meta
* Conflito elevado → aumentar Kindra Layer2
* Discussão emocional → aumentar Δ12

### 3. Full Integration with 4iam.ai UI

Com:

* Dropdown de presets
* Visualização de perfil
* Preview das ênfases
* Heatmap configurável

---

## 🔬 **Research Track (Long Term)**

### 1. Learned Preset Synthesis

Sistema aprende novos presets automaticamente:

* Clustering de inputs
* Agrupamento de padrões

### 2. User Adaptive Preset Evolution

Cada perfil evolui sozinho baseado em:

* Narrativas que o usuário envia
* Domínio mais utilizado
* Tolerância ao risco

### 3. Hyper-Presets (v3.6)

Preset híbrido:

* Meta + Kindra + Story + TW369
* Ajustado dinamicamente a cada input

### 4. Preset + Story Arc Coupling

No v3.2:

* StoryStage envia sinais temporais para o Exoskeleton
* Exoskeleton adapta configuração ao longo do tempo

---

## ⚠️ **Known Limitations**

1. Persistência via JSON, não DB
2. Emphasis não ligada ao Orchestrator ainda
3. Router não exibe warnings detalhados
4. Profiles não possuem histórico temporal
5. Não há presets adaptativos ainda
6. Não há preset recommendation engine

---

## 🧪 **Testing Status**

### Status atual:

* **56 testes passando**
* **Nenhuma regressão**
* **PresetRouter validado em 17 cenários**
* **ProfileManager testado com persistência real (tmp_path)**

### Faltam testes:

* E2E real com UnifiedKaldra.analyze()
* E2E com StoryStage e TW369 (v3.2)
* API testing (v3.4)
* Performance profile switching under load

---

## 📍 **Next Steps (Immediate)**

### 1. Criar **docs/next_steps/phase4_next_steps.md**

Para a nova fase:

* Story Buffer
* Arc Detection
* TW369 Topological Deepening

### 2. Criar Execution Orders:

* StoryStage v3.2
* TW369 v3.2 Integration
* Story Buffer
* Arc Detector
* Timeline Builder
* Coherence Scorer

### 3. Conectar Preset → Temporal Intelligence

* Adicionar preset hooks para StoryStage
* Mapear presets para modos temporais ("story", "full")

### 4. Criar API v3.1 endpoints para o frontend

* `/presets`
* `/profiles`
* `/analyze?preset=...&profile=...`

---

## 🎉 **Conclusion**

A Phase 3 do v3.1 está 100% concluída.
Presets + Profiles + PresetRouter estão estáveis, robustos e prontos para uso real no 4iam.ai.

A engine agora possui um **Exoskeleton sólido** — a fundação perfeita para as próximas fases:

* **v3.2: Temporal Mind**
* **v3.3: Multi-Stream**
* **v3.4: Explainable**
* **v3.6: Convergence**
