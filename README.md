# A2A Hub

**The Universal Agent Control Plane.**

**Mission:** Make every AI resource discoverable, trustworthy, observable, and interoperable across the open Agent Internet.

**Status:** MVP (`v0.1.0`) — discovery pipeline + search API + minimal web UI. Public deployment is the next step (SQLite volume on Railway / Render / Fly.io).

---

## Repository Governance

This repository intentionally separates long-term vision from the current implementation.

**Only one document defines what engineers build:**

[`docs/implementation/BUILD_SPEC.md`](docs/implementation/BUILD_SPEC.md)

Everything else exists for context.

### Priority Order

1. `docs/implementation/BUILD_SPEC.md` — **Implementation source of truth. Wins all conflicts.**
2. `docs/implementation/SPRINT_XX.md` — Current sprint plan.
3. `docs/implementation/BACKLOG.md` — Prioritized backlog.
4. `docs/architecture/ARCHITECTURE_MVP.md` — Current architecture.
5. `docs/architecture/DOMAIN_MODEL_MVP.md` — Current domain model.
6. `docs/architecture/ENGINEERING_PRINCIPLES.md` — Engineering standards.
7. `docs/strategy/VISION.md` — Long-term product vision.

If any document conflicts with `BUILD_SPEC.md`, `BUILD_SPEC.md` always wins.

Target architecture documents (`ARCHITECTURE_TARGET.md`, `DOMAIN_MODEL_TARGET.md`) never define current implementation. They exist for planning only.

---

## What This Is

A2A Hub is an open-source infrastructure project. It provides a unified control plane for discovering, verifying, monitoring, and governing AI resources across any platform, protocol, or organization.

This repository contains the MVP: a crawler, search index, API, and minimal web UI for discovering A2A-compatible AI agents.

For the full product vision, see [`docs/strategy/VISION.md`](docs/strategy/VISION.md).

---

## Install

Requires **Python 3.11+**.

```bash
git clone https://github.com/hashgenglobal-dotcom/a2a-hub.git
cd a2a-hub
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

---

## Crawl

Fetch configured seed Agent Cards, validate, normalize, and upsert Resources into SQLite:

```bash
python -m a2a_hub crawl
```

Default seeds are local fixtures under `samples/agent_cards/` (via `config/seeds.json`). Enable public URLs in that file when ready (`public_seeds[].enabled`).

List configured seeds:

```bash
python scripts/seed_urls.py
```

---

## Serve

Start the API + Jinja2 UI (crawl does **not** run on startup):

```bash
python -m a2a_hub serve
```

Open http://localhost:8000/

- HTML search: `/`
- JSON search: `/search?q=resume`
- Health: `/health`
- OpenAPI docs: `/docs`

---

## Configuration

All settings use the `A2A_HUB_` prefix (optional `.env` file):

| Variable | Default | Meaning |
|----------|---------|---------|
| `A2A_HUB_DATABASE_PATH` | `data/a2a_hub.db` | SQLite file path |
| `A2A_HUB_SEEDS_PATH` | `config/seeds.json` | Seed URL configuration |
| `A2A_HUB_CRAWLER_TIMEOUT_SECONDS` | `30` | HTTP fetch timeout |
| `A2A_HUB_LOG_LEVEL` | `INFO` | Logging level |
| `A2A_HUB_HOST` | `0.0.0.0` | Bind host |
| `A2A_HUB_PORT` | `8000` | Bind port |
| `A2A_HUB_APP_NAME` | `a2a-hub` | Application name |

Logs are JSON lines on stdout (timestamp, level, logger, message, optional `fields`).

---

## API Examples

```bash
# Health
curl -s http://localhost:8000/health

# Keyword search
curl -s 'http://localhost:8000/search?q=resume&limit=10'

# Resource detail (URL-encode the URN id)
curl -s "http://localhost:8000/resources/$(python -c 'import urllib.parse; print(urllib.parse.quote("urn:air:unverified:...", safe=""))')"
```

Example health payload:

```json
{
  "status": "ok",
  "database": "connected",
  "resources": 2,
  "version": "0.1.0"
}
```

---

## Docker

```bash
docker build -t a2a-hub:0.1.0 .
docker run --rm -p 8000:8000 -v a2a-hub-data:/app/data a2a-hub:0.1.0
```

One-shot crawl inside the container (same volume):

```bash
docker run --rm -v a2a-hub-data:/app/data a2a-hub:0.1.0 python -m a2a_hub crawl
```

**First public demo recommendation:** Railway / Render / Fly.io with a single FastAPI process and a **persistent SQLite volume**. Do not move to Postgres for the MVP demo.

```
Internet → FastAPI (API + Jinja UI) → SQLite volume
```

---

## Repository Map

| Path | Purpose |
|------|---------|
| [`docs/implementation/BUILD_SPEC.md`](docs/implementation/BUILD_SPEC.md) | **Start here.** Implementation contract for the MVP. |
| [`docs/implementation/SPRINT_01.md`](docs/implementation/SPRINT_01.md) | Sprint 1 day plan. |
| [`docs/implementation/SPRINT_1_5.md`](docs/implementation/SPRINT_1_5.md) | MVP release hardening (pre-deploy). |
| [`docs/implementation/RELEASE_NOTES_v0.1.0.md`](docs/implementation/RELEASE_NOTES_v0.1.0.md) | GitHub release notes draft. |
| [`docs/architecture/ARCHITECTURE_MVP.md`](docs/architecture/ARCHITECTURE_MVP.md) | Current architecture (single process, SQLite). |
| [`docs/adr/`](docs/adr/) | Architecture Decision Records. |
| [`config/seeds.json`](config/seeds.json) | Seed Agent Card URLs. |
| [`Dockerfile`](Dockerfile) | Repeatable container image. |

---

## License

Apache 2.0. See [LICENSE](LICENSE).
