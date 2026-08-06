# Sprint 1.5 — MVP Release Hardening

**Goal:** Production-readiness pass before public deployment.  
**Status:** In progress  
**Does not include:** Live deploy to Railway/Render/Fly (manual follow-up).

---

## Tasks

### A — Environment documentation

- [x] README: install, crawl, serve, configuration, API examples, Docker, deploy recommendation

### B — Docker support

- [x] `Dockerfile`
- [x] `.dockerignore`

### C — Health improvement

- [x] `/health` returns `status`, `database`, `resources`, `version`

### D — Logging verification

- [x] Startup log on serve
- [x] Crawl / validation logs already emit structured JSON
- [x] Unit test for JSON log formatter

### E — GitHub release preparation

- [x] `CHANGELOG.md` for `v0.1.0`
- [x] `docs/implementation/RELEASE_NOTES_v0.1.0.md` draft for GitHub Release

---

## Deployment recommendation (not executed in this sprint)

| Item | Choice |
|------|--------|
| Platform | Railway / Render / Fly.io |
| Process | Single FastAPI (`python -m a2a_hub serve`) |
| Storage | Persistent **SQLite volume** |
| Database | **Do not** move to Postgres yet |
| Crawl | One-shot `python -m a2a_hub crawl` (CLI), not on boot |

```
Internet
   │
   ▼
FastAPI
   ├── JSON API
   ├── Jinja UI
   ▼
SQLite volume
```
