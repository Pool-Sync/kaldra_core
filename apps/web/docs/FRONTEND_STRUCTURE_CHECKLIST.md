# KALDRA Frontend — Structure Checklist
**Last Updated:** 2025-11-24

## Estrutura Esperada
4iam_frontend/
 ├── app/
 ├── components/
 ├── lib/api/
 ├── public/
 ├── styles/
 ├── .env.example
 ├── package.json
 └── next.config.js

## Checklist

### 1. Páginas
[x] Pastas alpha, geo, product, safeguard, kaldra
[x] layout.tsx presente
[x] page.tsx presente

### 2. Componentes
[x] components/ui existe
[x] components/kaldra existe

### 3. API Client
[x] kaldra_client.ts com retry + fallback
[x] types.ts atualizado com schema v2.1

### 4. Env Vars
[x] .env.example atualizado
[x] NEXT_PUBLIC_ variables configuradas

### 5. Build
[x] npm install funciona
[x] npm run build funciona

### 6. Deploy
[x] Nada hardcoded para localhost
[x] Uso correto de NEXT_PUBLIC_KALDRA_API_URL

## Recomendações Futuras
- Criar componentes unificados de cards
- Integrar Visual Engine no dashboard
- Criar modo mobile
- Criar landing de marketing
