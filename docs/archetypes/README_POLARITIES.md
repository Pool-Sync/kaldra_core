# 📘 README — Polaridades do Sistema KALDRA

**Arquivo:** `polarities.json`  
**Local:** `kaldra/core/archetypes/`  
**Status:** Fonte de verdade — imutável para Antigravity

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

> **Antigravity exige um arquivo de referência único, imutável e determinístico para todas as tasks do ecossistema.**

`polarities.json` cumpre exatamente este papel.

---

## 🔢 3. Quantas polaridades existem?

Este arquivo contém **49 polaridades**, que representam:

| Dimensão | Quantidade | Exemplos |
|----------|------------|----------|
| **Existencial** | 3 | Luz/Sombra, Sentido/Vazio, Esperança/Desespero |
| **Estrutura** | 5 | Ordem/Caos, Centro/Periferia, Hierarquia/Rede, Rigidez/Flexibilidade, Simplicidade/Complexidade |
| **Energia** | 3 | Expansão/Contração, Fluxo/Bloqueio, Impulso/Apatia |
| **Evolução** | 1 | Metanoia/Estagnação |
| **Identidade** | 4 | Individual/Coletivo, Autenticidade/Conformismo, Autonomia/Dependência, Enraizamento/Deslocamento |
| **Alquímica** | 1 | Criação/Destruição |
| **Presença** | 2 | Visível/Invisível, Presença/Ausência |
| **Cognição** | 6 | Racional/Mítico, Análise/Intuição, Foco/Dispersão, Convergente/Divergente, Literal/Simbólico, Certeza/Dúvida |
| **Afeto** | 7 | Estabilidade/Volatilidade, Confiança/Suspeita, Conexão/Isolamento, Abertura/Repressão, Coragem/Medo, Calma/Ansiedade, Compaixão/Indiferença |
| **Vontade** | 4 | Controle/Entrega, Dominação/Serviço, Impulsividade/Disciplina, Ressentimento/Afirmação |
| **Cultura** | 5 | Ritualístico/Pragmático, Honra/Vergonha, Alta/Baixa-Contextualização, Hierárquico/Horizontal, Local/Global |
| **Jornada** | 4 | Chamado/Recusa, Teste/Retraimento, Sacrifício/Recompensa, Descida/Subida |
| **Ética** | 3 | Dever/Evasão, Responsabilidade/Culpa, Integridade/Fragmentação |

**Total: 49 polaridades**

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

### **Δ144 Engine**
- reforça ou enfraquece certos estados
- ajusta Modifiers
- define direção narrativa (Expansão, Contração, Metanoia)

### **TW369 Engine**
Polaridades são usadas como:
- sinais de **drift**
- marcadores de **instabilidade**
- indicadores de **recalibração de plano dominante**

### **Kindra 3×48 Engine**
Polaridades funcionam como:
- camada semântica superior
- rastreadores culturais de alta resolução
- interpretadores de tom e etiqueta cultural

### **Safeguard Engine**
Polaridades são cruciais para:
- detectar **narrativas tóxicas**
- identificar **manipulação emocional**
- projetar **riscos simbólicos**

### **KALDRA-Alpha / GEO / Product**
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

O motor **TW369** usa isso para:
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

## 🧨 8. Por que 49 polaridades?

Porque o KALDRA trabalha com:

**49 = 7² (número sagrado)**

Perfeito para:
- Mapeamento completo de tensões arquetípicas
- Compatibilidade com **Sinais KALDRA**
- Topologia narrativa fractal
- Balanceamento entre motores
- Cobertura completa de dimensões existenciais, cognitivas, culturais e emocionais

---

## 🔐 9. Regra Antigravity — IMUTÁVEL

Este arquivo:
- ❌ **não deve ser alterado**
- ❌ **não deve ter IDs trocados**
- ❌ **não deve ter labels modificados**
- ❌ **não deve deletar polaridades**
- ❌ **não deve reordenar nada**

Apenas é permitido **adicionar novas polaridades**, e ainda assim somente se:

> ✅ Não criar conflito de semântica com TW369 ou Δ144.

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

- ✨ o **esqueleto emocional e cognitivo** do sistema
- 🗺️ o **atlas das tensões arquetípicas**
- 🌉 a **ponte entre TW369, Δ144 e Kindras**
- 🔒 a **referência fixa para Antigravity**

**Sem ele, os motores não conseguem calibrar deriva, risco, sombra, metanoia ou coerência.**

---

## 📊 12. Distribuição por TW369

| TW Plane | Polaridades Alinhadas | Característica |
|----------|----------------------|----------------|
| **3** | 28 polaridades | Ação, expansão, manifestação |
| **6** | 27 polaridades | Defesa, tensão, segurança |
| **9** | 26 polaridades | Transcendência, invisibilidade, metanoia |

Muitas polaridades estão alinhadas a **múltiplos planos**, refletindo a natureza multidimensional das tensões arquetípicas.

---

**Última atualização:** 2025-11-22  
**Versão:** 1.0 (49 polaridades)
