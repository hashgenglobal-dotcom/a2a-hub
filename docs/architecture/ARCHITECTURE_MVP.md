# A2A Hub — MVP Architecture

**This document describes the MVP architecture only.**

For the target architecture, see `ARCHITECTURE_TARGET.md`.

---

## Overview

```
┌─────────────────────────────────────────────┐
│           Single Process (FastAPI)           │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Crawler  │→ │ Parser   │→ │ Store    │  │
│  │ (aiohttp)│  │(pydantic)│  │ (SQLite) │  │
│  └──────────┘  └──────────┘  └────┬─────┘  │
│                                    │        │
│  ┌──────────┐  ┌──────────┐       │        │
│  │ Web UI   │← │ API      │←──────┘        │
│  │ (HTML)   │  │(FastAPI) │                │
│  └──────────┘  └──────────┘                │
└─────────────────────────────────────────────┘
```

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Single process | No background workers, no Redis, no Celery, no Kafka. Crawl runs on startup or via CLI. |
| SQLite | Single file, zero infrastructure, sufficient for thousands of resources. |
| No auth | Public read-only API. Auth adds complexity without validated need. |
| No rate limiting | Premature optimization. Add when abuse is observed. |
| No embeddings | Keyword search only. Semantic search is Phase 2. |
| No health checks | Phase 2. |
| No event system | Phase 2. |

## Data Flow

```
1. Startup: Load seed URLs → queue in crawl_jobs table
2. Crawl: Fetch each URL → store raw JSON in crawl_results
3. Parse: Validate against A2A v1.0 schema → extract fields
4. Normalize: Convert to Resource model
5. Store: Insert/update resources table
6. Search: API queries resources table via SQL LIKE
7. Present: Web UI renders search results and resource details
```

## Project Layout

```
src/a2a_hub/
├── __init__.py
├── config.py          # Settings via pydantic-settings
├── main.py            # FastAPI app, startup, CLI entry point
├── models/
│   ├── __init__.py
│   └── resource.py    # Resource, CrawlTarget, CrawlResult
├── crawler/
│   ├── __init__.py
│   └── fetcher.py     # aiohttp-based HTTP fetcher
├── parser/
│   ├── __init__.py
│   └── validator.py   # A2A v1.0 schema validation + normalization
├── store/
│   ├── __init__.py
│   └── database.py    # SQLite CRUD, search, migration
├── api/
│   ├── __init__.py
│   └── routes.py      # FastAPI routes: /search, /resources/{id}, /health
└── ui/
    ├── __init__.py
    └── templates/     # Jinja2 HTML templates
        ├── search.html
        └── resource.html
```

## Replaceability

Every subsystem is designed to be replaceable:

| Subsystem | Can be replaced by | When |
|-----------|-------------------|------|
| Crawler (aiohttp) | Any HTTP client | Any time |
| Parser (pydantic) | Any validation library | Any time |
| Store (SQLite) | PostgreSQL, any DB | Phase 2 |
| Search (LIKE) | Full-text search, vector search | Phase 2 |
| UI (Jinja2) | React, Vue, any framework | Phase 2 |
| Protocol adapter (A2A) | MCP, ARDS, any protocol | Phase 2 |

No layer depends on the implementation details of another layer.
