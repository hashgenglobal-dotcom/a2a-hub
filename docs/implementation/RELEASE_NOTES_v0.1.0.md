# A2A Hub MVP — v0.1.0

**Release title:** A2A Hub MVP

## Features

- Agent discovery (configurable seed list + local fixtures)
- A2A Agent Card crawling (async HTTP / `file:` fixtures)
- Resource registry (canonical `Resource` entity, immutable `RawAgentCard`)
- Tolerant validation + normalization + upsert
- Keyword Search API (`GET /search`, `GET /resources/{id}`, `GET /health`)
- Minimal Jinja2 web interface (`GET /`)

## Not in v0.1.0

- Public cloud deployment (recommended next: Railway / Render / Fly.io + SQLite volume)
- Semantic search / embeddings
- Auth, rate limiting, registration
- Trust scoring / reputation
- Postgres

## Quick verify

```bash
pip install -e ".[dev]"
pytest -q
python -m a2a_hub crawl
python -m a2a_hub serve
curl -s http://localhost:8000/health
```

## Docker

```bash
docker build -t a2a-hub:0.1.0 .
docker run --rm -p 8000:8000 -v a2a-hub-data:/app/data a2a-hub:0.1.0
```
