# KINDRA Layer 1 — Cultural Macro (48 Vetores)

## 0. Visão Geral

O **Layer 1 — Cultural Macro** é a camada de entrada dos Kindras no KALDRA.  
Ele modela o **campo cultural de fundo** onde os 144 arquétipos (Δ144) operam.

- **Escopo**: 48 vetores de campo cultural.
- **Plano TW**: `3` (superfície / comportamento visível).
- **Arquivo de dados**:  
  `schema/kindras/kindra_vectors_layer1_cultural_macro_48.json`
- **Função principal**: colorir a distribuição Δ144 de acordo com o **ambiente cultural macro**.

Em termos de motor:

> Contexto bruto → Δ144 (144 estados) → Layer 1 aplica o “filtro macro-cultural” → distribuição ajustada segue para TW369 / demais Layers.

---

## 1. O que o Layer 1 mede

Cada um dos 48 vetores mede **tendências culturais estruturais**, em escala macro, agrupadas em 6 blocos:

1. **Expressividade**  
   - expressividade emocional  
   - intensidade de linguagem  
   - ritmo de comunicação e interação  
   - espontaneidade, humor, estética de comunicação  
2. **Relação Social**  
   - calor social  
   - individualismo/coletivismo  
   - limites de intimidade  
   - fluxo conversacional  
3. **Hierarquia e Poder**  
   - hierarquia vs igualitarismo  
   - formalidade estrutural  
   - centralização de poder  
   - obediência cultural / autoridade internalizada  
4. **Temporalidade**  
   - orientação temporal (passado/presente/futuro)  
   - velocidade de execução  
   - sincronização social / pressão temporal  
   - narrativa de futuro  
5. **Risco**  
   - aversão ao risco  
   - controle de incerteza  
   - flexibilidade de regras  
   - tolerância ao caos / experimentação  
6. **Mito e Moral**  
   - centralidade de mitos  
   - sacralidade de símbolos  
   - arquitetura moral  
   - narrativa de destino, espiritualidade, tradição, coesão identitária

**Interpretação**:  
O Layer 1 não fala de eventos pontuais; ele descreve o **clima cultural de fundo** em que qualquer narrativa ocorre.

---

## 2. Estrutura de Dados do Layer 1

### 2.1. Arquivo de vetores

Path oficial:

```text
schema/kindras/kindra_vectors_layer1_cultural_macro_48.json
```

Cada vetor possui os campos:

```jsonc
{
  "id": "E01",
  "layer": "L1_CULTURAL_MACRO",
  "domain": "EXPRESSIVE",
  "tw_plane": "3",
  "scale_type": "spectrum",          // spectrum | binary | index
  "scale_direction": "high/low...",  // interpretação da escala
  "weight": 1.0,                     // peso base no motor
  "short_name": "Expressividade Emocional",
  "objective_definition": "...",
  "examples": ["Brasil", "Itália", "..."],
  "narrative_role": "..."
}
```

* `layer`: identifica explicitamente este arquivo como **Layer 1**.
* `domain`: bloco temático (`EXPRESSIVE`, `SOCIAL`, `POWER`, `TEMPORAL`, `RISK`, `MYTHIC`).
* `tw_plane`: sempre `"3"` (plano superficial da TW369).
* `scale_type` e `scale_direction`: instruções para o motor interpretar o valor numérico.
* `weight`: permite calibrar a influência de cada vetor na distribuição Δ144.

---

## 3. Ligação com Δ144 (Arquetipos)

### 3.1. Fluxo conceitual

1. **Δ144 Engine** (`core/archetypes/delta144_engine.py`) gera uma distribuição inicial:

   ```python
   base_distribution: Dict[str, float]  # 144 estados
   ```

2. **Kindra Layer 1** lê o contexto cultural (país, setor, organização) e produz um vetor:

   ```python
   cultural_macro: Dict[str, float]  # 48 vetores normalizados (0–1 ou -1..1, conforme scale_type)
   ```

3. O motor **mapeia cada vetor de Layer 1 para grupos de estados Δ144**, via tabelas de mapeamento (a serem criadas):

   ```python
   # exemplo conceitual
   mapping["E01"] = ["JESTER_LIGHT", "CAREGIVER_SHADOW", ...]
   ```

4. Para cada estado Δ144, a distribuição é ajustada:

   ```python
   adjusted[state_id] = base_distribution[state_id] * f(cultural_macro, mapping, weights)
   ```

### 3.2. Arquivos de mapeamento necessários (a criar)

Para tornar isso implementável, o motor precisa de:

* `schema/kindras/kindra_layer1_to_delta144_map.json`

  * Estrutura sugerida:

    ```jsonc
    {
      "E01": {
        "boost": ["JESTER_LIGHT", "LOVER_LIGHT"],
        "suppress": ["RULER_SHADOW"]
      },
      "R33": {
        "boost": ["GUARDIAN_LIGHT"],
        "suppress": ["OUTLAW_LIGHT", "TRICKSTER_LIGHT"]
      }
    }
    ```

* `src/kindras/kindra_layer1_mapping.py`

  * Funções para carregar o mapa e aplicar ajustes na Δ144.

Esses arquivos **ainda não existem** e são parte do backlog de implementação.

---

## 4. Ligação com TW369 e Quiralidade 3/6/9

### 4.1. Plano 3 (superfície)

* `tw_plane = 3` indica que o Layer 1 atua na **camada observável**:

  * linguagem pública
  * comportamento institucional
  * tom das comunicações

Em código, o Layer 1 deve ser consumido pelo **TW369 Engine** como **entrada de plano 3**:

```python
from tw369.engine import TWState

tw_state = TWState(
    plane3_cultural_macro=cultural_macro_vector,
    # plane6 e plane9 recebem outros layers
)
```

### 4.2. Quiralidade 3 → 6 → 9

* O Layer 1 atua principalmente na **transição 3 → 6**:

  * **3**: o que é dito e mostrado (expressivo, social, midiático).
  * **6**: como isso se converte em tensões, defesas, riscos.
  * **9**: como isso sedimenta em estruturas profundas (Layer 3).

Em termos de engine:

1. Layer 1 fornece o **campo cultural visível**.
2. O TW369 engine calcula **drifts** (3→6) de acordo com:

   * vetores de risco (`R33–R40`)
   * vetores de tempo (`T25–T32`)
3. A saída de 6 é então usada por Layers 2 e 3 para consolidar estados no plano 9.

---

## 5. Como o Layer 1 deve funcionar em código

### 5.1. Arquivos de dados já existentes

* `schema/kindras/kindra_vectors_layer1_cultural_macro_48.json`

  * Definição formal dos 48 vetores.

### 5.2. Arquivos de engine recomendados (a criar)

Para o motor funcionar de ponta a ponta, são recomendados os seguintes arquivos:

1. **Módulo de carregamento e normalização**

   * `src/kindras/layer1_cultural_macro_loader.py`

   Funções sugeridas:

   ```python
   def load_layer1_vectors(path: str) -> List[KindraVector]:
       """Carrega e valida os 48 vetores do Layer 1."""
   ```

2. **Módulo de scoring de contexto**

   * `src/kindras/layer1_cultural_macro_scoring.py`

   Responsabilidades:

   * Receber metadados do contexto (país, setor, tipo de organização).
   * Produzir um vetor de intensidade para cada um dos 48 vetores:

   ```python
   def score_cultural_macro(context: Dict[str, Any]) -> Dict[str, float]:
       """
       Retorna intensidade normalizada (0–1 ou -1..1) para cada id de vetor (E01..M48).
       """
   ```

3. **Módulo de integração com Δ144**

   * `src/kindras/layer1_delta144_bridge.py`

   Responsabilidades:

   * Carregar mapa `kindra_layer1_to_delta144_map.json`.
   * Receber `base_distribution` da Δ144.
   * Aplicar ajustes baseados em `cultural_macro`.

   ```python
   def apply_layer1_to_delta144(
       base_distribution: Dict[str, float],
       cultural_macro: Dict[str, float]
   ) -> Dict[str, float]:
       """
       Ajusta a distribuição Δ144 usando o Layer 1 (macro-cultural).
       """
   ```

4. **Testes**

   * `tests/kindras/test_layer1_cultural_macro.py`
   * `tests/kindras/test_layer1_delta144_bridge.py`

Esses arquivos **não existem ainda** e devem ser criados em etapas futuras de implementação.

---

## 6. Interação com a Estrutura Narrativa Profunda

Na prática, o Layer 1:

1. **Define a “cor do pano de fundo”**:

   * Se o ambiente é altamente hierárquico, mitológico e avesso ao risco, o mesmo arquétipo terá leitura diferente do que em um ambiente igualitário, experimental e secular.

2. **Funciona como “meta-modificador” da Δ144**:

   * Ele não cria novos arquétipos, mas altera:

     * intensidade relativa de estados
     * probabilidade de transição entre estados
     * leitura de luz/sombra de determinados papéis

3. **Prepara o terreno para Layers 2 e 3**:

   * Layer 1 = campo cultural macro (plano 3).
   * Layer 2 = camadas semióticas / mídia (plano 6).
   * Layer 3 = camadas estruturais / sistêmicas (plano 9).

---

## 7. Resumo Operacional

* **Entrada**: metadados culturais do contexto (país, setor, tipo de organização, etc.).
* **Processo**:

  1. Carregar vetores do `kindra_vectors_layer1_cultural_macro_48.json`.
  2. Gerar `cultural_macro_vector` (48 valores).
  3. Ajustar distribuição Δ144 via `layer1_delta144_bridge`.
  4. Fornecer esse resultado ao TW369 Engine como **plano 3**.
* **Saída**: distribuição Δ144 já “colorida” pelo campo cultural macro.

Este documento é a referência oficial para implementação do **Kindra Layer 1 — Cultural Macro** no KALDRA.
