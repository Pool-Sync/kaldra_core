# KALDRA Backend Deployment Guide - Render.com

**Version**: 2.1  
**Last Updated**: 2025-11-23  
**Platform**: Render.com

---

## 📋 Prerequisites

- GitHub account with `kaldra_core` repository
- Render.com account (free tier works)
- API keys for external services:
  - MediaStack API key
  - GNews API key
  - (Optional) X/Twitter, YouTube, Reddit API keys

---

## 🚀 Deployment Steps

### 1. Prepare Repository

Ensure these files are in your repository root:

```
kaldra_core/
├── Dockerfile              ✅ Created
├── render.yaml             ✅ Created
├── requirements.txt        ✅ Created
├── kaldra_api/
│   └── main.py            ✅ Updated with CORS
└── src/                   ✅ All engine code
```

**Commit and push** to GitHub:
```bash
cd /Users/niki/Desktop/kaldra_core
git add Dockerfile render.yaml requirements.txt kaldra_api/main.py
git commit -m "Add Render.com deployment configuration"
git push origin main
```

---

### 2. Create Service on Render

#### Option A: Using render.yaml (Recommended)

1. Go to https://dashboard.render.com
2. Click **"New" → "Blueprint"**
3. Connect your GitHub repository (`kaldra_core`)
4. Render will auto-detect `render.yaml`
5. Click **"Apply"**

#### Option B: Manual Setup

1. Go to https://dashboard.render.com
2. Click **"New" → "Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `kaldra-api`
   - **Region**: Oregon (or closest to you)
   - **Branch**: `main`
   - **Runtime**: Docker
   - **Dockerfile Path**: `./Dockerfile`
   - **Docker Build Context**: `.`

---

### 3. Configure Environment Variables

In the Render dashboard, go to **Environment** tab and add:

| Variable | Value | Description |
|----------|-------|-------------|
| `KALDRA_ENV` | `production` | Application environment |
| `MEDIASTACK_API_KEY` | `your_key_here` | MediaStack news API |
| `GNEWS_API_KEY` | `your_key_here` | GNews API |
| `X_BEARER_TOKEN` | `your_token_here` | X/Twitter Bearer Token (optional) |
| `X_API_KEY` | `your_key_here` | X/Twitter API Key (optional) |
| `YOUTUBE_API_KEY` | `your_key_here` | YouTube Data API (optional) |
| `REDDIT_CLIENT_ID` | `your_id_here` | Reddit Client ID (optional) |
| `REDDIT_CLIENT_SECRET` | `your_secret_here` | Reddit Client Secret (optional) |
| `FRONTEND_URL` | `https://your-frontend.vercel.app` | Frontend URL for CORS |

**Important**:
- ✅ Copy values from your local `.env.local`
- ❌ Never commit `.env.local` to Git
- ✅ Use Render's "Secret File" feature for sensitive data

---

### 4. Deploy

1. Click **"Manual Deploy" → "Deploy latest commit"**
2. Wait for build (5-10 minutes first time)
3. Monitor logs in real-time

**Build Process**:
```
1. Cloning repository...
2. Building Docker image...
3. Installing dependencies (torch, numpy, fastapi)...
4. Starting uvicorn server...
5. Health check passed ✅
6. Service live!
```

---

### 5. Verify Deployment

#### Test Health Endpoint

```bash
curl https://kaldra-api.onrender.com/health
```

**Expected**:
```json
{"status": "ok"}
```

#### Test News Aggregation

```bash
curl "https://kaldra-api.onrender.com/kaldra/news?query=AI&limit=5"
```

**Expected**: JSON with aggregated news articles

#### Test KALDRA Signal

```bash
curl -X POST https://kaldra-api.onrender.com/engine/kaldra/signal \
  -H "Content-Type: application/json" \
  -d '{"text": "Artificial intelligence is transforming the world"}'
```

**Expected**: JSON with archetype, delta_state, bias_score, etc.

---

## 🔧 Configuration Details

### Dockerfile Breakdown

```dockerfile
FROM python:3.11-slim          # Base image
WORKDIR /app                   # Set working directory
COPY requirements.txt .        # Copy dependencies
RUN pip install -r requirements.txt  # Install
COPY . .                       # Copy application
USER kaldra                    # Non-root user for security
CMD uvicorn kaldra_api.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

### render.yaml Breakdown

```yaml
services:
  - type: web                  # Web service
    name: kaldra-api          # Service name
    runtime: docker           # Use Dockerfile
    region: oregon            # Deployment region
    plan: starter             # Free tier
    healthCheckPath: /health  # Health endpoint
    autoDeploy: true          # Auto-deploy on push
```

---

## 📊 Monitoring

### Logs

View real-time logs in Render dashboard:
- **Build logs**: Docker build process
- **Deploy logs**: Application startup
- **Runtime logs**: API requests, errors

### Metrics

Render provides:
- CPU usage
- Memory usage
- Request count
- Response times

### Alerts

Set up alerts for:
- Health check failures
- High error rates
- Memory/CPU spikes

---

## 🐛 Troubleshooting

### Issue: CORS Error

**Symptom**: Frontend can't connect, CORS error in browser console

**Solution**:
1. Add frontend URL to `FRONTEND_URL` environment variable
2. Redeploy service
3. Verify CORS origins in logs

**Check**:
```python
# In kaldra_api/main.py
origins = [
    "http://localhost:3000",
    "https://4iam-frontend.vercel.app",
    os.getenv("FRONTEND_URL")  # Your custom URL
]
```

---

### Issue: Port Binding Error

**Symptom**: `Address already in use` or `Failed to bind to port`

**Solution**:
- Render sets `$PORT` dynamically
- Ensure Dockerfile uses: `--port ${PORT:-8000}`
- Never hardcode port in Python code

**Verify**:
```bash
# In Dockerfile CMD
CMD uvicorn kaldra_api.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

---

### Issue: Slow News API Responses

**Symptom**: `/kaldra/news` endpoint times out or is very slow

**Causes**:
- External API rate limits
- Network latency
- Free tier quotas exhausted

**Solutions**:
1. **Implement caching**:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def fetch_news(query: str):
       # Cache results for 5 minutes
   ```

2. **Use async requests**:
   ```python
   import asyncio
   import httpx
   
   async def fetch_all_sources():
       async with httpx.AsyncClient() as client:
           tasks = [fetch_mediastack(), fetch_gnews()]
           return await asyncio.gather(*tasks)
   ```

3. **Monitor API quotas**:
   - MediaStack: 500 req/month (free)
   - GNews: Check your plan limits

---

### Issue: Build Fails

**Symptom**: Docker build fails during `pip install`

**Common Causes**:
1. **PyTorch too large**: Use CPU-only version
   ```txt
   # In requirements.txt
   torch==2.9.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
   ```

2. **Out of memory**: Upgrade to Standard plan

3. **Missing system dependencies**:
   ```dockerfile
   # In Dockerfile
   RUN apt-get update && apt-get install -y \
       build-essential \
       libgomp1
   ```

---

### Issue: Health Check Failing

**Symptom**: Service keeps restarting, health check fails

**Debug**:
1. Check logs for startup errors
2. Verify `/health` endpoint works locally
3. Increase health check timeout in `render.yaml`:
   ```yaml
   healthCheckPath: /health
   healthCheckTimeout: 30  # seconds
   ```

---

## 🔐 Security Best Practices

### Environment Variables

✅ **DO**:
- Store all secrets in Render environment variables
- Use Render's "Secret File" feature for `.env` files
- Rotate API keys regularly

❌ **DON'T**:
- Commit `.env.local` to Git
- Hardcode API keys in code
- Share environment variables publicly

### CORS Configuration

✅ **DO**:
- Whitelist specific origins
- Use environment variables for dynamic origins
- Enable credentials only when needed

❌ **DON'T**:
- Use `allow_origins=["*"]` in production
- Allow all methods/headers unnecessarily

### Docker Security

✅ **DO**:
- Run as non-root user (`USER kaldra`)
- Use official Python slim images
- Keep dependencies updated

❌ **DON'T**:
- Run as root in production
- Use `latest` tags (pin versions)

---

## 📈 Performance Optimization

### 1. Enable Caching

**Redis** (requires paid plan):
```python
from redis import Redis
cache = Redis(host='redis-url', port=6379)

@app.get("/kaldra/news")
def get_news(query: str):
    cached = cache.get(f"news:{query}")
    if cached:
        return json.loads(cached)
    # ... fetch and cache
```

### 2. Use Async Endpoints

```python
@app.post("/engine/kaldra/signal")
async def generate_signal(payload: KaldraSignalRequest):
    # Async processing
    result = await process_async(payload.text)
    return result
```

### 3. Increase Workers

```yaml
# In render.yaml
envVars:
  - key: WEB_CONCURRENCY
    value: "4"  # Increase for Standard/Pro plans
```

---

## 🔄 CI/CD Pipeline

### Auto-Deploy on Push

Render automatically deploys when you push to `main`:

```bash
git add .
git commit -m "Update KALDRA engine"
git push origin main
# Render auto-deploys ✅
```

### Manual Deploy

In Render dashboard:
1. Go to service
2. Click "Manual Deploy"
3. Select branch/commit
4. Click "Deploy"

---

## 📞 Support

### Render Support

- **Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

### KALDRA Issues

- Check logs in Render dashboard
- Review [API_GATEWAY_WALKTHROUGH.md](./API_GATEWAY_WALKTHROUGH.md)
- Contact 4IAM.AI support

---

## 🎯 Next Steps

After successful deployment:

1. **Update Frontend**:
   ```bash
   # In 4iam_frontend/.env.local
   NEXT_PUBLIC_KALDRA_API_URL=https://kaldra-api.onrender.com
   NEXT_PUBLIC_KALDRA_API_MODE=real
   ```

2. **Deploy Frontend** to Vercel

3. **Monitor Performance**:
   - Set up alerts
   - Track API usage
   - Monitor error rates

4. **Optimize**:
   - Add caching
   - Implement rate limiting
   - Upgrade plan if needed

---

**Deployment Checklist**:
- [ ] Repository pushed to GitHub
- [ ] Render service created
- [ ] Environment variables configured
- [ ] Health check passing
- [ ] All endpoints tested
- [ ] Frontend connected
- [ ] Monitoring enabled

---

**Maintained by**: 4IAM.AI Engineering Team  
**Last Review**: 2025-11-23
