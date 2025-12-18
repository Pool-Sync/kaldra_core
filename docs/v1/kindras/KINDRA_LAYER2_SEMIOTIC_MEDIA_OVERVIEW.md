# KINDRA Layer 2 — Cultural Semiótico / Mídia (48 Vetores)

## 0. Visão Geral

O **Layer 2 — Semiótico / Mídia** modela como narrativas, símbolos, enquadramentos, mídia e códigos semióticos transformam a superfície cultural (Layer 1) em **deriva narrativa ativa**.

Este Layer captura não o “clima cultural macro”, mas **as forças que amplificam, distorcem, aceleram, enquadram ou ritualizam narrativas públicas**.

- **Escopo**: 48 vetores semióticos-midiáticos.  
- **Plano TW**: `6` (tensão, fricção, deriva, amplificação, ruído e pressão narrativa).  
- **Arquivo de dados**:  
  `schema/kindras/kindra_vectors_layer2_semiotic_media_48.json`
- **Função**: ajustar Δ144 para refletir a influência real da mídia, símbolos e enquadramentos sobre o campo narrativo.

Em termos do motor:

> Δ144 (ajustado pelo Layer 1) → Layer 2 amplifica/filtra/ritualiza → deriva TW369 (plano 6) → saída enviada ao Layer 3.

---

## 1. O que o Layer 2 mede

O Layer 2 descreve **dinâmicas de comunicação pública e semiótica**, agrupadas em blocos:

### **1. Intensidade Semiótica**
- carga simbólica por mensagem
- saturação memética  
- iconografia dominante  
- teatralidade e performatividade narrativa  

### **2. Estrutura de Mídia**
- centralização vs descentralização da mídia  
- velocidade de difusão  
- amplitude de alcance  
- confiabilidade percebida  

### **3. Enquadramento e Roteiro**
- presença de narrativas mestres  
- frames moralizantes  
- polarização comunicacional  
- repetição ritualística de mensagens  

### **4. Ritmo e Pressão Narrativa**
- velocidade de ciclos narrativos  
- sobrecarga simbólica  
- fadiga narrativa  
- rotatividade de temas  

### **5. Dinâmicas de Atenção**
- volatilidade da atenção coletiva  
- fixação em símbolos/personagens  
- dominância emocional vs racional  

### **6. Distorção e Amplificação**
- ruído  
- propaganda  
- viés estrutural  
- viralidade  

O Layer 2 funciona como **motor de aceleração e distorção narrativa**.

---

## 2. Estrutura de Dados

Arquivo:

```text
schema/kindras/kindra_vectors_layer2_semiotic_media_48.json
```

Formato de cada vetor:

```jsonc
{
  "id": "M01",
  "layer": "L2_SEMIOTIC_MEDIA",
  "domain": "SEMIOTIC",
  "tw_plane": "6",
  "scale_type": "spectrum",
  "scale_direction": "high = alta carga simbólica",
  "weight": 1.0,
  "short_name": "Carga Simbólica",
  "objective_definition": "...",
  "examples": [...],
  "narrative_role": "..."
}
```

Campos obrigatórios:

* `layer`: identifica este Layer como **L2_SEMIOTIC_MEDIA**
* `domain`: SEMIOTIC, MEDIA, FRAME, ATTENTION, DISTORTION, etc.
* `tw_plane`: `"6"`
* `scale_type` e `scale_direction`: instruções interpretativas
* `weight`: peso base
* `narrative_role`: descreve influência direta sobre Δ144

---

## 3. Ligação com Δ144

### 3.1. Pipeline

1. Δ144 gera uma distribuição bruta.
2. Layer 1 ajusta esta distribuição via campo cultural.
3. Layer 2 **amplifica ou distorce estados específicos**.

Exemplo conceitual:

```python
# estados relacionados a teatralidade e projeção de imagem
mapping["M05"] = {
  "boost": ["PERFORMER_LIGHT", "MAGICIAN_LIGHT"],
  "suppress": ["HERMIT_LIGHT"]
}
```

Vetores de mídia podem:

* mudar a probabilidade de transição entre estados Δ144
* amplificar modos sombra
* reforçar narrativas míticas ou conspiratórias
* empurrar arquétipos coletivos para modos de crise ou euforia

O Layer 2 é o **motor de histerese e carga narrativa**.

### 3.2. Arquivo necessário para implementação (a criar):

```
schema/kindras/kindra_layer2_to_delta144_map.json
```

Estrutura sugerida:

```jsonc
{
  "M01": { "boost": [...], "suppress": [...] },
  "M17": { "boost": [...], "suppress": [...] }
}
```

---

## 4. Relação com TW369 e Quiralidade

### **4.1. TW-Plane 6**

Este é o plano da **fricção**, **tensão**, **deriva**, **transição**, **caos**, **pressão**, **sombra emergente**.

O Layer 2 entra no motor TW como:

```python
tw_state = TWState(
    plane3_cultural_macro = layer1_vector,
    plane6_semiotic_media = layer2_vector,
    plane9_structural_systemic = None
)
```

### **4.2. Quiralidade 3 → 6 → 9**

* **3**: comportamento cultural visível
* **6**: tensão narrativa, transformação, conflito, distorção
* **9**: sedimentação estrutural

Layer 2 é **onde a transformação ocorre**.

---

## 5. Implementação em Código

### 5.1. Arquivos que já existem

* `schema/kindras/kindra_vectors_layer2_semiotic_media_48.json`

### 5.2. Arquivos do motor que ainda precisam ser criados

1. Loader:

```
src/kindras/layer2_semiotic_media_loader.py
```

2. Scoring:

```
src/kindras/layer2_semiotic_media_scoring.py
```

Função sugerida:

```python
def score_layer2(context, media_metrics):
    """Retorna intensidades normalizadas dos 48 vetores semióticos."""
```

3. Ligação Δ144:

```
src/kindras/layer2_delta144_bridge.py
```

4. Tabelas de mapeamento:

```
schema/kindras/kindra_layer2_to_delta144_map.json
```

5. Testes:

```
tests/kindras/test_layer2_semiotic_media.py
tests/kindras/test_layer2_delta144_bridge.py
```

---

## 6. Função do Layer 2 na Estrutura Narrativa Profunda

O Layer 2:

* amplifica símbolos
* acelera ciclos narrativos
* cria pressões de tensão
* define forma como crises são percebidas
* distorce luz/sombra
* gera ruído, ironia, propaganda, viralidade
* cria "momentum" cultural

Ele é o **motor da pressão semiótica** dentro do KALDRA.

---

## 7. Resumo Operacional

* Entrada: métricas de comunicação, mídia, símbolos e frames.
* Processo:

  1. Carregar vetores layer2.
  2. Produzir vetor layer2.
  3. Ajustar Δ144 via bridge.
  4. Alimentar TW369 no plano 6.
* Saída: Δ144 distorcido/amplificado pelo ambiente semiótico real.

Este arquivo define oficialmente o funcionamento do **Layer 2 — Semiótico / Mídia** no KALDRA.
