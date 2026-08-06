# A2A Hub — Demo Deployment

**Status:** Configuration ready — deployment pending
**Date:** August 6, 2026

---

## Platform Evaluation

| Criteria | Railway | Render | Fly.io |
|----------|---------|--------|--------|
| Python FastAPI support | ✅ Native | ✅ Native | ✅ Native |
| Persistent SQLite volume | ✅ Volumes | ✅ Disks | ✅ Volumes |
| Free tier | ✅ $5 credit/month | ✅ Free tier | ✅ Free tier |
| One-click deploy from GitHub | ✅ | ✅ | ✅ |
| Custom domain | ✅ | ✅ | ✅ |
| Ease of setup | ★★★★★ | ★★★★☆ | ★★★☆☆ |

**Recommendation: Railway**

Railway is the simplest option for this deployment:
- Native Python/FastAPI support with automatic `uvicorn` detection
- Persistent volumes for SQLite (`/app/data`)
- One-click deploy from GitHub
- Generous free tier ($5 credit/month — enough for a demo)
- No YAML configuration needed for basic deployment
- Automatic HTTPS

---

## Deployment Configuration

### Environment Variables

Set these in Railway dashboard:

| Variable | Value | Purpose |
|----------|-------|---------|
| `A2A_HUB_DATABASE_PATH` | `/app/data/a2a_hub.db` | Persistent SQLite path |
| `A2A_HUB_HOST` | `0.0.0.0` | Bind all interfaces |
| `A2A_HUB_PORT` | `8000` | HTTP port |
| `A2A_HUB_LOG_LEVEL` | `INFO` | Log level |
| `A2A_HUB_CRAWLER_TIMEOUT_SECONDS` | `30` | Crawl timeout |

### Start Command

```
python -m a2a_hub serve
```

### Persistent Volume

Mount a volume at `/app/data` to preserve the SQLite database across restarts.

### One-Time Crawl

After deployment, run once:

```
python -m a2a_hub crawl
```

This populates the database with sample agents. The data persists in the volume.

---

## Deployment Steps

### Option A: Railway (Recommended)

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `hashgenglobal-dotcom/a2a-hub`
5. Railway auto-detects Python and sets the start command
6. Add environment variables (see table above)
7. Add a volume at `/app/data`
8. Deploy
9. Open the generated URL
10. Run one-time crawl via Railway's "Shell" tab:
   ```
   python -m a2a_hub crawl
   ```

### Option B: Render

1. Go to https://render.com
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Connect `hashgenglobal-dotcom/a2a-hub`
5. Set:
   - **Name:** `a2a-hub`
   - **Environment:** `Python`
   - **Build Command:** `pip install -e ".[dev]"`
   - **Start Command:** `python -m a2a_hub serve`
6. Add environment variables (see table above)
7. Add a Disk at `/app/data` (Render Persistent Disk)
8. Deploy
9. Run one-time crawl via Render's "Shell" tab

### Option C: Fly.io

1. Install flyctl: `curl -fsSL https://fly.io/install.sh | sh`
2. Sign in: `fly auth login`
3. Create config: `fly launch --no-deploy`
4. Edit `fly.toml` to set `[mounts] source="a2a_hub_data", destination="/app/data"`
5. Deploy: `fly deploy`
6. Run crawl: `fly ssh console -C "python -m a2a_hub crawl"`

---

## Architecture

```
Internet
    ↓
Railway HTTPS endpoint
    ↓
FastAPI (uvicorn, single process)
    ↓
SQLite (/app/data/a2a_hub.db)
    ↓
Persistent volume (survives restarts)
```

## Known Limitations

| Limitation | Impact | Resolution |
|-----------|--------|------------|
| SQLite single-writer | No concurrent writes | Acceptable for demo scale |
| No background crawl | Must run crawl manually | Phase 2 feature |
| No auth | Public read-only API | Acceptable for demo |
| No rate limiting | No abuse protection | Acceptable for demo |
| No custom domain | Railway generates URL | Can add later |

## Verification

After deployment, verify:

```bash
# Health
curl -s https://<your-url>.railway.app/health

# Search
curl -s "https://<your-url>.railway.app/search?q=resume"

# UI
open https://<your-url>.railway.app/
```

Expected health response:
```json
{
  "status": "ok",
  "database": "connected",
  "resources": 2,
  "version": "0.1.0"
}
```
