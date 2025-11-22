# 📘 **README_DO_DEPLOY_COMPLETO.md**

### **KALDRA — Full Deployment & Master Engine Technical Documentation**

> Versão 1.0 — Documento Oficial do Sistema KALDRA
> Este README consolida todo o pipeline, arquitetura, integrações e instruções de deploy do ecossistema KALDRA.

---

# 🔥 **1. Visão Geral do Sistema KALDRA**

O **KALDRA** é um sistema completo de **Narrative Intelligence** capaz de interpretar textos (earnings calls, discursos, relatórios, comentários, etc.) e gerar um **KALDRA Signal**, composto por:

* Estado arquétipo (Δ12)
* Estado expandido da matriz Δ144 (12×12)
* Distribuição cultural (Kindras 3×48)
* Bias score
* Regime TW369 (Tracy-Widom + Painlevé)
* Meta-modifiers
* Confiança e explicação sintética

O sistema foi projetado para operar em produção via:

* **Backend → Render**
* **Frontend → Vercel**
* **Master Engine → Python (FastAPI + módulos KALDRA)**

---

# 🧩 **2. Arquitetura Completa do Sistema**

```
kaldra_core/
├── core/                 # Motores fundamentais (Bias, Δ12, Δ144, TW369, Kindras, Meta)
├── kaldra_engine/        # Orquestrador do Master Engine (gera o KALDRA Signal)
├── kaldra_api/           # API Gateway (FastAPI + CORS + Routers)
├── scripts/              # Scripts auxiliares (mock signals, validators)
└── 4iam_frontend/        # Frontend (Next.js + Vercel)
```

### **Fluxo Geral**

```
Texto → Preprocessing → Δ12 → Δ144 → Kindras → Bias → TW369 → Meta → KALDRA Signal
```

---

# ⚙️ **3. Pipeline Técnico do Master Engine**

O pipeline executado pelo `generate_kaldra_signal()`:

```
1. Recebe o texto bruto
2. Normaliza texto + quebra ruído
3. Bias Engine
4. Δ12 Dynamic Engine
5. Δ144 Projection (12×12)
6. Kindra 3×48 Distribution
7. TW369 Regime Calculation (Tracy-Widom + Painlevé)
8. Meta Modifiers
9. Monta KaldraSignalResponse
10. Retorna via API
```

---

# 🏗 **4. Arquivos e Responsabilidades**

## **core/**

| Arquivo                  | Função                                        |
| ------------------------ | --------------------------------------------- |
| `core/bias.py`           | Cálculo de bias_score e classificação         |
| `core/tw369/core.py`     | Núcleo TW369 (instabilidade, regime base)     |
| `core/tw369/tw_guard.py` | Guardião TW, safe mode, ajustes               |
| `core/delta144/*`        | Lógica da matriz Δ144 (inferência de estados) |
| `core/kindras.py`        | Mapeamento cultural 3×48                      |
| `core/meta.py`           | Aplicação dos meta-modifiers                  |
| `core/preprocessing.py`  | (opcional) normalização de texto              |

## **kaldra_engine/**

| Arquivo                          | Função                                             |
| -------------------------------- | -------------------------------------------------- |
| `kaldra_engine/kaldra_engine.py` | Função **central**: `generate_kaldra_signal(text)` |
| `preprocessing.py`               | Prepara texto (se aplicável)                       |
| `postprocessing.py`              | Monta resposta final                               |

## **kaldra_api/**

| Arquivo                    | Função                                        |
| -------------------------- | --------------------------------------------- |
| `main.py`                  | FastAPI + CORS + routers                      |
| `routers/router_engine.py` | Endpoint oficial `POST /engine/kaldra/signal` |

---

# 🧬 **5. Δ12 → Δ144 (Explicação Operacional)**

### Δ12 = Semente Arquétipa

Cada texto gera uma ativação entre 12 arquétipos base (Jung/Campbell).

### Δ144 = Expansão 12×12

O sistema cruza:

```
(Arquetipo Primário) × (Arquetipo Condicionante)
```

≈ 144 possíveis estados combinados.

Processo:

```
1. Normalizar texto
2. Classificar nos 12 arquétipos
3. Expandir ao grid 12×12
4. Selecionar estado Δ144 dominante
5. Gerar intensidades (0–1)
```

Δ144 é o núcleo da leitura simbólica narrativa.

---

# ⚡ **6. TW369, Painlevé II e Tracy-Widom**

| Componente      | Função                                                   |
| --------------- | -------------------------------------------------------- |
| **Tracy-Widom** | Detecta anomalias narrativas extremas                    |
| **Painlevé II** | Suaviza curvatura e influência no regime                 |
| **TW369**       | Converte isso em 3 estados: Stable / Unstable / Critical |

Processo:

```
TW Score = Tracy-Widom(x)
Curve = Painleve_II(x)
TW Regime = TW369(TW Score, Curve)
```

Arquivo responsável:

* `core/tw369/core.py`
* `core/tw369/tw_guard.py`

---

# 🌐 **7. API Gateway — Documentação Completa**

### **Endpoint Oficial**

```
POST https://kaldra-core-api.onrender.com/engine/kaldra/signal
```

### **Body**

```json
{
  "text": "The CEO is optimistic about revenue growth"
}
```

### **Response (exemplo real)**

```json
{
  "archetype": "UNSPECIFIED",
  "delta_state": "GENERIC",
  "tw_regime": "CRITICAL",
  "kindra_distribution": { "K01": 1.0 },
  "bias_score": 0.04,
  "meta_modifiers": { "strength": [7,7,...] },
  "confidence": 0.98,
  "explanation": "neutral",
  "narrative_risk": "LOW"
}
```

### **CORS (Render)**

Arquivo: `kaldra_api/main.py`

```python
origins = [
    "http://localhost:3000",
    "https://4iam-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

# 🚀 **8. Deploy Backend (Render)**

### **Passos**

1. Criar serviço Web → Docker
2. Usar:

```
uvicorn kaldra_api.main:app --host 0.0.0.0 --port $PORT
```

3. Build automático do Render
4. Teste via `/docs`

### **Dockerfile**

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["sh", "-c", "uvicorn kaldra_api.main:app --host 0.0.0.0 --port ${PORT}"]
```

---

# 🖥 **9. Deploy Frontend (Vercel)**

### **Configuração do Endpoint no Frontend**

Arquivo: `app/lib/api/kaldra.ts`

```ts
const url = `${API_CONFIG.baseUrl}/engine/kaldra/signal`;

export async function getKaldraSignal(text: string) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });
  return res.json();
}
```

---

# 🧪 **10. Testes End-to-End**

### Teste básico:

```
curl -X POST \
  https://kaldra-core-api.onrender.com/engine/kaldra/signal \
  -H "Content-Type: application/json" \
  -d '{"text":"growth"}'
```

### Esperado:

* OPTIONS 200 (CORS OK)
* POST 200 (JSON completo)

### Teste no browser:

Acesse:

```
https://4iam-frontend.vercel.app/alpha
```

---

# 📈 **11. Roadmap Futuro**

* Δ144 v2 com embeddings semânticos
* Painlevé/TW em stream (tempo real)
* KALDRA-GEO + KALDRA-PRODUCT integrados
* Dashboard avançado no Explorer

---

# 🎉 **Fim do README 1.0**

Este documento está pronto para produção, para onboarding técnico, e para publicação oficial.
