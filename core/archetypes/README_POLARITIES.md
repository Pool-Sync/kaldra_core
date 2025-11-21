# README — Polaridades do Sistema KALDRA

**Arquivo**: `polarities.json`  
**Local**: `kaldra/core/archetypes/`  
**Status**: Fonte de verdade — imutável para Antigravity

---

## 🧬 1. O que são as Polaridades KALDRA?

**Polaridades** são eixos fundamentais de tensão simbólica, emocional, cognitiva, cultural ou existencial.

Elas representam **forças opostas** que estruturam o comportamento humano, narrativas, culturas e arquétipos.

No KALDRA, polaridades:
- funcionam como **eixos universais de avaliação narrativa**
- alimentam **Tw369, Δ144, Modifiers, Bias Engine, Kindras**
- expressam **tensões, drifts e instabilidades**
- formam o **campo de leitura simbólica total** do sistema

São o **mapa de forças** que operam dentro de qualquer texto, discurso, mercado, cultura ou evento geopolítico.

---

## 🧩 2. Por que um arquivo separado?

Porque polaridades:
- são **transversais** (não pertencem a um arquétipo)
- são **atemporais** (não mudam com cultura)
- são **cognitivamente estáveis**
- são utilizadas por **todos os motores** (Alpha, GEO, Product, Safeguard)

E principalmente:

> **Antigravity exige um arquivo de referência único, imutável e determinístico** para todas as tasks do ecossistema.

`polarities.json` cumpre exatamente este papel.

---

## 🔢 3. Quantas polaridades existem?

Este arquivo contém **48 polaridades**, que representam:

- 10 eixos fundamentais (núcleo universal)
- 14 eixos emocionais
- 12 eixos cognitivos
- 6 eixos culturais
- 6 eixos de jornada/arquetípicos

**Total**: 48 polaridades (3×16)

→ perfeito para mapear em **Kindras 3×48** se necessário.

---

## 🧱 4. Estrutura do Arquivo

Cada polaridade segue este esquema:

```json
{
  "id": "POL_XYZ",
  "label": "NomeA ↔ NomeB",
  "description": "Descrição do eixo e sua função simbólica.",
  "dimension": "categoria_semântica",
  "tw_alignment": ["3", "6", "9"]
}
```

### Campos:

| Campo | Função |
|-------|--------|
| `id` | Identificador imutável usado no Antigravity e nos engines |
| `label` | Nome humano do eixo (A ↔ B) |
| `description` | Explica o significado e aplicação narrativa |
| `dimension` | Classificação: `existential`, `cognition`, `culture`, `energy`, etc. |
| `tw_alignment` | Quais planos TW369 estão relacionados ao eixo |

---

## 🎛 5. Como os motores usam Polaridades?

### Δ144 Engine
- reforça ou enfraquece certos estados
- ajusta Modifiers
- define direção narrativa (Expansão, Contração, Metanoia)

### TW369 Engine
Polaridades são usadas como:
- sinais de **drift**
- marcadores de **instabilidade**
- indicadores de **recalibração de plano dominante**

### Kindra 3×48 Engine
Polaridades funcionam como:
- camada semântica superior
- rastreadores culturais de alta resolução
- interpretadores de tom e etiqueta cultural

### Safeguard Engine
Polaridades são cruciais para:
- detectar narrativas tóxicas
- identificar manipulação emocional
- projetar riscos simbólicos

### KALDRA-Alpha / GEO / Product
Polaridades aparecem em:
- mapas arquetípicos setoriais
- relatórios de earnings calls
- leitura geopolítica de tensão civilizacional
- diagnóstico de UX/Produto (KALDRA-PRODUCT)

---

## 🧠 6. Como as polaridades se ligam a TW369?

Cada polaridade possui um campo:

```json
"tw_alignment": ["3", "6", "9"]
```

Isso diz:
- **Plano 3**: Ação, expansão, declaração
- **Plano 6**: Defesa, tensão, contração
- **Plano 9**: Metanoia, invisibilidade, transcendência

O motor TW369 usa isso para:
- projetar o texto em planos de vibração
- inferir shifts emocionais
- mapear segurança vs. risco narrativo
- amplificar símbolos em momentos críticos

---

## 📡 7. Como elas se ligam aos 144 estados?

Cada estado do Δ144 tem:
- `profile` (EXPANSIVE / CONTRACTIVE / TRANSCENDENT)
- `tw_plane_default` (3/6/9)
- `allowed_modifiers`
- `default_modifiers`

As polaridades fornecem:
- **vetores de força**
- **eixos de leitura emocional**
- **potenciais de sombra/luz**
- **direção narrativa**

Um mesmo estado pode ser interpretado de forma diferente dependendo da **ativação polar** (ex.: Ordem vs. Caos, Confiança vs. Suspeita).

---

## 🧨 8. Por que 48 polaridades?

Porque o KALDRA trabalha com:

**3 planos × 16 eixos = 48**

Perfeito para:
- Kindras 3×48
- Δ48 dentro da Δ144
- compatibilidade com Sinais KALDRA
- topologia narrativa fractal
- balanceamento entre motores

---

## 🔐 9. Regra Antigravity — IMUTÁVEL

Este arquivo:
- ❌ **não deve ser alterado**
- ❌ **não deve ter IDs trocados**
- ❌ **não deve ter labels modificados**
- ❌ **não deve deletar polaridades**
- ❌ **não deve reordenar nada**

Apenas é permitido **adicionar novas polaridades**, e ainda assim somente se:

> Não criar conflito de semântica com TW369 ou Δ144.

---

## 🧵 10. Exemplo de Uso (Jules)

```python
from kaldra.core.archetypes import polarities

for pol in polarities:
    print(pol["id"], pol["tw_alignment"])
```

### Em engines:

```python
if polarity_score["POL_TRUST_SUSPICION"] > 0.7:
    modifier_scores["MOD_CAUTIOUS"] += 0.3
```

### Em Sinais KALDRA:

```
Δ144: Ruler_6_05 (Governante Defensivo)
Polaridade dominante: Confiança ↔ Suspeita (alto lado Suspeita)
TW: Plano 6 ↑
Resultado: Risco narrativo ↑
```

---

## 🧭 11. Conclusão

`polarities.json` é:
- o **esqueleto emocional e cognitivo** do sistema
- o **atlas das tensões arquetípicas**
- a **ponte entre TW369, Δ144 e Kindras**
- a **referência fixa para Antigravity**

**Sem ele, os motores não conseguem calibrar deriva, risco, sombra, metanoia ou coerência.**

---

## 📊 Dimensões e Distribuição

| Dimensão | Polaridades | Exemplos |
|----------|-------------|----------|
| `affect` | 7 | Confiança↔Suspeita, Coragem↔Medo, Calma↔Ansiedade |
| `cognition` | 6 | Análise↔Intuição, Foco↔Dispersão, Certeza↔Dúvida |
| `structure` | 5 | Ordem↔Caos, Hierarquia↔Rede, Rigidez↔Flexibilidade |
| `culture` | 5 | Local↔Global, Honra↔Vergonha, Ritual↔Pragmático |
| `identity` | 4 | Individual↔Coletivo, Autonomia↔Dependência |
| `journey` | 4 | Chamado↔Recusa, Descida↔Subida, Sacrifício↔Recompensa |
| `will` | 4 | Controle↔Entrega, Dominação↔Serviço |
| `energy` | 3 | Expansão↔Contração, Fluxo↔Bloqueio, Impulso↔Apatia |
| `ethic` | 3 | Responsabilidade↔Culpa, Integridade↔Fragmentação |
| `existential` | 3 | Luz↔Sombra, Sentido↔Vazio, Esperança↔Desespero |
| `presence` | 2 | Presença↔Ausência, Visível↔Invisível |
| `evolution` | 1 | Metanoia↔Estagnação |
| `alchemical` | 1 | Criação↔Destruição |

**Total**: 48 polaridades
