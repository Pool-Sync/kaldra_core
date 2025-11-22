# 📘 Δ144 Engine — Mecanismo Arquetípico do Sistema KALDRA

O **Δ144 Engine** é o coração simbólico e dinâmico do Sistema KALDRA.

Ele transforma sinais linguísticos, culturais, estatísticos e narrativos em **estados arquetípicos vivos**, aplicando:

- a matriz **Δ144** (12 arquétipos × 12 estados)
- **TW369** (planos psico-dinâmicos 3, 6, 9)
- **Modifiers dinâmicos** (62 vetores emocionais/estruturais)
- Integração com **Kindras 3×48** (vetores culturais)

O objetivo do engine é responder a uma única pergunta:

> **"Qual é o estado arquetípico real por trás do discurso, texto ou comportamento observado?"**

---

## 🧬 1. Arquitetura Geral

O Δ144 Engine recebe sinais já agregados (numéricos) de outros módulos:

```
TEXT → Bias Engine → Embeddings → TW369 Engine → Kindra Engine → Δ144 Engine
```

**O próprio Δ144 não faz NLP.**

Ele é o **tradutor simbólico** que recebe esses sinais e devolve:

- o **arquétipo dominante** (Axx)
- o **estado específico** dentro da matriz Δ144
- **modifiers dinâmicos**
- **scores completos**

---

## 🔢 2. Arquivos de Dados Necessários

O Δ144 depende dos seguintes arquivos JSON:

```
archetypes_12.core.json         (12 arquétipos)
delta144_states.core.json       (144 estados: Axx_3_01 … Axx_9_12)
archetype_modifiers.core.json   (62 modifiers)
```

Todos devem estar na mesma pasta:

```
kaldra/core/archetypes/
```

---

## 🧱 3. Estrutura da Matriz Δ144

A matriz Delta é formada por:

### **12 Arquétipos** (linhas)

1. **Criador**
2. **Sábio**
3. **Mago**
4. **Herói**
5. **Explorador**
6. **Cuidador**
7. **Governante**
8. **Rebelde**
9. **Amante**
10. **Inocente**
11. **Trickster**
12. **Oráculo**

→ Definidos em `archetypes_12.core.json`.

### **12 Estados** (colunas)

Cada arquétipo se manifesta através de um ciclo fixo:

#### **4 Expansivos** (Plano 3 → ação)
1. Iniciador
2. Visionário
3. Acelerador
4. Potencializador

#### **4 Contrativos** (Plano 6 → defesa/tensão)
5. Defensivo
6. Reativo
7. Conservador
8. Retraído

#### **4 Transcendentes** (Plano 9 → metanoia/evolução)
9. Liminal
10. Sombra Revelada
11. Metanoico
12. Transcendente

→ Cada arquétipo × cada estado = **144 células**.  
→ Cada célula tem um `tw_plane_default` (3, 6 ou 9) + modifiers padrão.

---

## 🎛 4. Como o Engine Funciona

O processo de inferência segue:

### **1. Recebe scores numéricos:**

```python
plane_scores     = {"3": x, "6": y, "9": z}
profile_scores   = {"EXPANSIVE": a, "CONTRACTIVE": b, "TRANSCENDENT": c}
modifier_scores  = {"MOD_SHADOW": 0.8, ...}
```

### **2. Normaliza scores**
- Ajusta pesos
- Garante que somem 1.0

### **3. Seleciona o perfil dominante**
- (EXPANSIVE / CONTRACTIVE / TRANSCENDENT)

### **4. Filtra os estados do arquétipo apenas desse perfil**

### **5. Calcula um score para cada estado, usando:**
- aderência ao TW-plane
- coerência com perfil dominante
- leve ruído ordenado (colunas) para desempate

### **6. Escolhe o estado vencedor**

### **7. Ativa modifiers dinâmicos, com regras:**
- começa pelos defaults
- adiciona modifiers com score acima de threshold
- limita a máx. 4 modifiers simultâneos

### **8. Retorna um `StateInferenceResult` completo**

---

## 🧩 5. Exemplo Completo de Uso

```python
from pathlib import Path
from kaldra.core.archetypes.delta144_engine import Delta144Engine

base = Path("kaldra/core/archetypes")
engine = Delta144Engine.from_default_files(base)

result = engine.infer_state(
    archetype_id="A07_RULER",
    plane_scores={"3": 0.2, "6": 0.6, "9": 0.2},
    profile_scores={"EXPANSIVE": 0.1, "CONTRACTIVE": 0.7, "TRANSCENDENT": 0.2},
    modifier_scores={
        "MOD_DEFENSIVE": 0.8,
        "MOD_INSTITUTIONAL": 0.6,
        "MOD_SHADOW": 0.3
    }
)

print(result.to_dict())
```

### **Retorno:**

```json
{
  "archetype": {...},
  "state": {
    "id": "A07_RULER_6_05",
    "label": "Governante Defensivo",
    ...
  },
  "active_modifiers": [
    {"id": "MOD_DEFENSIVE", "label": "Defensivo", ...},
    {"id": "MOD_INSTITUTIONAL", ...}
  ],
  "scores": {...}
}
```

---

## 🧠 6. Como Integrar TW369 + Δ144

**TW369 entrega:**

- Plano dominante: 3 / 6 / 9
- Drift: deslocamento entre planos
- Instabilidade narrativa
- Polaridade energética
- Forças culturais associadas a cada frequência

**O Δ144 Engine usa TW369 assim:**

```
TW369 → plane_scores
TW369 → profile_scores
TW369 → modifier_scores (tensão emocional / risco / sombra)
```

### **Exemplos:**

- **Plano 6 ↑** → estados contrativos ganham mais peso
- **Drift 3→6** → aumenta `MOD_DEFENSIVE` / `MOD_REACTIVE`
- **Frequência 9 dominante** → favorece estados transcendentes

---

## 🌐 7. Como Integrar Kindras (3×48)

**Kindras atuam como filtro cultural/comportamental:**

- **Função:** ajustar modifiers por cultura, contexto e estilo narrativo.
- **Saída do Kindra Engine** → alimenta `modifier_scores`.

### **Exemplos:**

- **K42 (Boundary Terms) ↑** → favorece `MOD_DEFENSIVE`, `MOD_INSTITUTIONAL`
- **K19 (Ruptura Criativa) ↑** → favorece `MOD_CHAOTIC`, `MOD_VOLATILE`
- **K02 (Afeto Direto) ↑** → favorece `MOD_RADIANT`, `MOD_SYMBIOTIC`

---

## ⚙️ 8. Estrutura Interna do Código

O engine contém:

- `Archetype`
- `ArchetypeState`
- `Modifier`
- `StateInferenceResult`

E a classe principal:

### **`Delta144Engine`**

- `.infer_state()`
- `.get_archetype()`
- `.get_state()`
- `.list_states_for_archetype()`
- `.from_default_files()`

Tudo **100% desacoplado, modular, testável**.

---

## 🧪 9. Como Antigravity Deve Testar

### **Testar cada arquétipo com vários perfis:**
- EXPANSIVE / CONTRACTIVE / TRANSCENDENT

### **Testar coerência TW-plane:**
- Plano 3 → estados com `tw_plane_default=3` devem subir

### **Forçar vários modifiers:**
- Sombra
- Coletivo
- Volátil

### **Testar estabilidade:**
- Mesmos inputs → mesmo state

### **Testar ruído:**
- Pequena variação → mudança coerente de state (não caos)

---

## 📦 10. Próximos Módulos Dependentes

Depois do Δ144 Engine, vêm:

1. **TW369 Engine**
2. **Bias Normalization Engine**
3. **KALDRA Core Engine** (fusão TW369 + Kindras + Δ144)
4. **Earnings Engine** (KALDRA-Alpha)
5. **Geo Engine** (KALDRA-GEO)
6. **Product Engine** (KALDRA-PRODUCT)
7. **SafeGuard Engine**
8. **Sinal KALDRA** (schema oficial)

---

## 🏁 Conclusão

O **Δ144 Engine** transforma sinais em estados arquetípicos vivos, com sofisticada lógica simbólica e cultural.

Ele é a **espinha dorsal do KALDRA** — tudo o que vem depois (Alpha, GEO, Product, Safe) depende dele.

**É o cérebro simbólico do ecossistema.**

---

**Última atualização:** 2025-11-22  
**Versão:** 1.0
