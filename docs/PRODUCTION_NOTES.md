# KALDRA Frontend — Production Notes

**Version**: 1.0  
**Last Updated**: 2025-11-24  
**Status**: Active

---

## 1. Production Overview

The **4iam.ai Frontend** is the visual interface for the KALDRA Narrative Intelligence ecosystem. In production, it serves as a "Thin Client" that delegates complex semantic inference to the Master Engine API while handling visualization, user interaction, and state management locally.

---

## 2. Runtime Architecture

```mermaid
graph LR
    Browser[User Browser] -->|HTTPS| Vercel[4iam.ai Frontend\n(Next.js / Vercel)]
    Vercel -->|API Calls| Render[KALDRA API Gateway\n(Render.com)]
    Render -->|Inference| Engine[Master Engine V2]
    Engine -->|Signal| Render
    Render -->|JSON| Vercel
```

- **Client-Side Rendering (CSR)**: Most interactions (signal generation) happen client-side via `kaldra_client.ts`.
- **Static Generation (SSG)**: Marketing and landing pages are statically generated for performance.
- **API Communication**: Direct calls from the browser to the Render backend (bypassing Next.js API routes for lower latency).

---

## 3. Environment Configuration

The frontend behavior is strictly controlled by Environment Variables.

### Modes
1. **Mock Mode** (`NEXT_PUBLIC_KALDRA_API_MODE=mock`)
   - **Use Case**: Local development, UI testing, Staging (optional).
   - **Behavior**: Bypasses network calls. Returns deterministic mock data from `mock_data.ts`.
   - **Safety**: Zero risk of backend overload or cost.

2. **Real Mode** (`NEXT_PUBLIC_KALDRA_API_MODE=real`)
   - **Use Case**: Production, Integration Testing.
   - **Behavior**: Connects to `NEXT_PUBLIC_KALDRA_API_URL`.
   - **Resilience**: Includes retry logic and fallback mechanisms.

---

## 4. Error Handling & Resilience

The `kaldra_client.ts` implements a robust strategy for production reliability:

1. **Retry Logic**:
   - If a network request fails, it retries up to **3 times**.
   - **Exponential Backoff**: Waits 1s, 2s, then 4s between attempts to avoid thundering herd problems.

2. **Timeouts**:
   - Hard timeout of **15 seconds** per request to prevent hanging UI states.

3. **Graceful Fallback**:
   - **Critical Safety Feature**: If the Real API is unreachable (down, timeout, or 500 error) after all retries, the client **automatically falls back to Mock Data**.
   - This ensures the user *always* sees a result, even if the backend is catastrophic.
   - A console error is logged for debugging: `[KALDRA Client] Real API failed, falling back to mock data`.

---

## 5. Current Limitations

- **Authentication**: Currently open access. Future versions will require JWT/Auth0.
- **Rate Limiting**: Enforced by the Backend (Render), not the Frontend.
- **Observability**: Relies on browser console and Vercel runtime logs. No centralized frontend telemetry (e.g., Sentry) yet.

---

## 6. Future Roadmap

- **Real Embeddings**: Frontend will send text to backend, which will use OpenAI/HuggingFace embeddings instead of heuristics.
- **Streaming Responses**: Support for streaming tokens/signals for lower perceived latency.
- **User Accounts**: Save history of signals and user preferences.
- **Telemetry**: Integration with Vercel Analytics or PostHog.

---

## 7. Docs Relacionados
- `DEPLOY_FRONTEND_VERCEL.md` — Passo-a-passo de deploy.
- `ENV_REFERENCE_FRONTEND.md` — Matriz de envs por ambiente.
- `FRONTEND_STRUCTURE_CHECKLIST.md` — Checklist para integridade do frontend.

---

**Maintained by**: 4IAM.AI Engineering Team
