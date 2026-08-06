# A2A Hub — v0.1.0 Release Checklist

**Release:** A2A Hub MVP (`v0.1.0`)  
**Date:** 2026-08-06  
**Scope:** Discovery layer only. No Phase 2 features.

---

## Pre-release verification

| Check | Status | Notes |
|-------|--------|-------|
| `pytest -q` | ☐ | All tests green |
| Clean install `pip install -e ".[dev]"` | ☐ | From fresh venv |
| `python -m a2a_hub crawl` | ☐ | Indexes local seed fixtures |
| `python -m a2a_hub serve` | ☐ | UI at `/`, API at `/search`, `/health` |
| `curl localhost:8000/health` | ☐ | `status` / `database` / `resources` / `version` |
| Docker build | ☐ | `docker build -t a2a-hub:0.1.0 .` |
| Docker run | ☐ | `-p 8000:8000 -v …:/app/data` |
| README matches implementation | ☐ | Quick start, CLI, API, UI, Docker, roadmap |
| `.env.example` present | ☐ | Documented env vars |
| No secrets in logs | ☐ | No response bodies / auth headers in log fields |
| GitHub Release notes ready | ☐ | See also `docs/implementation/RELEASE_NOTES_v0.1.0.md` |

---

## Features in v0.1.0

- Agent discovery (seed list + local fixtures)
- A2A Agent Card crawling
- Resource registry (canonical `Resource`)
- Keyword Search API
- Minimal web interface (Jinja2)

---

## Known limitations

- Seed coverage is fixture-first; public Agent Card URLs must be enabled manually
- Keyword `LIKE` search only (no semantic / vector search)
- No authentication, rate limiting, or registration API
- No continuous crawl / background workers (CLI crawl only)
- No crawler SSRF / robots / max-body hardening for arbitrary public URLs (backlog P1.5)
- SQLite only — fine for demo; not multi-writer scale
- Docker image available; **cloud deploy is a manual follow-up**

---

## Future roadmap (not this release)

```
MVP Discovery → Phase 2 Trust → Phase 3 Federation → Phase 4 Control Plane
```

Do **not** add in v0.1.0: trust scoring, embeddings, auth, federation, Postgres, background workers.

---

## First public demo (after checklist)

```
Internet → FastAPI (API + Jinja UI) → SQLite volume
```

Platforms: Railway / Render / Fly.io. Keep SQLite. Do not move to Postgres yet.

---

## Cut release commands (maintainer)

```bash
pytest -q
git tag -a v0.1.0 -m "A2A Hub MVP v0.1.0"
git push origin v0.1.0
# Create GitHub Release from docs/implementation/RELEASE_NOTES_v0.1.0.md
```
