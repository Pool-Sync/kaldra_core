# DEPLOY_FRONTEND_VERCEL.md

## 1. Goal

Verify the frontend documentation and **deploy `4iam_frontend/` to Vercel**, ensuring:

- Correct environment variables.
- Successful build and deploy.
- Working connection to the **Render backend** (`kaldra-core-api.onrender.com`).
- No CORS issues between Vercel and Render.

---

## 2. Prerequisites

- GitHub repository with `4iam_frontend/` at the root (or clearly defined).
- Vercel account connected to GitHub.
- KALDRA API Gateway deployed on Render at:

> `https://kaldra-core-api.onrender.com`

- Documentation files created:
  - `docs/ENV_REFERENCE_FRONTEND.md`
  - `docs/FRONTEND_STRUCTURE_CHECKLIST.md`
  - `docs/PRODUCTION_NOTES.md`

---

## 3. Documentation Verification

Before deploying, verify that the following files exist and are coherent:

1. **`docs/ENV_REFERENCE_FRONTEND.md`**
   - [ ] Describes `NEXT_PUBLIC_KALDRA_API_MODE`.
   - [ ] Describes `NEXT_PUBLIC_KALDRA_API_URL`.
   - [ ] Specifies recommended values for Vercel production.

2. **`docs/FRONTEND_STRUCTURE_CHECKLIST.md`**
   - [ ] References `4iam_frontend/` as the root frontend project.
   - [ ] Describes main sections: `app/`, `components/`, `design_system/`, `lib/`, `public/`, `styles/`.

3. **`docs/PRODUCTION_NOTES.md`**
   - [ ] Explains how production differs from local development.
   - [ ] Mentions integration with the Render backend.

After verification:

- [ ] Commit and push documentation changes:
  - Example:
    ```bash
    git add docs/
    git commit -m "docs: add frontend env + deploy + production notes"
    git push origin main
    ```

---

## 4. Importing the Project into Vercel

1. Go to **Vercel Dashboard** → "Add New Project".
2. Select the GitHub repo containing `4iam_frontend/`.
3. Set the **project root** (if necessary) to:

   - `4iam_frontend/`

4. Confirm the framework detection:
   - Framework: **Next.js**
   - Build command: `next build` (default).
   - Output directory: `.next` (default).

---

## 5. Environment Variables on Vercel

In the Vercel project settings, configure:

**Required for production:**

- `NEXT_PUBLIC_KALDRA_API_MODE=remote`
- `NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-core-api.onrender.com`

(Optional but recommended):

- `NEXT_PUBLIC_FRONTEND_ENV=production`

Apply these to:

- **Production** environment.
- **Preview** environment (can optionally use different values).

---

## 6. First Deployment

Once environment variables are configured:

1. Trigger a new deployment by:
   - Clicking **"Deploy"** in Vercel, or
   - Pushing a new commit to the main branch.
2. Wait for the deployment to finish.
3. Confirm:
   - Build **succeeds**.
   - A **Production URL** is generated (e.g. `https://4iam-frontend.vercel.app`).

> **User Review Required:** Confirm deployment success on the Vercel dashboard.

---

## 7. Smoke Test: Live Signal → Render Backend

With the deployment URL (e.g. `https://4iam-frontend.vercel.app`):

1. Open the site in a browser.
2. Navigate to the **KALDRA Alpha** area (e.g. `/alpha`).
3. Perform an action that triggers a **KALDRA signal** request (e.g. clicking “Send signal” / “Analyze” / similar button).
4. Open **DevTools → Network**.
5. Filter by `fetch` or `XHR`.
6. Verify a request is sent to:

   > `https://kaldra-core-api.onrender.com/engine/kaldra/signal`

7. Confirm:
   - [ ] HTTP status is **200 OK**.
   - [ ] Response body is consistent with the expected KALDRA Signal schema (at least at a high level).

If the response is not 200 or there are CORS errors, proceed to the next section.

---

## 8. CORS Adjustment (If Needed)

If you see errors like:

- `CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource`
- `CORS error` in DevTools

Then:

1. Identify the **exact Vercel domain**, e.g.:
   - `https://4iam-frontend.vercel.app`
   - Custom domain: `https://4iam.ai`

2. In the **KALDRA API Gateway (`kaldra_api/main.py` or config)**, ensure CORS is configured to allow this origin.

Example for FastAPI with `CORSMiddleware`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

allowed_origins = [
    "http://localhost:3000",
    "https://4iam-frontend.vercel.app",  # Vercel project URL
    "https://4iam.ai",                   # Custom domain (if configured)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. Redeploy the backend (Render) after updating CORS config.
4. Repeat the smoke test and verify that:

   * [ ] The frontend can call `/engine/kaldra/signal` without CORS errors.
   * [ ] Response is 200 OK.

---

## 9. Failure Modes & Rollback

If deployment fails or the site breaks:

* **Build time errors**:

  * Fix the root cause locally.
  * Commit and push again to trigger a new build.
* **Runtime errors**:

  * Use the Vercel logs to inspect errors.
  * Temporarily switch `NEXT_PUBLIC_KALDRA_API_MODE=mock` to decouple UI from backend issues.
* **CORS errors**:

  * Update `kaldra_api` CORS allowed origins.
  * Redeploy backend.

---

## Future Implementations

* Add GitHub Actions or Vercel checks that:

  * Validate the presence of environment variables before deploy.
  * Run a minimal smoke test script post-deploy.
* Automate notification to Slack/Email after successful production deploys.

---

## Enhancements (Short/Medium Term)

* Add a dedicated **"Status"** section in the frontend UI that shows:

  * Current API mode (`mock` vs `remote`).
  * API health status from `/status/health`.
* Improve error messages when backend calls fail (user-friendly copy).

---

## Research Track (Long Term)

* Explore **multi-region** deployments and latency-based routing between Vercel and backend.
* Investigate **edge functions** for pre-processing or caching KALDRA signals at the edge.
* Evaluate canary releases and feature flags for gradual rollout.

---

## Known Limitations

* Manual verification is still required for:

  * Vercel deployment success.
  * Network requests in DevTools.
* CORS configuration must be kept in sync between:

  * Vercel domains.
  * Render backend config.

---

## Testing

* Current:

  * Manual smoke tests via browser + DevTools.
* Future:

  * Basic integration tests using Playwright or Cypress hitting the Vercel URL.
  * API contract tests to ensure `/engine/kaldra/signal` returns the expected shape.

---

## Next Steps

* Create/verify this document at `docs/DEPLOY_FRONTEND_VERCEL.md`.
* Ensure `docs/ENV_REFERENCE_FRONTEND.md` and `docs/FRONTEND_STRUCTURE_CHECKLIST.md` are consistent with this plan.
* Perform the first full **Vercel production deployment** and record findings in:

  * `docs/PRODUCTION_NOTES.md`
