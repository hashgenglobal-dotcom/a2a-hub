# A2A Hub — Backlog

---

## Priority Definitions

| Priority | Definition | When |
|----------|------------|------|
| P0 | MVP — must ship for public launch | Week 1-2 |
| P1 | Week 3 polish | Week 3 |
| P2 | Phase 2 — trust & intelligence | Post-MVP |
| P3 | Phase 3 — platform & enterprise | Post-MVP |

---

## P0 — MVP (Weeks 1-2)

### P0.0 — Platform Foundation

**Tasks:**
- [ ] Project setup (pyproject.toml, layout, __init__.py files)
- [ ] Configuration loader (pydantic-settings)
- [ ] FastAPI app factory + CLI entry point
- [ ] SQLite initialization with migration
- [ ] Structured logging
- [ ] Testing framework (pytest, pytest-asyncio)

### P0.1 — Seed Discovery & Fetch

**Tasks:**
- [ ] Hardcoded seed URLs from A2A partner list + known domains
- [ ] URL queue with deduplication (SQLite)
- [ ] HTTP fetcher using aiohttp
- [ ] Store raw JSON in crawl_results table
- [ ] Mark URLs as fetched/failed

### P0.2 — Parse & Validate

**Tasks:**
- [ ] pydantic models: Resource, CrawlTarget, CrawlResult
- [ ] A2A v1.0 schema validation
- [ ] Error reporting for invalid cards
- [ ] `urn:air:` identifier generation
- [ ] A2A adapter: Agent Card → Resource

### P0.3 — Store & Index

**Tasks:**
- [ ] SQLite schema: resources, crawl_jobs, crawl_results
- [ ] Insert/update/dedup for resources
- [ ] Keyword search over name + description + skills
- [ ] Simple pagination (offset/limit)

### P0.4 — Search API

**Tasks:**
- [ ] `GET /search?q=...&limit=...&offset=...`
- [ ] `GET /resources/{id}`
- [ ] `GET /health`
- [ ] Standardized JSON error responses

### P0.5 — Minimal Web UI

**Tasks:**
- [ ] Search page (HTML form → GET /search)
- [ ] Resource detail page
- [ ] Jinja2 templates served by FastAPI

### P0.6 — Public Deployment

**Tasks:**
- [ ] Deploy on Railway / Fly.io / Render
- [ ] Persistent SQLite storage
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Deployment documentation

---

## P1 — Week 3 Polish

### P1.1 — Continuous Crawl

**Tasks:**
- [ ] TTL-based re-crawl scheduler
- [ ] Staleness detection
- [ ] Discovered URL follow-up

### P1.2 — Health Checks

**Tasks:**
- [ ] Periodic HEAD/GET to resource endpoints
- [ ] Store health results
- [ ] Expose health status in API and UI

### P1.3 — CLI Tool

**Tasks:**
- [ ] `a2a-hub search <query>`
- [ ] `a2a-hub resource <id>`
- [ ] `a2a-hub health`

### P1.4 — Error Handling & Monitoring

**Tasks:**
- [ ] Error categorization
- [ ] Crawl failure tracking
- [ ] Basic metrics endpoint

---

## P2 — Phase 2: Trust & Intelligence

### P2.1 — Semantic Search

**Tasks:**
- [ ] Integrate sentence-transformers (all-MiniLM-L6-v2)
- [ ] Generate embeddings for all resources
- [ ] Vector similarity search
- [ ] Hybrid search (keyword + semantic)

### P2.2 — ARDS Compliance

**Tasks:**
- [ ] `POST /search` with ARDS query model
- [ ] `POST /explore` (facet aggregation)
- [ ] `GET /resources` (list/browse)
- [ ] Trust manifest support
- [ ] Pass ARDS conformance test suite

### P2.3 — Rich Resource Profiles

**Tasks:**
- [ ] Resource profile page design
- [ ] Trust score, health, uptime, latency display
- [ ] Version history and changelog
- [ ] Compatibility badges

### P2.4 — Identity Verification

**Tasks:**
- [ ] Resource Card signature verification
- [ ] Domain ownership verification
- [ ] Trust score calculation

### P2.5 — OAuth Broker

**Tasks:**
- [ ] OAuth2 authorization server
- [ ] Token issuance and validation
- [ ] Resource identity binding

---

## P3 — Phase 3: Platform & Enterprise

### P3.1 — Reputation System

**Tasks:**
- [ ] Task completion tracking
- [ ] Peer review system
- [ ] Composite trust score
- [ ] Trust score decay

### P3.2 — Federation Protocol

**Tasks:**
- [ ] Auto federation mode
- [ ] Referrals federation mode
- [ ] Federation handshake

### P3.3 — Enterprise Dashboard

**Tasks:**
- [ ] Resource inventory view
- [ ] Health overview
- [ ] Compliance reporting
- [ ] Policy management

### P3.4 — Platform Adapters

**Tasks:**
- [ ] Google Agent Registry adapter
- [ ] Salesforce AgentExchange adapter
- [ ] MCP registry adapter
