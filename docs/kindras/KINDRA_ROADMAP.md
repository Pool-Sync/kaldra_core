# KINDRA 3×48 — Roadmap Oficial de Implementação (v1.0)

## 0. Visão Geral
O sistema Kindra 3×48 fornece os 144 vetores culturais-narrativos que modulam os 144 estados arquetípicos Δ144. Ele opera em três layers alinhados à TW369:

- **Layer 1 (Plano 3)** — Campo cultural superficial (48 vetores)
- **Layer 2 (Plano 6)** — Campo semiótico / midiático (48 vetores)
- **Layer 3 (Plano 9)** — Campo estrutural / civilizacional (48 vetores)

Cada layer precisa de:
- Vetores → OK  
- Documentação → OK  
- Mapas Δ144 → faltando  
- Engine loaders → faltando  
- Scorers → faltando  
- Bridges → faltando  
- TW369 integration → parcial  
- Testes → faltando  

---

# 1. Nível 1 — Dados (Status: 70%)

### O que existe
- `kindra_vectors_layer1_cultural_macro_48.json`
- `kindra_vectors_layer2_semiotic_media_48.json`
- `kindra_vectors_layer3_structural_systemic_48.json`

### O que falta
- Normalização final de IDs, domains, scale_type, scale_direction
- Verificação semântica final

---

# 2. Nível 2 — Mapeamentos Δ144 (Status: 0%)

Necessário criar:
- `kindra_layer1_to_delta144_map.json`
- `kindra_layer2_to_delta144_map.json`
- `kindra_layer3_to_delta144_map.json`

Estrutura:
```json
{
  "VECTOR_ID": {
    "boost": [...],
    "suppress": [...]
  }
}
```

Dependências: lista completa Δ144.

---

# 3. Nível 3 — Loaders (Status: 0%)

Módulos:

```
src/kindras/layer1_cultural_macro_loader.py
src/kindras/layer2_semiotic_media_loader.py
src/kindras/layer3_structural_systemic_loader.py
```

---

# 4. Nível 4 — Scoring Engines (Status: 0%)

Módulos:

```
src/kindras/layer1_cultural_macro_scoring.py
src/kindras/layer2_semiotic_media_scoring.py
src/kindras/layer3_structural_systemic_scoring.py
```

---

# 5. Nível 5 — Bridges Δ144 (Status: 0%)

Módulos:

```
src/kindras/layer1_delta144_bridge.py
src/kindras/layer2_delta144_bridge.py
src/kindras/layer3_delta144_bridge.py
```

Cada um aplica:

```
base_distribution -> adjusted_distribution
```

---

# 6. Nível 6 — Integração TW369 (Status: 30%)

Arquivos necessários:

```
src/tw369/tw369_integration.py
```

TWState deve comportar:

* plane3 (L1)
* plane6 (L2)
* plane9 (L3)

---

# 7. Nível 7 — Pipeline KALDRA Engine (Status: 20%)

Necessário criar:

```
src/core/kaldra_engine_pipeline.py
```

Fluxo:
Δ144 → L1 → L2 → L3 → TW369 → Score final

---

# 8. Nível 8 — Testes (Status: 0%)

Estrutura:

```
tests/kindras/
tests/tw369/
tests/core/
```

---

# 9. Nível 9 — Documentação Final (Status: 80%)

Já existe:

* Layer1 Overview
* Layer2 Overview
* Layer3 Overview
* Master Layers Document

Falta:

* “Kindra Developer Guide”
* “Δ144 Integration Manual”

---

# 10. Sprints

### Sprint 1 — Normalização dos dados

### Sprint 2 — Mapeamentos Δ144

### Sprint 3 — Loaders

### Sprint 4 — Scoring Engines

### Sprint 5 — Bridges

### Sprint 6 — TW369 Integration

### Sprint 7 — Pipeline Engine

### Sprint 8 — Testes

### Sprint 9 — Docs finais

---

# 11. Conclusão

Este Roadmap detalha **tudo o que falta** para que o Kindra 3×48 se torne funcional dentro do KALDRA.
