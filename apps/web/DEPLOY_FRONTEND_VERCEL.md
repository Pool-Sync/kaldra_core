# KALDRA Frontend Deployment Guide - Vercel

**Version**: 2.1  
**Last Updated**: 2025-11-23  
**Platform**: Vercel

---

## 📋 Prerequisites

- GitHub account with `kaldra_core` repository
- Vercel account (free tier works)
- Backend deployed on Render (e.g., `https://kaldra-core-api.onrender.com`)

---

## 🚀 Deployment Steps

### 1. Prepare Frontend Configuration

Ensure your local `.env.local` is configured for production testing:

```bash
# 4iam_frontend/.env.local
NEXT_PUBLIC_KALDRA_API_MODE=real
NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-core-api.onrender.com
```

**Test locally first**:
```bash
cd 4iam_frontend
npm run dev
# Visit http://localhost:3000 and test KALDRA Alpha page
```

---

### 2. Create Project on Vercel

#### Option A: Using Vercel Dashboard (Recommended for Beginners)

1. Go to https://vercel.com/new
2. Click **"Import Git Repository"**
3. Select **"Add GitHub Account"** (if not connected)
4. Authorize Vercel to access your repositories
5. Find and select **`Pool-Sync/kaldra_core`**
6. Click **"Import"**

#### Configure Project Settings:

| Setting | Value | Notes |
|---------|-------|-------|
| **Project Name** | `kaldra-frontend` | Or your preferred name |
| **Framework Preset** | Next.js | Auto-detected |
| **Root Directory** | `4iam_frontend` | ⚠️ **IMPORTANT**: Click "Edit" and set this! |
| **Build Command** | `npm run build` | Default (auto-detected) |
| **Output Directory** | `.next` | Default (auto-detected) |
| **Install Command** | `npm install` | Default (auto-detected) |

**Critical**: Make sure to set **Root Directory** to `4iam_frontend`!

---

### 3. Configure Environment Variables

In the Vercel project settings:

1. Go to **"Settings" → "Environment Variables"**
2. Add the following variables:

| Variable Name | Value | Environment |
|---------------|-------|-------------|
| `NEXT_PUBLIC_KALDRA_API_MODE` | `real` | Production, Preview, Development |
| `NEXT_PUBLIC_KALDRA_API_URL` | `https://kaldra-core-api.onrender.com` | Production, Preview, Development |

**How to Add**:
1. Click **"Add New"**
2. **Key**: `NEXT_PUBLIC_KALDRA_API_MODE`
3. **Value**: `real`
4. **Environments**: Check all three (Production, Preview, Development)
5. Click **"Save"**
6. Repeat for `NEXT_PUBLIC_KALDRA_API_URL`

**Important Notes**:
- ✅ Variables starting with `NEXT_PUBLIC_` are exposed to the browser
- ✅ Update `NEXT_PUBLIC_KALDRA_API_URL` with your actual Render URL
- ✅ Use `real` mode for production to connect to live backend

---

### 4. Deploy

1. Click **"Deploy"** (blue button)
2. Wait for build (2-5 minutes first time)
3. Monitor build logs in real-time

**Build Process**:
```
1. Cloning repository...
2. Installing dependencies (npm install)...
3. Building Next.js app (npm run build)...
4. Optimizing pages...
5. Generating static pages...
6. Deployment ready ✅
```

**Expected Output**:
```
✓ Compiled successfully
✓ Linting and checking validity of types
✓ Collecting page data
✓ Generating static pages (X/X)
✓ Finalizing page optimization
```

---

### 5. Verify Deployment

#### Test Production URL

Vercel will provide a URL like: `https://kaldra-frontend.vercel.app`

**Test Checklist**:

1. **Home Page**:
   - Visit: `https://your-app.vercel.app`
   - Should load without errors

2. **KALDRA Alpha Page**:
   - Visit: `https://your-app.vercel.app/alpha` (or your route)
   - Enter text in the input
   - Click "Generate Signal"
   - Should call real API

3. **Browser Console**:
   - Open DevTools (F12)
   - Go to Console tab
   - Look for: `[KALDRA Client] Using real API mode`
   - Should see API requests to Render URL

4. **Network Tab**:
   - Open DevTools → Network
   - Generate a signal
   - Should see POST request to `https://kaldra-core-api.onrender.com/engine/kaldra/signal`
   - Status: 200 OK

---

## 🔧 Configuration Details

### Environment Variables Explained

#### `NEXT_PUBLIC_KALDRA_API_MODE`

**Purpose**: Controls API client behavior

**Values**:
- `mock`: Uses local mock data (development)
- `real`: Calls real backend API (production)

**Default**: `mock` (if not set)

**Usage in Code**:
```typescript
// app/lib/api/kaldra_client.ts
const mode = process.env.NEXT_PUBLIC_KALDRA_API_MODE || 'mock';
if (mode === 'real') {
  // Call real API
} else {
  // Use mock data
}
```

---

#### `NEXT_PUBLIC_KALDRA_API_URL`

**Purpose**: Backend API base URL

**Values**:
- Development: `http://localhost:8000`
- Production: `https://kaldra-core-api.onrender.com`

**Usage in Code**:
```typescript
const apiUrl = process.env.NEXT_PUBLIC_KALDRA_API_URL || 'http://localhost:8000';
const response = await fetch(`${apiUrl}/engine/kaldra/signal`, {...});
```

---

### Build Configuration

**Next.js Config** (`next.config.js`):
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Default settings work for Vercel
}

module.exports = nextConfig
```

**No special configuration needed** - Vercel auto-detects Next.js!

---

## 🐛 Troubleshooting

### Issue: Build Fails with "Root Directory Not Found"

**Symptom**: Build fails immediately with error about missing files

**Solution**:
1. Go to **Settings → General**
2. Find **"Root Directory"**
3. Click **"Edit"**
4. Set to: `4iam_frontend`
5. Click **"Save"**
6. Redeploy

---

### Issue: API Calls Failing (CORS Error)

**Symptom**: Frontend loads but API calls fail with CORS error

**Solution**:
1. **Check Backend CORS**: Ensure Render backend has `FRONTEND_URL` env var
   ```bash
   # In Render dashboard for kaldra-api
   FRONTEND_URL=https://your-app.vercel.app
   ```

2. **Verify in Backend Code** (`kaldra_api/main.py`):
   ```python
   origins = [
       "http://localhost:3000",
       "https://4iam-frontend.vercel.app",
       os.getenv("FRONTEND_URL")  # Your Vercel URL
   ]
   ```

3. **Redeploy Backend** after adding env var

---

### Issue: Environment Variables Not Working

**Symptom**: App uses mock data even with `NEXT_PUBLIC_KALDRA_API_MODE=real`

**Solution**:
1. **Check Variable Names**: Must start with `NEXT_PUBLIC_`
2. **Check Environments**: Ensure variables are set for "Production"
3. **Redeploy**: Changes to env vars require redeploy
4. **Clear Cache**: Hard refresh browser (Cmd+Shift+R or Ctrl+Shift+F5)

---

### Issue: Build Succeeds but Page Shows Error

**Symptom**: Build completes but page shows runtime error

**Common Causes**:

1. **Missing Environment Variables**:
   - Check Vercel dashboard → Settings → Environment Variables
   - Ensure both `NEXT_PUBLIC_*` vars are set

2. **API URL Incorrect**:
   - Verify `NEXT_PUBLIC_KALDRA_API_URL` matches Render URL
   - Test URL manually: `curl https://your-backend.onrender.com/health`

3. **Backend Not Running**:
   - Check Render dashboard
   - Ensure backend service is "Live"
   - Test health endpoint

---

### Issue: Slow Initial Load

**Symptom**: First page load is very slow (10-30 seconds)

**Cause**: Render free tier spins down after inactivity

**Solutions**:
1. **Upgrade Render Plan**: Standard plan ($7/mo) keeps service always on
2. **Implement Loading States**: Show spinner while waiting
3. **Add Timeout Handling**: Fallback to mock if API is slow

**Code Example**:
```typescript
// In kaldra_client.ts
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 15000); // 15s timeout

try {
  const response = await fetch(url, { 
    signal: controller.signal,
    // ...
  });
} catch (error) {
  if (error.name === 'AbortError') {
    console.warn('API timeout, falling back to mock');
    return getMockData();
  }
}
```

---

## 🔐 Security Best Practices

### Environment Variables

✅ **DO**:
- Use `NEXT_PUBLIC_` prefix for client-side variables
- Set different values for Preview vs Production
- Keep backend URL in environment variables

❌ **DON'T**:
- Hardcode API URLs in code
- Expose sensitive keys (API keys should be backend-only)
- Commit `.env.local` to Git

---

### CORS Configuration

**Frontend** (automatic):
- Next.js handles CORS for API routes
- No configuration needed for external API calls

**Backend** (must configure):
- Add Vercel URL to CORS whitelist
- See backend deployment guide

---

## 📈 Performance Optimization

### 1. Enable Edge Functions (Optional)

For faster global response:

```javascript
// app/api/route.ts
export const runtime = 'edge';
```

### 2. Use Image Optimization

```jsx
import Image from 'next/image';

<Image 
  src="/logo.png" 
  width={200} 
  height={100}
  alt="KALDRA"
/>
```

### 3. Enable Analytics

In Vercel dashboard:
1. Go to **Analytics** tab
2. Enable **Web Analytics**
3. Monitor performance metrics

---

## 🔄 CI/CD Pipeline

### Auto-Deploy on Push

Vercel automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update KALDRA frontend"
git push origin main
# Vercel auto-deploys ✅
```

### Preview Deployments

Every pull request gets a preview URL:
- Test changes before merging
- Share with team for review
- Automatic cleanup after merge

---

## 📊 Monitoring

### Vercel Analytics

Track:
- Page views
- Performance metrics (Core Web Vitals)
- Error rates
- Geographic distribution

### Custom Logging

Add to your code:
```typescript
// Log API calls
console.log('[KALDRA] Signal generated:', {
  archetype: signal.archetype,
  confidence: signal.confidence,
  timestamp: new Date().toISOString()
});
```

View logs in Vercel:
- Dashboard → Your Project → Logs
- Real-time function logs
- Filter by severity

---

## 🎯 Production Checklist

Before going live:

- [ ] **Backend deployed** on Render and healthy
- [ ] **Environment variables** configured in Vercel
- [ ] **Root directory** set to `4iam_frontend`
- [ ] **Build successful** (no errors)
- [ ] **Home page** loads correctly
- [ ] **KALDRA Alpha** page functional
- [ ] **API calls** working (check Network tab)
- [ ] **Console logs** show "Using real API mode"
- [ ] **CORS** configured on backend
- [ ] **Custom domain** configured (optional)
- [ ] **Analytics** enabled
- [ ] **Error tracking** set up (optional: Sentry)

---

## 🌐 Custom Domain (Optional)

### Add Custom Domain

1. Go to **Settings → Domains**
2. Click **"Add Domain"**
3. Enter your domain (e.g., `kaldra.4iam.ai`)
4. Follow DNS configuration instructions
5. Wait for SSL certificate (automatic)

**DNS Configuration**:
```
Type: CNAME
Name: kaldra (or @)
Value: cname.vercel-dns.com
```

---

## 📞 Support

### Vercel Support

- **Docs**: https://vercel.com/docs
- **Community**: https://github.com/vercel/next.js/discussions
- **Status**: https://www.vercel-status.com

### KALDRA Issues

- Check browser console for errors
- Review [KALDRA Client Documentation](../app/lib/api/kaldra_client.ts)
- Test backend health: `curl https://your-backend.onrender.com/health`

---

## 🎉 Next Steps

After successful deployment:

1. **Test All Features**:
   - KALDRA signal generation
   - News aggregation (if exposed)
   - All pages and routes

2. **Update Backend CORS**:
   ```bash
   # In Render dashboard
   FRONTEND_URL=https://your-app.vercel.app
   ```

3. **Share with Team**:
   - Production URL
   - Preview deployment workflow
   - Environment variable management

4. **Monitor Performance**:
   - Enable Vercel Analytics
   - Set up error tracking
   - Monitor API response times

---

**Deployment Checklist**:
- [ ] Vercel project created
- [ ] Root directory configured
- [ ] Environment variables set
- [ ] Build successful
- [ ] Production URL working
- [ ] API integration tested
- [ ] CORS configured
- [ ] Analytics enabled

---

**Maintained by**: 4IAM.AI Engineering Team  
**Last Review**: 2025-11-23
