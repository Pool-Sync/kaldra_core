# Deploying KALDRA Frontend to Vercel

**Version**: 1.0  
**Last Updated**: 2025-11-24  
**Status**: Verified

---

## 🧠 Overview

The **4iam.ai Frontend** is a Next.js 14 application that serves as the user interface for the KALDRA ecosystem. It consumes the KALDRA Master Engine via the API Gateway deployed on Render.

- **Repo Path**: `4iam_frontend/`
- **Framework**: Next.js 14 (App Router)
- **Backend**: `https://kaldra-core-api.onrender.com` (Production)

---

## ✅ Prerequisites

1. **Vercel Account**: [Create one here](https://vercel.com/signup).
2. **GitHub Repository**: Access to `Pool-Sync/kaldra_core`.
3. **Backend Deployed**: The API Gateway must be running on Render (or another provider).

---

## 🚀 Step-by-Step Deployment

### 1. Import Project
1. Go to your [Vercel Dashboard](https://vercel.com/dashboard).
2. Click **"Add New..."** -> **"Project"**.
3. Import the `Pool-Sync/kaldra_core` repository.

### 2. Configure Project Settings
Vercel will detect Next.js, but you need to point it to the correct folder.

- **Framework Preset**: Next.js
- **Root Directory**: Click "Edit" and select `4iam_frontend`.
  > ⚠️ **Crucial**: If you don't set this, the build will fail because it won't find `package.json`.

### 3. Build Settings (Default)
Leave these as default unless you have a custom setup:
- **Build Command**: `npm run build`
- **Install Command**: `npm install`
- **Output Directory**: `.next` (default)

### 4. Environment Variables
Configure the connection to the backend.

| Variable | Value (Production) | Description |
|---|---|---|
| `NEXT_PUBLIC_KALDRA_API_MODE` | `real` | Enables real API calls (disables mocks). |
| `NEXT_PUBLIC_KALDRA_API_URL` | `https://kaldra-core-api.onrender.com` | URL of your deployed backend. |

> **Tip**: You can also set these for "Preview" environments if you want pull requests to use the real backend (or keep them as `mock` for safety).

### 5. Deploy
Click **"Deploy"**. Vercel will:
1. Clone the repo.
2. Install dependencies in `4iam_frontend/`.
3. Build the Next.js app.
4. Assign a domain (e.g., `kaldra-core-frontend.vercel.app`).

---

## 🔍 Verification

Once deployed, verify the integration:

1. **Open the App**: Visit the provided Vercel URL.
2. **Check Network**: Open Developer Tools (F12) -> Network tab.
3. **Trigger Signal**: Go to the Alpha or Geo page and request a signal.
4. **Validate Request**:
   - Ensure the request goes to `https://kaldra-core-api.onrender.com/...`.
   - Check for `200 OK` status.
   - Verify the response contains KALDRA signal data (Archetype, Risk, etc.).

### Troubleshooting

**Issue**: "Network Error" or "Failed to fetch"
- **Check**: Is the backend URL correct in Env Vars? (No trailing slash issues?)
- **Check**: Is the Backend running on Render? (Check Render logs)
- **Check**: CORS. The Backend must allow the Vercel domain. (Already configured to allow `*` or specific domains in `main.py`).

**Issue**: App shows mock data despite `real` mode
- **Check**: Did you redeploy after changing Env Vars? Vercel requires a redeploy to bake in new `NEXT_PUBLIC_` variables.

---

## Referências Relacionadas
- `docs/ENV_REFERENCE_FRONTEND.md` — Referência completa de envs.
- `docs/FRONTEND_STRUCTURE_CHECKLIST.md` — Checklist estrutural antes do deploy.
- `docs/PRODUCTION_NOTES.md` — Notas de operação em produção.

---

**Maintained by**: 4IAM.AI Engineering Team
