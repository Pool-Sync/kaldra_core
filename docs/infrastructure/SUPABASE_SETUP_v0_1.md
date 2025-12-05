# Supabase Integration v0.1 - Setup Guide

**Status:** ✅ Scaffolding Complete  
**Date:** December 2025

---

## Files Created

### Backend
- `ENV_SUPABASE.example` - Environment template
- `src/infra/supabase_client.py` - Client initialization
- `src/infra/db/supabase_repository.py` - Repository layer
- `src/api/routes/supabase_test.py` - Test endpoint

### Frontend
- `frontend/.env.example` - Environment template
- `frontend/lib/supabase.ts` - Client initialization

---

## Manual Setup Required

### 1. Backend Environment

Create `.env` file in project root:

```bash
SUPABASE_URL=https://YOUR-PROJECT-URL.supabase.co
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY_HERE
```

**Get keys from:** Supabase Dashboard → Project Settings → API

### 2. Frontend Environment

Create `frontend/.env.local`:

```bash
NEXT_PUBLIC_SUPABASE_URL=https://YOUR-PROJECT-URL.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=YOUR_ANON_KEY_HERE
```

### 3. Render (Backend Deployment)

Add environment variables:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

### 4. Vercel (Frontend Deployment)

Add environment variables:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

---

## Testing

### Backend Test

```bash
curl http://localhost:8000/api/supabase/test
```

Expected: `{"status": "ok", "rows": 0}`

### Frontend Test

```tsx
import { supabase } from '@/lib/supabase'

const { data, error } = await supabase.from('profiles').select('*')
```

---

## Security Notes

⚠️ **Never commit:**
- `.env` files
- Real API keys
- Service role keys

✅ **Safe to commit:**
- `.env.example` files
- Placeholder values

---

## Next Steps

1. Create Supabase tables (`profiles`, `signals`, etc.)
2. Integrate KALDRA signals with Supabase
3. Add caching layer (Redis)
