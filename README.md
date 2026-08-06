# A2A Hub

**The trust infrastructure / discovery layer for the open Agent Internet.**

**Version:** `0.1.0` (MVP)  
**License:** Apache 2.0

A2A Hub is an open-source registry that helps developers and systems **find** A2A-compatible AI agents. It crawls Agent Cards, validates and normalizes them into canonical **Resources**, and exposes keyword search via API and a minimal web UI.

> Long-term vision: Universal Agent Control Plane (discovery → trust → federation). See [`docs/strategy/VISION.md`](docs/strategy/VISION.md).  
> **Build contract:** [`docs/implementation/BUILD_SPEC.md`](docs/implementation/BUILD_SPEC.md) wins all implementation conflicts.

---

## The Problem

The A2A protocol defines *how* agents communicate (tasks, messages, auth) via Agent Cards at `/.well-known/agent.json`. It does **not** define *how agents find each other*.

Without a shared index:

- Every integration requires a hand-copied URL
- There is no cross-owner discovery layer
- Trust and reputation have nowhere to attach later

A2A Hub fills the **discovery** gap first — a neutral layer between growing numbers of agents and the people/systems trying to find them.

---

## Architecture (MVP)

```
Seeds (config/seeds.json)
        │
        ▼
   Crawl (aiohttp / file:)
        │
        ▼
  crawl_results (raw HTTP)
        │
        ▼
 RawAgentCard (immutable)
        │
        ▼
 Validator → Normalizer
        │
        ▼
   Resource (SQLite)
        │
   ┌────┴────┐
   ▼         ▼
 JSON API   Jinja UI
```

Single process. SQLite file. No Postgres, Redis, background workers, or auth in v0.1.0.

---

## MVP Capabilities

| Capability | Status |
|------------|--------|
| Seed discovery (`config/seeds.json` + local fixtures) | Done |
| Async Agent Card crawl | Done |
| Tolerant validate + normalize → Resource | Done |
| Keyword Search API | Done |
| Minimal Jinja2 discovery UI | Done |
| Docker image | Done |
| Public cloud deploy | Manual next step |

**Not in v0.1.0:** trust scoring, embeddings, authentication, federation, Postgres, background workers.

---

## Quick Start

Requires **Python 3.11+**.

```bash
git clone https://github.com/hashgenglobal-dotcom/a2a-hub.git
cd a2a-hub
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env        # optional
python -m a2a_hub crawl
python -m a2a_hub serve
```

Open http://localhost:8000/

---

## CLI Commands

```bash
# Index seed Agent Cards into SQLite
python -m a2a_hub crawl

# Serve JSON API + HTML UI (does not crawl on startup)
python -m a2a_hub serve

# List configured seed URLs
python scripts/seed_urls.py

# Tests
pytest -q
```

---

## Configuration

Copy [`.env.example`](.env.example). All settings use the `A2A_HUB_` prefix:

| Variable | Default | Meaning |
|----------|---------|---------|
| `A2A_HUB_APP_NAME` | `a2a-hub` | Application name |
| `A2A_HUB_DATABASE_PATH` | `data/a2a_hub.db` | SQLite path |
| `A2A_HUB_SEEDS_PATH` | `config/seeds.json` | Seed URL config |
| `A2A_HUB_CRAWLER_TIMEOUT_SECONDS` | `30` | HTTP timeout |
| `A2A_HUB_LOG_LEVEL` | `INFO` | Log level |
| `A2A_HUB_HOST` | `0.0.0.0` | Bind host |
| `A2A_HUB_PORT` | `8000` | Bind port |

Logs are **JSON lines on stdout**. Crawl logs include URL/status/error codes — not raw response bodies or secrets.

---

## API Examples

```bash
# Health
curl -s http://localhost:8000/health
# → {"status":"ok","database":"connected","resources":2,"version":"0.1.0"}

# Search
curl -s 'http://localhost:8000/search?q=resume&limit=10'

# Resource detail (encode the URN)
curl -s --get "http://localhost:8000/resources/urn:air:unverified:..." \
  --data-urlencode ""
```

OpenAPI: http://localhost:8000/docs

---

## UI Example

1. Run crawl + serve  
2. Open http://localhost:8000/  
3. Search e.g. `resume` or `echo`  
4. Click a result for detail (name, description, endpoint, skills, publisher, id)

Browsers receive HTML for `/resources/{id}`; API clients requesting `application/json` still get JSON.

---

## Docker

```bash
docker build -t a2a-hub:0.1.0 .
docker run --rm -p 8000:8000 -v a2a-hub-data:/app/data a2a-hub:0.1.0
```

One-shot crawl (same volume):

```bash
docker run --rm -v a2a-hub-data:/app/data a2a-hub:0.1.0 python -m a2a_hub crawl
```

---

## First Public Demo (recommended)

```
Internet → FastAPI (API + Jinja UI) → SQLite volume
```

Use **Railway / Render / Fly.io**. Keep **SQLite** for the first demo — do not move to Postgres yet. Crawl via one-shot CLI, not on server boot.

Release checklist: [`RELEASE.md`](RELEASE.md)

---

## Roadmap

| Phase | Focus |
|-------|--------|
| **MVP** | Discovery (this release) |
| **Phase 2** | Trust (verification, health, reputation signals) |
| **Phase 3** | Federation (cross-registry) |
| **Phase 4** | Agent Internet Control Plane |

Backlog: [`docs/implementation/BACKLOG.md`](docs/implementation/BACKLOG.md)

---

## Repository Governance

| Priority | Document |
|----------|----------|
| 1 (wins) | [`BUILD_SPEC.md`](docs/implementation/BUILD_SPEC.md) |
| 2 | Sprint plans / [`SPRINT_1_5.md`](docs/implementation/SPRINT_1_5.md) |
| 3 | [`BACKLOG.md`](docs/implementation/BACKLOG.md) |
| 4+ | Architecture, ADRs, Vision |

---

## License

Apache 2.0. See [LICENSE](LICENSE).
