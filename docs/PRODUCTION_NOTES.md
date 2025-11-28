# PRODUCTION_NOTES.md

## 1. Purpose

This document captures **practical notes** about running the `4iam_frontend/` application in **production**, including:

- Differences from local development.
- How it integrates with the KALDRA API on Render.
- Operational considerations after deployment to Vercel.

---

## 2. Environments Overview

We consider three main environments:

1. **Local**
   - Frontend: `npm run dev` on developer machine.
   - Backend: optional (may hit Render or use mocks).
   - `NEXT_PUBLIC_KALDRA_API_MODE=mock` or `remote`.

2. **Preview (Vercel)**
   - Auto-deployed from branches or PRs.
   - Used to validate features before merging.

3. **Production (Vercel)**
   - Public-facing environment.
   - Connects to the **production** KALDRA API Gateway on Render.

---

## 3. Behavior Differences: Local vs Production

### 3.1 Local

- Frequent code changes and hot reload.
- Safe to use mock mode:
  - `NEXT_PUBLIC_KALDRA_API_MODE=mock`
- No strict uptime expectations.

### 3.2 Production

- Must use:
  - `NEXT_PUBLIC_KALDRA_API_MODE=remote`
  - `NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-core-api.onrender.com`
- Visitors expect:
  - Stable behavior.
  - Consistent responses from the KALDRA Engine.
- Any error from the backend should be:
  - Logged.
  - Handled gracefully in the UI (no raw stack traces).

---

## 4. Render Backend Integration

- The frontend talks to the backend via `NEXT_PUBLIC_KALDRA_API_URL`.
- Key endpoint for verification:
  - `/engine/kaldra/signal`
- CORS must allow:
  - Vercel production domain(s), e.g.:
    - `https://4iam-frontend.vercel.app`
    - `https://4iam.ai`

If production CORS issues appear:

1. Check Network tab for `CORS` errors.
2. Update CORS config in `kaldra_api`.
3. Redeploy backend and test again.

---

## 5. Logging and Monitoring

At the frontend level:

- Use browser DevTools for ad-hoc debugging.
- For production-grade monitoring (future):
  - Add analytics + error tracking.
  - Link frontend events to backend logs (via request IDs, correlation IDs).

At the backend level (Render):

- API logs should show:
  - Requests from Vercel domains.
  - Status codes for key endpoints like `/engine/kaldra/signal`.

---

## 6. Release Process (High-Level)

1. Implement and test changes locally.
2. Run any available unit tests / integration tests.
3. Commit and push to main branch.
4. Vercel auto-deploys to production.
5. Perform quick smoke test:
   - Visit Vercel URL / custom domain.
   - Hit `/alpha` and send a signal.
   - Verify 200 OK from `/engine/kaldra/signal`.
6. Document relevant findings here (e.g., performance, issues, observations).

---

## 7. Common Issues & Playbook

### 7.1 Issue: Backend returns 500

- Symptoms:
  - UI shows error state.
  - Network tab shows 500 from Render.
- Actions:
  - Check Render logs.
  - Fix root cause in `kaldra_core` / `kaldra_api`.
  - Redeploy backend.

### 7.2 Issue: CORS Error

- Symptoms:
  - Requests fail with CORS-related message.
- Actions:
  - Confirm Vercel domain is in allowed origins list.
  - Redeploy backend.
  - Re-test via browser.

### 7.3 Issue: Wrong API URL

- Symptoms:
  - Requests go to `localhost` or an outdated URL.
- Actions:
  - Check `NEXT_PUBLIC_KALDRA_API_URL` in Vercel settings.
  - Re-deploy after fix.

---

## Future Implementations

- Add a **Production Runbook** detailing:
  - Incident response.
  - On-call expectations.
- Implement structured logging from the frontend (e.g. sending logs to a logging service).
- Define SLAs / SLOs for KALDRA Alpha and other dashboards.

---

## Enhancements (Short/Medium Term)

- Add a small **health badge** in the UI indicating:
  - API status (UP/DOWN).
  - API mode (mock/remote).
- Create a **"System Status"** page under `/status` or `/docs/status`.
- Document typical performance baselines (load time, time-to-first-signal).

---

## Research Track (Long Term)

- Explore end-to-end observability:
  - Tracing from frontend user actions to backend processing.
- Evaluate multi-cloud or multi-region setups.
- Investigate blue/green or canary deployment strategies for both frontend and backend.

---

## Known Limitations

- Current setup relies heavily on manual smoke tests.
- No automatic rollback from Vercel based on health checks yet.
- Frontend errors are not yet centrally collected in a monitoring system.

---

## Testing

- Manual smoke tests after each production deploy:
  - Visit main dashboard.
  - Trigger at least one KALDRA signal.
  - Confirm response and basic rendering.
- Future:
  - Automated Playwright/Cypress tests that run against production or a production-like environment.

---

## Next Steps

- Keep this file updated after each **major deploy** with:
  - Known issues.
  - Lessons learned.
- Link this document from:
  - `docs/DEPLOY_FRONTEND_VERCEL.md`
  - Any higher-level `KALDRA_V2.1_RELEASE_NOTES.md` or similar release docs.
