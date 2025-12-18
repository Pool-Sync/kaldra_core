# ENV_REFERENCE_FRONTEND.md

## 1. Purpose

This document defines and explains all **frontend environment variables** used by the `4iam_frontend/` application.

It focuses on:

- How the frontend connects to the **KALDRA API Gateway** on Render.
- How to switch between **mock** and **remote** API modes.
- How to configure **Vercel** environment variables correctly for production.

---

## 2. Frontend Environment Context

The `4iam_frontend/` project runs in three main contexts:

1. **Local Development**
   - Run via `npm run dev` or `yarn dev`.
   - Often uses `NEXT_PUBLIC_KALDRA_API_MODE=mock` while the backend is evolving.

2. **Vercel Preview**
   - Automatic deployments from feature branches or PRs.
   - Used to validate UI/UX and integration behavior.

3. **Vercel Production**
   - Main public URL for `4iam.ai`.
   - Must point to the **production API Gateway** on Render.

---

## 3. Environment Variables Overview

All variables listed here are **public** (prefixed with `NEXT_PUBLIC_`) and will be embedded into the frontend bundle.  
Do **not** put secrets here.

### 3.1 Core Variables

#### `NEXT_PUBLIC_KALDRA_API_MODE`

- **Type**: string (`"mock"` | `"remote"`)
- **Scope**: Frontend only (public)
- **Description**: Controls whether the frontend uses **mocked data** or **real API calls**.
- **Typical Values**:
  - `mock`
    - Uses internal mock data (e.g. `app/lib/api/mock_data.ts`).
    - Safe when the backend is offline or unstable.
  - `remote`
    - Uses the **KALDRA API Gateway** on Render or another backend.
    - Requires `NEXT_PUBLIC_KALDRA_API_URL` to be set correctly.

- **Recommended configuration**:
  - Local dev: `mock` (or `remote` when testing full integration)
  - Vercel preview: `remote` (to test real flows)
  - Vercel production: `remote`

---

#### `NEXT_PUBLIC_KALDRA_API_URL`

- **Type**: string (URL)
- **Scope**: Frontend only (public)
- **Description**: Base URL for the KALDRA API Gateway.
- **Example (Render)**:
  - `https://kaldra-core-api.onrender.com`

- **Usage**:
  - The frontend API layer (e.g. `app/lib/api/config.ts`) should build endpoints like:
    - `${NEXT_PUBLIC_KALDRA_API_URL}/engine/kaldra/signal`
    - `${NEXT_PUBLIC_KALDRA_API_URL}/status/health`

- **Important**:
  - Must include `https://` and **no trailing slash**.
  - Must be aligned with CORS configuration on the API Gateway.

---

### 3.2 Optional / Future-Proof Variables

These variables may not be used immediately but are reserved for future production hardening.

#### `NEXT_PUBLIC_FRONTEND_ENV` (optional)

- **Type**: string (`"local"` | `"preview"` | `"production"`)
- **Description**: Helps the frontend show small indicators (e.g. badges) to distinguish environments.

#### `NEXT_PUBLIC_ANALYTICS_KEY` (optional)

- **Type**: string
- **Description**: Analytics provider public key (e.g. PostHog, Plausible).
- **Note**: Do **not** use this for secrets; only public keys.

---

## 4. Vercel Configuration

When creating the project on **Vercel**, set the following environment variables under:

> Project → Settings → Environment Variables

**Required:**

- `NEXT_PUBLIC_KALDRA_API_MODE=remote`
- `NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-core-api.onrender.com`

**Recommended (future):**

- `NEXT_PUBLIC_FRONTEND_ENV=production`

For preview environments, you can override:

- `NEXT_PUBLIC_KALDRA_API_MODE=remote` or `mock`
- `NEXT_PUBLIC_FRONTEND_ENV=preview`

---

## 5. Local Development Setup

For local development, you can use a `.env.local` file under `4iam_frontend/`:

```bash
NEXT_PUBLIC_KALDRA_API_MODE=mock
NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-core-api.onrender.com
NEXT_PUBLIC_FRONTEND_ENV=local
```

When you want to test real integration locally:

```bash
NEXT_PUBLIC_KALDRA_API_MODE=remote
NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-core-api.onrender.com
NEXT_PUBLIC_FRONTEND_ENV=local
```

---

## Future Implementations

* Add dedicated variables for:

  * Error tracking (e.g. `NEXT_PUBLIC_SENTRY_DSN`).
  * Feature flags (e.g. `NEXT_PUBLIC_FEATURE_ALPHA_SIGNALS`).
* Introduce environment-specific defaults through a centralized config module.

---

## Enhancements (Short/Medium Term)

* Document concrete examples of `.env.local`, `.env.preview`, `.env.production`.
* Add a small **Environment Badge** component on the UI using `NEXT_PUBLIC_FRONTEND_ENV`.
* Extend `app/lib/api/config.ts` to log which mode (`mock` vs `remote`) is currently active.

---

## Research Track (Long Term)

* Evaluate dynamic runtime configuration (pulling config from an API instead of build-time envs).
* Explore multi-region deployments and how environment variables map to regional endpoints.
* Investigate using a configuration service (e.g. Doppler, Vault) for non-public values.

---

## Known Limitations

* All `NEXT_PUBLIC_*` variables are visible in the browser; no secrets allowed.
* Changing env variables on Vercel requires a new deployment to propagate.
* Misconfigured `NEXT_PUBLIC_KALDRA_API_URL` will only show up as runtime errors in the Network tab.

---

## Testing

* Manual:

  * Inspect `window.__NEXT_DATA__` to confirm env usage.
  * Open DevTools → Network and verify requests go to `NEXT_PUBLIC_KALDRA_API_URL`.
* Automated (future):

  * Add a small Jest/Playwright test that asserts `process.env.NEXT_PUBLIC_KALDRA_API_MODE` is set in CI.

---

## Next Steps

* Ensure this file exists in `docs/ENV_REFERENCE_FRONTEND.md`.
* Verify Vercel config matches the values documented here.
* Link this document from:

  * `docs/DEPLOY_FRONTEND_VERCEL.md`
  * `docs/PRODUCTION_NOTES.md`
