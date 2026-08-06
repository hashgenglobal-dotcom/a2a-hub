# Changelog

## 0.1.0 — 2026-08-06

A2A Hub MVP release candidate (pre-public-deploy hardening).

### Features

- Seed discovery via `config/seeds.json` (local `file:` fixtures + optional public URLs)
- Async Agent Card crawl → raw `crawl_results` storage
- Tolerant validation / normalization into canonical `Resource` records
- Keyword Search API: `GET /search`, `GET /resources/{id}`, enriched `GET /health`
- Minimal Jinja2 discovery UI at `GET /`
- Structured JSON logging (stdlib)
- Docker image for repeatable runs (`Dockerfile`)

### Docs

- README: install, crawl, serve, configuration, API examples, Docker, deploy guidance
- Sprint 1.5 hardening notes and GitHub release draft

### Explicitly deferred

- Live deploy to Railway / Render / Fly.io
- PostgreSQL / pgvector
- Auth, rate limits, registration, semantic search, trust scoring
