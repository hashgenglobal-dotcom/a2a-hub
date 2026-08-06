# Sprint 1.5 — MVP Release Hardening

**Goal:** Production-readiness pass before public deployment.  
**Status:** Complete (code/docs). Cloud deploy remains a manual follow-up.  
**Does not include:** Phase 2 features (trust, embeddings, auth, federation, Postgres, workers).

---

## Tasks

### 1 — README release update

- [x] What A2A Hub is, problem, architecture, MVP capabilities
- [x] Quick start, CLI, API examples, UI example, roadmap, Docker

### 2 — Docker support

- [x] `Dockerfile` (Python 3.12-slim / 3.11+ compatible package)
- [x] `.dockerignore`
- [x] Documented `docker build` / `docker run`

### 3 — Production configuration

- [x] `config.py` env vars + safe defaults
- [x] `.env.example`

### 4 — Health endpoint

- [x] `GET /health` → status, database, resources, version

### 5 — Logging verification

- [x] Startup / crawl / validation warning paths
- [x] Policy: no raw bodies / secrets in logs (`docs/implementation/LOGGING.md`)

### 6 — Release checklist

- [x] Root [`RELEASE.md`](../../RELEASE.md)

### 7 — Final test pass

- [x] `pytest -q` (run in CI / before tag)

---

## Deployment recommendation (not executed here)

```
Internet → FastAPI (API + Jinja UI) → SQLite volume
```

Railway / Render / Fly.io. **Keep SQLite.** Do not move to Postgres yet.
