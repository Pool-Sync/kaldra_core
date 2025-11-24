# KINDRA 3×48 — Documento Mestre dos 3 Layers (L1 + L2 + L3)

## 0. Visão Geral

O sistema **Kindra 3×48** é a engenharia cultural-narrativa do KALDRA.  
Ele organiza 144 forças culturais em três planos (TW369), formando:

- **Layer 1 — Cultural Macro** (48 vetores)  
- **Layer 2 — Semiótico / Mídia** (48 vetores)  
- **Layer 3 — Estrutural / Sistêmico** (48 vetores)

Esses 3 Layers formam um **motor de transformação cultural**, usado para ajustar, modular e interpretar os **144 estados arquetípicos (Δ144)** dentro do KALDRA Engine.

Cada Layer opera em um plano específico da TW369:

| Layer | Plano TW | Função |
|-------|----------|--------|
| **Layer 1** | **3** | Campo cultural visível, comportamento, expressão |
| **Layer 2** | **6** | Tensão, fricção, deriva narrativa, mídia |
| **Layer 3** | **9** | Estruturas profundas, civilização, trauma, poder |

---

# 1. Layer 1 — Cultural Macro (Plano 3)

### **Função Essencial**
Fornece o “campo cultural” onde Δ144 opera:
- Expressividade
- Risco
- Relações sociais
- Hierarquia
- Mito e moral
- Temporalidade

### **Relação com Δ144**
Layer 1 altera:
- intensidade relativa dos estados  
- leitura cultural dos arquétipos  
- como luz/sombra se manifestam em cada contexto  

### **Relação com TW369**
- **Plano 3** = superfície  
- Determina como mensagens aparecem e se comportam  
- Impacta transição **3 → 6** (comportamento → tensão)

### **Arquivos**
- `schema/kindras/kindra_vectors_layer1_cultural_macro_48.json`
- Necessário criar:
  - `kindra_layer1_to_delta144_map.json`
  - loader, scoring, bridge

---

# 2. Layer 2 — Semiótico / Mídia (Plano 6)

### **Função Essencial**
Modela:
- símbolos  
- frames  
- mídia  
- ruído  
- iconografia  
- amplificação narrativa  
- viralidade  
- distorção  
- teatralidade  

É o motor de **pressão semiótica**, alterando a probabilidade de deriva narrativa.

### **Relação com Δ144**
Layer 2 amplifica/suprime estados arquetípicos conforme:
- carga simbólica  
- frames dominantes  
- ciclos de mídia  
- polarização  

### **Relação com TW369**
- **Plano 6** = tensão, conflito, transformação  
- Onde ocorrem:
  - drift  
  - pressão  
  - saturação  
  - transições de sombra  

### **Arquivos**
- `schema/kindras/kindra_vectors_layer2_semiotic_media_48.json`
- Necessário criar:
  - `kindra_layer2_to_delta144_map.json`
  - loader, scoring, bridge

---

# 3. Layer 3 — Estrutural / Sistêmico (Plano 9)

### **Função Essencial**
Modela:
- estruturas de poder  
- instituições  
- economia profunda  
- trauma coletivo  
- continuidade civilizacional  
- rigidez ou fluidez do sistema  

É o layer de **gravidade simbólica**.

### **Relação com Δ144**
Layer 3 altera:
- estabilidade de estados  
- velocidade de transição  
- probabilidade de colapso  
- arquétipos de governança, guardião, profeta  

### **Relação com TW369**
- **Plano 9** = raiz, destino, profundidade  
- Interpreta:
  - trauma  
  - memória  
  - rigidez civilizacional  
  - tendência a colapso/renascimento

### **Arquivos**
- `schema/kindras/kindra_vectors_layer3_structural_systemic_48.json`
- Necessário criar:
  - `kindra_layer3_to_delta144_map.json`
  - loader, scoring, bridge

---

# 4. Pipeline Operacional Integrado

## 4.1. Entrada do Sistema

1. Dados do contexto cultural, midiático e estrutural:
   - país  
   - setor  
   - organização  
   - mídia  
   - ciclos narrativos  
   - indicadores estruturais  

2. Cada layer gera um vetor:
   - `layer1_vector` (48 valores plano 3)  
   - `layer2_vector` (48 valores plano 6)  
   - `layer3_vector` (48 valores plano 9)  

---

## 4.2. Integração com Δ144

Pipeline:

1. **Δ144 Engine** gera distribuição base (144 estados).
2. Layer 1 aplica “cor cultural”.
3. Layer 2 amplifica/filtra/emoldura.
4. Layer 3 estabiliza/destabiliza/solidifica.
5. TW369 interpreta evolução temporal dos estados.

---

# 5. Interação com TW369 e Quiralidade

### Plano 3 (Layer 1)
- superfície  
- comportamento  
- símbolos explícitos  

### Plano 6 (Layer 2)
- tensão  
- conflito  
- pressão  
- drift  
- ruído  

### Plano 9 (Layer 3)
- estruturas  
- poder  
- trauma  
- destino  

**Quiralidade 3 → 6 → 9 → 3**

O ciclo inteiro se realimenta:
- o plano 3 gera mensagens  
- o plano 6 distorce  
- o plano 9 estabiliza  
- o plano 3 manifesta resultados

---

# 6. Arquivos que ainda precisam ser implementados (Resumo)

## Para Layer 1
- `kindra_layer1_to_delta144_map.json`
- `layer1_cultural_macro_loader.py`
- `layer1_cultural_macro_scoring.py`
- `layer1_delta144_bridge.py`
- testes correspondentes

## Para Layer 2
- `kindra_layer2_to_delta144_map.json`
- `layer2_semiotic_media_loader.py`
- `layer2_semiotic_media_scoring.py`
- `layer2_delta144_bridge.py`
- testes correspondentes

## Para Layer 3
- `kindra_layer3_to_delta144_map.json`
- `layer3_structural_systemic_loader.py`
- `layer3_structural_systemic_scoring.py`
- `layer3_delta144_bridge.py`
- testes correspondentes

---

# 7. Resumo Final

Os 3 Layers Kindra:

- formam a base cultural-narrativa do KALDRA  
- modulam Δ144 nos três planos TW  
- determinam como narrativas emergem, se espalham, colapsam ou se institucionalizam  
- constituem o sistema cultural mais completo já integrado ao Δ144 Engine  

Este documento serve como a **espinha dorsal de implementação** do Kindra 3×48 no KALDRA.
