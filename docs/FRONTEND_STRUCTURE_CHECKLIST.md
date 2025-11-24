# 4iam.ai Frontend — Structure Checklist

Este checklist garante que a estrutura mínima do frontend está íntegra
antes de cada deploy.

## 1. Estrutura de Diretórios (4iam_frontend/)

Verifique se existem:

- `4iam_frontend/package.json`
- `4iam_frontend/tsconfig.json`
- `4iam_frontend/next.config.mjs` ou `next.config.js`
- `4iam_frontend/tailwind.config.js` (se aplicável)
- `4iam_frontend/app/` (App Router)
- `4iam_frontend/app/(alpha)/` ou páginas equivalentes
- `4iam_frontend/app/lib/`
- `4iam_frontend/app/lib/kaldra_client.ts`
- `4iam_frontend/app/lib/api/types.ts`
- `4iam_frontend/public/`
- `4iam_frontend/styles/`

## 2. Dependências

Rodar localmente, na raiz do frontend:

```bash
cd 4iam_frontend
npm install
npm run dev

Se tudo subir sem erros, a base estrutural está OK.

3. Ambiente

Verificar:
	•	.env.local presente apenas localmente (NÃO comitado).
	•	.env.example atualizado com:
	•	NEXT_PUBLIC_KALDRA_API_MODE
	•	NEXT_PUBLIC_KALDRA_API_URL

4. Integração com Backend

Checklist rápido:
	•	kaldra_client.ts:
	•	Lê NEXT_PUBLIC_KALDRA_API_MODE
	•	Lê NEXT_PUBLIC_KALDRA_API_URL
	•	Implementa retry + fallback para mocks
	•	Páginas que chamam o KALDRA:
	•	Usam o client centralizado (não reinventar fetch em cada página).
	•	Lidam com estados: loading, erro, resultado.

5. Antes de Deployar para Vercel
	•	npm run lint (se configurado)
	•	npm run build passa localmente
	•	.env.local NÃO comitado
	•	Variáveis de ambiente configuradas no painel do Vercel
	•	DEPLOY_FRONTEND_VERCEL.md revisado, se algo mudou
