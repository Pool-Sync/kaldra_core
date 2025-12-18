# KALDRA Frontend - Production Notes

**Version**: 2.1  
**Framework**: Next.js 14 (App Router)  
**Deployment**: Vercel

---

## 🌐 API Configuration

### Environment Variables

The KALDRA frontend uses environment variables to configure API connectivity:

| Variable | Purpose | Values |
|----------|---------|--------|
| `NEXT_PUBLIC_KALDRA_API_MODE` | API mode | `mock` or `real` |
| `NEXT_PUBLIC_KALDRA_API_URL` | Backend URL | API Gateway endpoint |

**Important**: Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

---

### Configuration Files

#### `.env.local` (Local Development)

**Location**: `4iam_frontend/.env.local`  
**Git**: Ignored (never commit!)

**Development (Mock Mode)**:
```bash
NEXT_PUBLIC_KALDRA_API_MODE=mock
NEXT_PUBLIC_KALDRA_API_URL=http://localhost:8000
```

**Development (Real API)**:
```bash
NEXT_PUBLIC_KALDRA_API_MODE=real
NEXT_PUBLIC_KALDRA_API_URL=http://localhost:8000
```

**Production Testing**:
```bash
NEXT_PUBLIC_KALDRA_API_MODE=real
NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-core-api.onrender.com
```

---

#### `.env.example` (Template)

**Location**: `4iam_frontend/.env.example`  
**Git**: Committed (template only)

Use as reference to create your `.env.local`:
```bash
cp .env.example .env.local
# Edit .env.local with your values
```

---

### Vercel Configuration

**Location**: Vercel Dashboard → Settings → Environment Variables

Set for **all environments** (Production, Preview, Development):

```bash
NEXT_PUBLIC_KALDRA_API_MODE=real
NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-core-api.onrender.com
```

**Update URL** with your actual Render deployment URL.

---

## 🔌 API Client Behavior

### File: `app/lib/api/kaldra_client.ts`

The KALDRA API client automatically handles:

#### 1. Mode Switching

```typescript
const API_MODE = process.env.NEXT_PUBLIC_KALDRA_API_MODE || "mock";

if (API_MODE === "mock") {
  // Use local mock data
  return getMockKaldraSignal(text);
} else {
  // Call real API
  const response = await fetch(`${API_URL}/engine/kaldra/signal`, {...});
}
```

#### 2. Retry Logic

- **Max Retries**: 3 attempts
- **Backoff**: Exponential (1s, 2s, 4s)
- **Timeout**: 15 seconds per request

```typescript
const MAX_RETRIES = 3;
const TIMEOUT_MS = 15000;

// Automatic retry with exponential backoff
for (let attempt = 0; attempt <= retries; attempt++) {
  try {
    // Attempt request
  } catch (error) {
    const backoffMs = Math.pow(2, attempt) * 1000;
    await sleep(backoffMs);
  }
}
```

#### 3. Automatic Fallback

If real API fails after all retries:
- Falls back to mock data
- Logs warning to console
- Ensures UI never breaks

```typescript
try {
  return await fetchWithRetry(...);
} catch (error) {
  console.error("Real API failed, falling back to mock data:", error);
  return getMockKaldraSignal(text);
}
```

#### 4. Logging

**Mock Mode**:
```
[KALDRA Client] Using mock data (NEXT_PUBLIC_KALDRA_API_MODE=mock)
```

**Real Mode**:
```
[KALDRA Client] Using real API at https://... (NEXT_PUBLIC_KALDRA_API_MODE=real)
```

**Errors**:
```
[KALDRA Client] Real API failed, falling back to mock data: <error>
```

---

## 🚀 Deployment Workflow

### 1. Local Development

```bash
# Start frontend
cd 4iam_frontend
npm run dev

# Visit http://localhost:3000
```

**Mode**: Mock (no backend needed)

---

### 2. Local Testing with Backend

```bash
# Terminal 1: Start backend
cd kaldra_core
source .venv/bin/activate
uvicorn kaldra_api.main:app --reload --port 8000

# Terminal 2: Start frontend
cd 4iam_frontend
# Edit .env.local: NEXT_PUBLIC_KALDRA_API_MODE=real
npm run dev
```

**Mode**: Real (connects to localhost:8000)

---

### 3. Production Deployment

**Backend** (Render):
1. Deploy backend first
2. Note the URL (e.g., `https://kaldra-core-api.onrender.com`)
3. Ensure `/health` endpoint works

**Frontend** (Vercel):
1. Set environment variables in Vercel dashboard
2. Deploy from GitHub
3. Test production URL

**See**: [DEPLOY_FRONTEND_VERCEL.md](./DEPLOY_FRONTEND_VERCEL.md) for detailed steps

---

## 🧪 Testing

### Verify API Mode

**Open Browser Console** (F12):

**Mock Mode**:
```
[KALDRA Client] Using mock data (NEXT_PUBLIC_KALDRA_API_MODE=mock)
```

**Real Mode**:
```
[KALDRA Client] Using real API at https://kaldra-core-api.onrender.com
```

---

### Test API Connectivity

**Network Tab** (F12 → Network):

1. Generate a KALDRA signal
2. Look for POST request to `/engine/kaldra/signal`
3. Status should be `200 OK`
4. Response should contain `archetype`, `bias_score`, etc.

---

### Health Check

```typescript
import { checkApiHealth } from './app/lib/api/kaldra_client';

const isHealthy = await checkApiHealth();
console.log('API Health:', isHealthy);
```

---

## 🔐 Security

### Environment Variables

✅ **DO**:
- Use `.env.local` for local development
- Set variables in Vercel dashboard for production
- Use `NEXT_PUBLIC_` prefix for client-side variables

❌ **DON'T**:
- Commit `.env.local` to Git
- Hardcode API URLs in code
- Expose sensitive keys (backend-only keys should stay on backend)

---

### CORS

**Frontend**: No configuration needed (Next.js handles it)

**Backend**: Must whitelist frontend URL

```python
# kaldra_api/main.py
origins = [
    "http://localhost:3000",
    "https://your-app.vercel.app",  # Add your Vercel URL
]
```

---

## 📊 Monitoring

### Console Logs

Check browser console for:
- API mode confirmation
- Request/response logs
- Error messages
- Fallback warnings

### Network Requests

Monitor in DevTools → Network:
- Request URL
- Response status
- Response time
- Payload size

### Vercel Analytics

Enable in Vercel dashboard:
- Page views
- Performance metrics
- Error rates

---

## 🐛 Common Issues

### Issue: Using Mock Data in Production

**Symptom**: Console shows "Using mock data" even with `NEXT_PUBLIC_KALDRA_API_MODE=real`

**Solution**:
1. Check Vercel environment variables
2. Ensure variable name is exactly `NEXT_PUBLIC_KALDRA_API_MODE`
3. Redeploy after changing env vars
4. Hard refresh browser (Cmd+Shift+R)

---

### Issue: CORS Error

**Symptom**: API calls fail with CORS error in console

**Solution**:
1. Add Vercel URL to backend CORS whitelist
2. Set `FRONTEND_URL` env var in Render
3. Redeploy backend

---

### Issue: Slow API Responses

**Symptom**: First request takes 10-30 seconds

**Cause**: Render free tier spins down after inactivity

**Solutions**:
1. Upgrade Render plan (Standard: $7/mo)
2. Client already has 15s timeout + fallback
3. Show loading state in UI

---

## 📚 Related Documentation

- [Vercel Deployment Guide](./DEPLOY_FRONTEND_VERCEL.md)
- [Backend Deployment Guide](../docs/DEPLOY_BACKEND_RENDER.md)
- [API Gateway Walkthrough](../docs/API_GATEWAY_WALKTHROUGH.md)
- [KALDRA Client Source](./app/lib/api/kaldra_client.ts)

---

**Maintained by**: 4IAM.AI Engineering Team  
**Last Review**: 2025-11-23
