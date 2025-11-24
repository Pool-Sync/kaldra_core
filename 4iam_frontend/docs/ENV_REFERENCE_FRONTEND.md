# ENV Reference — KALDRA Frontend (Next.js / Vercel)
**Last Updated:** 2025-11-24

## Overview
Este documento lista todas as variáveis de ambiente usadas pelo frontend do KALDRA.

## Variáveis Obrigatórias

### NEXT_PUBLIC_KALDRA_API_MODE
Valores: mock | real

### NEXT_PUBLIC_KALDRA_API_URL
URL do backend em produção (Render).

## Variáveis de Debug (opcional)
NEXT_PUBLIC_DEBUG_KALDRA_CLIENT=true|false

## Templates

### Local
NEXT_PUBLIC_KALDRA_API_MODE=mock
NEXT_PUBLIC_KALDRA_API_URL=http://localhost:8000

### Preview
NEXT_PUBLIC_KALDRA_API_MODE=mock

### Production
NEXT_PUBLIC_KALDRA_API_MODE=real
NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-core-api.onrender.com

## Erros comuns
- Variável faltando → build falha
- API_URL errada → CORS
- Modo mock ativado por engano

## Observação
Sempre redeploy após atualizar NEXT_PUBLIC_*
