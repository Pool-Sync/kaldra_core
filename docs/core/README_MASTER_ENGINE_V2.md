# KALDRA MASTER ENGINE v2.0

## 0. Visão Geral

O **KALDRA Master Engine v2.0** é o orquestrador que combina:

1. **Δ144 Engine**  
   Motor arquetípico base (12×12 = 144 estados) que converte contexto em distribuição de arquétipos.

2. **Kindra Cultural Modulation 3×48**  
   Camada de modulação cultural (planos 3, 6, 9) que ajusta a distribuição Δ144 de acordo com o contexto cultural.

3. **TW-Painlevé Oracle**  
   Módulo estatístico que monitora janelas de sinais e detecta eventos extremos via maior autovalor + limiar Tracy–Widom (com espaço reservado para filtro Painlevé II).

4. **τ Layer / Epistemic Limiter**  
   Camada de limitação epistemológica que decide se o sistema está confiante o suficiente para “manifestar” um arquétipo ou delega decisão para revisão humana.

O objetivo do v2.0 é transformar o KALDRA em um **pipeline completo, testável e auditável**:

> embedding de contexto → Δ144 → modulação 3×48 → detecção TW → decisão τ → `KaldraSignal`

---

## 1. Componentes Principais

### 1.1 Δ144 Engine (`Delta144Engine`)

**Arquivo:**  
`src/archetypes/delta144_engine.py`

**Responsabilidade:**

- Carregar os schemas em `schema/archetypes/`:
  - `archetypes_12.json`
  - `delta144_states.json`
  - `archetype_modifiers.json`
  - `polarities.json`
- Inferir um **estado arquetípico Δ144** a partir de algum vetor de entrada (embedding, features, etc.).
- Produzir uma **distribuição de probabilidade sobre os 144 estados**.

**Interface típica (exemplo, adaptar aos nomes reais):**

```python
from src.archetypes.delta144_engine import Delta144Engine

engine = Delta144Engine.from_default_files()
result = engine.infer_from_vector(embedding)  # embedding: np.ndarray (d_ctx,)

# Exemplo de atributos esperados:
probs = result.probs          # np.ndarray shape (144,)
state_id = result.state_id    # ex: "A03_07"
```

⚠️ O Master Engine v2 não altera a semântica do Δ144 Engine.
Ele apenas consome a distribuição produzida pelo Δ144.

---

### 1.2 Kindra Cultural Modulation Layer (`KaldraKindraCulturalMod`)

**Arquivo:**
`src/kindras/kindra_cultural_mod.py`

**Responsabilidade:**
- Implementar a camada neural de modulação 3×48 sobre a distribuição Δ144.
- Receber:
  - `archetype_probs` – distribuição Δ144 base `(..., 144)`.
  - `context_vec` – vetor de contexto cultural `(..., d_ctx)`.
- Produzir:
  - distribuição modulada `(..., 144)`, normalizada por softmax (opcional).

**Ideia de funcionamento:**

Para cada plano $p \in \{3, 6, 9\}$:
1. Projetar contexto em 48 dimensões: $c_p = \sigma(W_p x + b_p)$.
2. Mapear 48 → 144: $g_p = \sigma(c_p M_p)$.
3. Combinar ganhos com pesos $\lambda_p$:
   $gain_{total} = 1 + \sum \lambda_p g_p$.

**Distribuição final:**

$s' = \text{softmax}(a \odot gain_{total})$

onde:
- $a$ = distribuição Δ144 base.
- $\odot$ = produto elemento a elemento.

**Exemplo de uso:**

```python
import torch
from src.kindras.kindra_cultural_mod import KaldraKindraCulturalMod

mod = KaldraKindraCulturalMod(d_ctx=256)

archetype_probs = torch.rand(1, 144)
archetype_probs = torch.softmax(archetype_probs, dim=-1)

context_vec = torch.randn(1, 256)

modulated = mod(archetype_probs, context_vec, apply_softmax=True)
print(modulated.shape)  # (1, 144)
print(modulated.sum(dim=-1))  # ~1.0
```

---

### 1.3 TW-Painlevé Oracle (`TWPainleveOracle`)

**Arquivo:**
`src/tw369/oracle_tw_painleve.py`

**Responsabilidade:**
- Receber uma janela temporal de sinais (ex: ativação de camadas, métricas, embeddings).
- Calcular:
  - Matriz de covariância $C$ da janela.
  - Maior autovalor $\lambda_{max}$.
  - Limiar aproximado baseado em distribuição Tracy–Widom.
- Retornar:
  - `trigger`: bool – se a janela indica evento extremo.
  - `TWStats` – estatísticas auxiliares ($\lambda_{max}$, threshold, etc.).

**Interface esperada:**

```python
import numpy as np
from src.tw369.oracle_tw_painleve import TWPainleveOracle, TWConfig

oracle = TWPainleveOracle(TWConfig(window_size=50, alpha=0.99))
window = np.random.randn(50, 16)  # (T, m)

trigger, stats = oracle.detect(window)
print(trigger, stats.lambda_max, stats.threshold)
```

🔬 O filtro Painlevé II pode ser mantido como TODO documentado — o módulo já está preparado para incluir essa etapa sem quebrar a interface.

---

### 1.4 τ Layer / Epistemic Limiter (`EpistemicLimiter`)

**Arquivo:**
`src/core/epistemic_limiter.py`

**Responsabilidade:**
- Receber distribuições de probabilidade sobre os 144 arquétipos.
- Verificar $\max(p)$ e decidir:
  - se o sistema está confiante o suficiente (status = "OK"), ou
  - se deve retornar um estado INCONCLUSIVO e delegar a decisão.

**Interface:**

```python
import numpy as np
from src.core.epistemic_limiter import EpistemicLimiter

tau_layer = EpistemicLimiter(tau=0.65)

probs = np.random.dirichlet([1.0] * 144)
decision = tau_layer.from_probs(probs)

print(decision.status, decision.delegate, decision.archetype_idx, decision.confidence)
```

---

## 2. KALDRA MASTER ENGINE v2.0

**Arquivo:**
`src/core/kaldra_master_engine.py`

### 2.1 Responsabilidade

O `KaldraMasterEngineV2` conecta os módulos anteriores em um único fluxo:
1. Recebe embedding de contexto (ex: texto de earnings call, contexto geopolítico, etc.).
2. Usa o **Δ144 Engine** para obter distribuição arquetípica base.
3. Usa a **Kindra Cultural Modulation** para ajustar essa distribuição ao contexto cultural.
4. (Opcional) Usa o **TW-Painlevé Oracle** para analisar uma janela de sinais.
5. Usa o **Epistemic Limiter** para decidir se o sistema deve “manifestar” um arquétipo ou ficar em estado INCONCLUSIVO.
6. Retorna um objeto `KaldraSignal` com tudo que é necessário para logs, dashboards e APIs.

### 2.2 Estrutura conceitual

**Fluxo simplificado:**

```
embedding (d_ctx)
   ↓
Δ144 Engine → probs_base (144,)
   ↓
Kindra Mod 3×48 → probs_modulated (144,)
   ↓
TW Oracle (janela opcional de sinais) → trigger / stats
   ↓
τ Layer → decisão epistemológica
   ↓
KaldraSignal (objeto final)
```

### 2.3 Interface de Alto Nível

**Exemplo de uso (versão mínima):**

```python
import numpy as np
from src.core.kaldra_master_engine import KaldraMasterEngineV2

# embedding de contexto (por ex., saída de um encoder de texto)
embedding = np.random.randn(256)

# janela de sinais para o TW (opcional)
tw_window = np.random.randn(50, 16)

engine = KaldraMasterEngineV2()
signal = engine.infer_from_embedding(embedding, tw_window=tw_window)

print(signal.archetype_probs.shape)  # (144,)
print(signal.tw_trigger)             # bool
print(signal.epistemic.status)       # "OK" ou "INCONCLUSIVO"
print(signal.epistemic.confidence)   # float
```

⚠️ A assinatura exata de `Delta144Engine` deve ser respeitada.
Caso os nomes reais sejam diferentes (`infer_state`, `infer`, `state_distribution`, etc.), adaptar internamente sem quebrar APIs públicas já usadas nos READMEs.

---

## 3. Integração com a API (`/engine/kaldra/signal`)

A rota HTTP principal do KALDRA já existe no API Gateway:
- **Endpoint:** `POST /engine/kaldra/signal`
- **Arquivo:** `kaldra_api/routers/router_engine.py`

### 3.1 Versão v2.0 — Payload Conceitual

**Request (conceitual):**

```json
{
  "text": "The CEO is optimistic about revenue growth",
  "context_features": {
    "domain": "earnings_call",
    "ticker": "TSLA",
    "language": "en"
  }
}
```

**Response (conceitual, incorporando v2.0):**

```json
{
  "archetype_probs": [0.01, 0.03, ..., 0.02],
  "top_archetype": {
    "id": "A03_07",
    "label": "MAGICIAN — ORDEAL",
    "confidence": 0.78
  },
  "tw": {
    "trigger": true,
    "lambda_max": 12.4,
    "threshold": 10.9,
    "num_eigenvalues": 16
  },
  "epistemic": {
    "status": "OK",
    "delegate": false,
    "tau": 0.65
  }
}
```

**Importante:**
A API atual não precisa necessariamente expor todos esses campos imediatamente.
O README serve como alvo de evolução – o backend pode começar com um subconjunto e adicionar o resto de forma incremental.

---

## 4. Testes e Garantias

### 4.1 Testes Unitários

**Local:**
- `tests/test_tw_oracle.py`
- `tests/test_kindra_mod.py`
- `tests/test_epistemic_limiter.py`
- `tests/test_master_engine_v2.py`

**Cobrem:**
- Inicialização de todos os módulos.
- Formato das saídas (shapes, tipos).
- Propriedades básicas:
  - soma das probabilidades ≈ 1.
  - `EpistemicLimiter` respeita o limiar τ.
  - `TWPainleveOracle.detect` sempre retorna um `TWStats` válido.

### 4.2 Não-Quebra de Compatibilidade

Este README define explicitamente:
- **O v2.0 não altera:**
  - o formato de schemas JSON em `schema/archetypes/`.
  - o comportamento base do `Delta144Engine`.
- **O v2.0 é aditivo:**
  - novos módulos em `src/tw369/`, `src/kindras/`, `src/core/`.
  - novas docstrings e READMEs em `docs/`.

---

## 5. Roadmap de Evolução

1. **v2.1 — Implementação real do filtro Painlevé II**
   - Resolver Painlevé II numericamente para filtrar autovalores.
   - Incluir benchmarks com dataset (ex: CrisisNLP).

2. **v2.2 — Treinamento da camada Kindra com dados reais**
   - Calibração via KL-divergence em dados rotulados.
   - Experimentação com RLHF para ajuste fino dos $\lambda_p$.

3. **v2.3 — Log Δᴴ e Auditoria Completa**
   - Integração com logger estruturado:
     - entradas (embedding, janela TW)
     - decisões (TW trigger, τ, arquétipo)
   - Trilhas de auditoria para uso em Safeguard / Governance.

4. **v2.4 — Integração profunda com KALDRA-ALPHA**
   - Conectar o Master Engine v2.0 à pipeline de earnings calls.
   - Expor sinais completos no dashboard 4iam.ai.

---

## 6. Resumo

O **KALDRA Master Engine v2.0** consolida todo o arcabouço teórico e simbólico do KALDRA em uma arquitetura concreta:
- **Δ144** como base arquetípica.
- **3×48 Kindras** como modulação cultural treinável.
- **TW-Painlevé** como oráculo estatístico de eventos extremos.
- **τ Layer** como guard rail epistemológico.

Ele é, ao mesmo tempo:
- **implementável** (código em `src/`),
- **auditável** (tests + docs),
- **extensível** (roadmap claro),
- e **pronto** para ser consumido por APIs e frontends como o 4iam.ai.
