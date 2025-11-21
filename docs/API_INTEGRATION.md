# KALDRA CORE — API Integration (v0.1)

## Visão Geral

O KALDRA CORE expõe um pipeline de geração de sinais via função:

- `kaldra_core.kaldra_engine.generate_kaldra_signal(text: str)`

Esta função deve ser encapsulada por um API Gateway (ex.: FastAPI) no serviço `kaldra_api`.

## Endpoint sugerido

`POST /engine/kaldra/signal`

### Request

```json
{
  "text": "texto de entrada a ser analisado"
}
```

### Response

Segue o schema `kaldra_signal.schema.json`:

```json
{
  "archetype": "string",
  "delta_state": "string",
  "tw_regime": "STABLE | CRITICAL | UNSTABLE",
  "kindra_distribution": { "K01": 0.12, "...": 0.0 },
  "bias_score": 0.42,
  "meta_modifiers": { 
    "strength": [...], 
    "journey": [...], 
    "discipline": [...] 
  },
  "confidence": 0.83,
  "explanation": "string"
}
```

## Considerações

- Respostas devem usar `application/json`.
- Erros devem retornar códigos 4xx/5xx com payload JSON padronizado.
- Implementar rate limiting para proteção.
- Adicionar logging de todas as requisições.

## Exemplo de Implementação (FastAPI)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kaldra_core.kaldra_engine import generate_kaldra_signal

app = FastAPI()

class SignalRequest(BaseModel):
    text: str

@app.post("/engine/kaldra/signal")
async def create_signal(request: SignalRequest):
    try:
        signal = generate_kaldra_signal(request.text)
        return signal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Endpoints Adicionais Sugeridos

### Apps Específicos

- `POST /apps/alpha/analyze` — KALDRA-ALPHA earnings analysis
- `POST /apps/geo/analyze` — KALDRA-GEO geopolitical analysis
- `POST /apps/product/analyze` — KALDRA-PRODUCT review analysis
- `POST /apps/safeguard/evaluate` — KALDRA-SAFEGUARD risk evaluation

### Batch Processing

- `POST /engine/kaldra/batch` — Process multiple texts
- `GET /engine/kaldra/status/{job_id}` — Check batch job status

## Autenticação

Recomendado: API Key ou JWT tokens

```http
Authorization: Bearer <token>
```

## Rate Limiting

Sugestão: 100 requisições/minuto por cliente
