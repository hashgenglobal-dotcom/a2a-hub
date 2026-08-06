# A2A Hub Public Demo

**Live:** [https://gallant-manifestation-production-d238.up.railway.app](https://gallant-manifestation-production-d238.up.railway.app)

A live instance of the A2A Hub v0.1.0 Discovery MVP, deployed on Railway.

---

## Try It

```bash
# Health check
curl -s https://gallant-manifestation-production-d238.up.railway.app/health

# Search for agents
curl -s "https://gallant-manifestation-production-d238.up.railway.app/search?q=resume"

# Web UI
open https://gallant-manifestation-production-d238.up.railway.app
```

---

## Current Limitations

This is a **live experiment**, not a production service.

| Limitation | Reason |
|-----------|--------|
| **Demo dataset only** | 2 sample Agent Cards. No real agents indexed yet. |
| **Manual crawling** | Crawl runs once on first boot. No continuous discovery. |
| **No authentication** | Public read-only API. Anyone can query. |
| **SQLite storage** | Single file. No replication. No backups. |
| **No rate limiting** | No abuse protection. |
| **No custom domain** | Railway-generated URL. |

---

## What Works

- Agent Card crawling (async HTTP + local file fixtures)
- A2A schema validation and normalization
- Resource registry (SQLite, deduplicated)
- Keyword search API (`GET /search`, `GET /resources/{id}`, `GET /health`)
- Minimal web UI (Jinja2 templates)
- Docker image

---

## What's Next

The demo exists to validate whether developers need a neutral agent discovery layer. Feedback drives the roadmap:

- **Phase 2:** Trust signals, health monitoring, identity verification
- **Phase 3:** Federation, cross-registry discovery
- **Phase 4:** Universal Agent Control Plane

See [`docs/strategy/VISION.md`](../strategy/VISION.md) for the full roadmap.

---

## Deploy Your Own

```bash
git clone https://github.com/hashgenglobal-dotcom/a2a-hub.git
cd a2a-hub
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m a2a_hub crawl
python -m a2a_hub serve
```

Or use Docker:

```bash
docker build -t a2a-hub:0.1.0 .
docker run --rm -p 8000:8000 -v a2a-hub-data:/app/data a2a-hub:0.1.0
```
