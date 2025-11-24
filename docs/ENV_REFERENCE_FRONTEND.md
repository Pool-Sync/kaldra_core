# 4iam.ai Frontend — Environment Reference

Este documento lista TODAS as variáveis de ambiente relevantes para o frontend
(4iam_frontend/) e como usá-las em cada ambiente.

## 1. Variáveis Principais

### NEXT_PUBLIC_KALDRA_API_MODE
- **Tipo**: string
- **Valores possíveis**:
  - `mock` → Usa dados mockados (sem chamadas reais).
  - `real` → Usa o backend real (Render).
- **Uso**:
  - Controla o comportamento do `kaldra_client.ts` (modo seguro de fallback).
- **Recomendado**:
  - Dev local: `mock` ou `real`
  - Preview (PRs no Vercel): `mock`
  - Production: `real`

### NEXT_PUBLIC_KALDRA_API_URL
- **Tipo**: string (URL)
- **Exemplo (produção)**:
  - `https://kaldra-core-api.onrender.com`
- **Uso**:
  - Base URL para chamadas ao backend KALDRA (Render).
- **Cuidados**:
  - Sem barra final (`/`) no final da URL.
  - Alterar SEMPRE via painel do Vercel (env vars).

---

## 2. Ambientes Recomendados

### 2.1. Desenvolvimento Local

Arquivo: `4iam_frontend/.env.local` (NÃO comitar)

Exemplo:

NEXT_PUBLIC_KALDRA_API_MODE=real
NEXT_PUBLIC_KALDRA_API_URL=http://localhost:8000

Ou, para desenvolvimento isolado de UI:

NEXT_PUBLIC_KALDRA_API_MODE=mock
NEXT_PUBLIC_KALDRA_API_URL=http://localhost:8000

---

### 2.2. Preview (PRs no Vercel)

- Objetivo: não depender do backend de produção.
- Recomendado:

NEXT_PUBLIC_KALDRA_API_MODE=mock
NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-core-api.onrender.com

(O URL pode existir, mas o modo será mock, então é apenas um fallback.)

---

### 2.3. Production (Vercel)

- Objetivo: usar o backend real KALDRA em Render.

NEXT_PUBLIC_KALDRA_API_MODE=real
NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-core-api.onrender.com

---

## 3. Fonte da Verdade

- Arquivo de template: `4iam_frontend/.env.example`
- Este documento (ENV_REFERENCE_FRONTEND.md)
- DEPLOY_FRONTEND_VERCEL.md para o passo-a-passo de deploy.
