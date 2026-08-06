# A2A Hub — MVP Specification

**This is the implementation contract. All implementation follows this document.**

For the product vision, see `docs/strategy/VISION.md`.
For the architecture, see `docs/architecture/ARCHITECTURE_MVP.md`.
For the domain model, see `docs/architecture/DOMAIN_MODEL_MVP.md`.

---

## Pipeline

Every commit moves a resource one step further through:

```
Discover → Fetch → Validate → Normalize → Store → Search → Present
```

If a proposed feature does not strengthen this pipeline, it waits.

---

## 7 MVP Capabilities

| # | Capability | Description |
|---|-----------|-------------|
| 1 | **Seed Discovery** | Hardcoded seed URLs from A2A partner list + known domains. No GitHub crawler. No registration. No search engines. |
| 2 | **Crawl** | HTTP fetch raw Resource Cards via aiohttp. Store raw payload in SQLite. |
| 3 | **Parse & Validate** | Validate against A2A v1.0 schema via pydantic. Reject invalid cards with clear errors. |
| 4 | **Normalize & Store** | Convert validated cards into the Resource model. Persist to SQLite with dedup. Enable keyword search. |
| 5 | **Search API** | `GET /search`, `GET /resources/{id}`, `GET /health`. No auth. No rate limiting. |
| 6 | **Minimal Web UI** | Search page + resource detail page. Static HTML served by FastAPI via Jinja2 templates. |
| 7 | **Public Deployment** | Deployed on Railway/Fly.io/Render. CI/CD via GitHub Actions. Public access. |

---

## API Contract

### Search Resources

```
GET /search?q=<query>&limit=<int>&offset=<int>

Response 200:
{
  "resources": [
    {
      "id": "urn:air:example:agents:my-agent",
      "name": "My Agent",
      "description": "Does something useful",
      "url": "https://api.example.com/a2a",
      "provider": { "organization": "Example Corp" },
      "skills": ["skill-1", "skill-2"],
      "resource_type": "a2a-agent"
    }
  ],
  "total": 1
}
```

### Get Resource

```
GET /resources/{id}

Response 200:
{
  "id": "urn:air:example:agents:my-agent",
  "name": "My Agent",
  "description": "Does something useful",
  "url": "https://api.example.com/a2a",
  "provider": { "organization": "Example Corp" },
  "capabilities": { "streaming": true },
  "skills": [{ "id": "skill-1", "name": "Skill 1", "description": "..." }],
  "auth": { "schemes": [{ "type": "apiKey", "in": "header", "name": "X-API-Key" }] },
  "raw_json": { ... },
  "resource_type": "a2a-agent",
  "created_at": "2026-08-06T10:00:00Z",
  "updated_at": "2026-08-06T10:00:00Z"
}
```

### Health Check

```
GET /health

Response 200:
{
  "status": "ok",
  "resources_count": 42,
  "uptime_seconds": 3600
}
```

---

## Data Model

See `docs/architecture/DOMAIN_MODEL_MVP.md` for the complete data model.

Three SQLite tables: `resources`, `crawl_jobs`, `crawl_results`.

One canonical entity: `Resource`.

---

## Protocol Adapter Pattern

```
Raw JSON (A2A Agent Card)
    ↓
A2A Adapter (protocol-specific parsing + validation)
    ↓
Resource (platform-agnostic canonical entity)
    ↓
SQLite
```

The A2A adapter is the only protocol adapter in MVP. It converts A2A Agent Card JSON into the Resource model. Future protocols get their own adapters. The Resource model never changes.

---

## Architecture

See `docs/architecture/ARCHITECTURE_MVP.md` for the complete architecture.

- Single process. No background workers. No Redis. No Celery. No Kafka.
- Crawl runs on startup or via CLI. No scheduler. No continuous loop.
- SQLite. Single file. Zero infrastructure.
- No auth. Public read-only API.
- No rate limiting.
- No embeddings. Keyword search only.
- No health checks.
- No event system.

---

## Success Criteria

The MVP is complete when:

- [ ] Crawl one or more seed sources
- [ ] Parse valid Resource Cards
- [ ] Store normalized resources
- [ ] Search resources by keyword
- [ ] View resource details
- [ ] Minimal web UI for browsing
- [ ] Deployed publicly
- [ ] Re-run crawl without duplicates

---

## Explicitly Not in MVP

| Feature | Phase |
|---------|-------|
| GitHub API crawler | Removed |
| robots.txt compliance | Removed |
| Rate limiting | Removed |
| Retry policies | Removed |
| Concurrency tuning | Removed |
| `POST /register` endpoint | Removed |
| OpenAPI spec generation | FastAPI auto-generates |
| pageToken pagination | Removed |
| Custom domain | Removed |
| 99.5% uptime target | Removed |
| Grafana / alerting | Removed |
| OAuth / authentication | Phase 2+ |
| Organizations table | Phase 2+ |
| Skills table | Phase 2+ |
| TTL tracking | Phase 2+ |
| Semantic / vector search | Phase 2 |
| Continuous health monitoring | Phase 2 |
| Identity verification | Phase 2 |
| Rich resource profiles / UI | Phase 2 |
| Federation | Phase 3 |
| Enterprise features | Phase 3 |
| Reputation system | Phase 3 |
| OAuth broker | Phase 3 |
