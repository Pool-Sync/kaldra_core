# KINDRA Layer 3 — Cultural Estrutural / Sistemas (48 Vetores)

## 0. Visão Geral

O **Layer 3 — Structural / Systemic** representa o plano mais profundo da arquitetura Kindra 3×48.  
Enquanto:

- **Layer 1 (Plano 3)** modela comportamento visível e clima cultural,  
- **Layer 2 (Plano 6)** modela força semiótica, mídia, tensão e deriva narrativa,  

o **Layer 3 (Plano 9)** define:

- estruturas civilizacionais  
- instituições  
- macro-poder  
- traumas históricos  
- ordem social  
- memória profunda  
- rigidez ou fluidez sistêmica  
- capacidade de colapso / resiliência  
- densidade narrativa estrutural  

É o layer responsável pela **gravidade simbólica**: aquilo que puxa narrativas sempre de volta para as estruturas profundas.

- **Escopo**: 48 vetores estruturais  
- **TW-plane**: `9` (profundidade, estrutura, fundações, raízes)  
- **Arquivo de dados**:  
  `schema/kindras/kindra_vectors_layer3_structural_systemic_48.json`

---

## 1. O que o Layer 3 mede

O Layer 3 mede **forças estruturantes**, agrupadas em:

### **1. Estruturas de Poder**
- concentração de elite  
- estratificação  
- densidade institucional  
- rigidez civilizacional  

### **2. Memória e Trauma Histórico**
- traumas coletivos não integrados  
- memórias de conflito  
- fatalismo cultural  
- cicatrizes civilizacionais  

### **3. Núcleo Econômico**
- concentração econômica  
- estabilidade estrutural  
- dependência externa  
- rigidez econômica  

### **4. Ordem Sociopolítica**
- coerência sistêmica  
- tensão estrutural  
- níveis de governabilidade  
- alinhamento civilizacional  

### **5. coesão cultural profunda**
- continuidade histórica  
- tradição  
- estruturas míticas profundas  
- identidade civilizacional  

### **6. Estruturas de Sistema**
- redundância  
- resiliência  
- capacidade de reconstrução  
- pressão demográfica/territorial  

Esses vetores determinam o **grau de estabilidade, risco, ressonância e lentidão/rapidez das narrativas** no plano mais profundo do KALDRA.

---

## 2. Estrutura de Dados

Arquivo:

```
schema/kindras/kindra_vectors_layer3_structural_systemic_48.json
```

Formato de cada vetor:

```jsonc
{
  "id": "X01",
  "layer": "L3_STRUCTURAL_SYSTEMIC",
  "domain": "POWER_SYSTEM",
  "tw_plane": "9",
  "scale_type": "spectrum",
  "scale_direction": "high = concentração de poder",
  "weight": 1.0,
  "short_name": "Concentração de Elite",
  "objective_definition": "...",
  "examples": [...],
  "narrative_role": "..."
}
```

Campos obrigatórios:

* `layer`: sempre `"L3_STRUCTURAL_SYSTEMIC"`
* `tw_plane`: `"9"`
* `domain`: POWER_SYSTEM, TRAUMA_HISTORY, ECONOMIC_CORE, ORDER_SYSTEM, IDENTITY_CORE, SYSTEM_RESILIENCE, etc.
* `scale_type`: spectrum | binary | index
* `weight`: 1.0
* `archetype_link`: reservado para Δ144
* `narrative_role`: impacto sobre narrativa profunda

---

## 3. Ligação com Δ144

### 3.1. Como o Layer 3 modifica Δ144

O Layer 3 altera:

* **estabilidade dos estados**
* **velocidade de transição entre estados**
* **probabilidade de colapso ou expansão**
* **peso relativo de arquétipos estruturais (Governante, Guardião, Sábio, Profeta)**
* **modo sombra estrutural (Corrupção, Ruína, Colapso, Traumático)**

Exemplo conceitual:

```jsonc
{
  "X04": {
    "boost": ["SAGE_LIGHT", "RULER_LIGHT", "GUARDIAN_LIGHT"],
    "suppress": ["OUTLAW_LIGHT", "TRICKSTER_LIGHT", "MAGICIAN_LIGHT"]
  }
}
```

### 3.2. Arquivo necessário (a criar)

```
schema/kindras/kindra_layer3_to_delta144_map.json
```

---

## 4. Relação com TW369 e Quiralidade

### **4.1. TW-plane 9**

Plano 9 representa:

* profundidade
* ordem estrutural
* civilização
* trauma acumulado
* raiz simbólica
* destino narrativo

No TW engine:

```python
tw_state = TWState(
    plane3_cultural_macro = ...,
    plane6_semiotic_media = ...,
    plane9_structural_systemic = layer3_vector
)
```

### **4.2. Quiralidade**

* Layer 1 (3): comportamento
* Layer 2 (6): tensão → conflito → transformação
* **Layer 3 (9): destino → estabilidade → colapso → reconstrução**

Layer 3 é responsável por:

* estabilizar ou desestabilizar Δ144
* definir se “deriva vira colapso”
* transformar crises em ciclo longo
* operar “pontos fixos” narrativos

---

## 5. Implementação em Código

### 5.1. Arquivos existentes

* `schema/kindras/kindra_vectors_layer3_structural_systemic_48.json`

### 5.2. Arquivos necessários (a criar)

1. Loader:

```
src/kindras/layer3_structural_systemic_loader.py
```

2. Scoring:

```
src/kindras/layer3_structural_systemic_scoring.py
```

3. Bridge com Δ144:

```
src/kindras/layer3_delta144_bridge.py
```

4. Map file:

```
schema/kindras/kindra_layer3_to_delta144_map.json
```

5. Testes:

```
tests/kindras/test_layer3_structural_systemic.py
tests/kindras/test_layer3_delta144_bridge.py
```

---

## 6. Função Narrativa Profunda

Layer 3 define:

* **o peso da história**
* **a resiliência ao caos**
* **a capacidade de renascer ou colapsar**
* **o ritmo lento e profundo das transições Δ144**
* **o campo gravítico da narrativa**

É aqui que se define:

* se uma narrativa pode mudar rápido
* se narrativas sombrias se perpetuam
* se crises viram trauma ou renascimento
* se arquétipos visionários conseguem emergir

Layer 3 é o **esqueleto civilizacional** do KALDRA.

---

## 7. Resumo Operacional

**Entrada**: métricas estruturais profundas
**Processo**:

1. Carregar vetores layer3
2. Produzir vetor de intensidade
3. Ajustar Δ144 (estabilidade, colapso, rigidez)
4. Alimentar TW369 no plano 9

**Saída**: estados Δ144 consolidados ou tensionados por estruturas profundas.

Este é o documento de referência oficial para implementação do **Layer 3 — Structural / Systemic**.
