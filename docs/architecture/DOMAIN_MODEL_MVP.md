# A2A Hub — Domain Model (MVP)

**This document describes the MVP domain model only.**

For the full target domain model, see `DOMAIN_MODEL_TARGET.md`.

---

## Core Entity: Resource

The platform owns Resources. Agent Cards are parser inputs, not platform entities.

```
Raw JSON (A2A Agent Card)
    ↓
A2A Adapter (protocol-specific parsing + validation)
    ↓
Resource (platform-agnostic canonical entity)
    ↓
SQLite
```

## Resource

The canonical representation of an AI resource in the A2A Hub MVP.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | str | Unique identifier (`urn:air:` format) | `urn:air:hashgen:agents:resume-parser` |
| `name` | str | Human-readable name | `Resume Parser` |
| `description` | str or None | What the resource does | `Parses resumes and extracts structured data` |
| `url` | str | Resource endpoint URL | `https://api.hashgen.ai/a2a` |
| `provider` | dict or None | Provider metadata | `{"organization": "HashGen Global"}` |
| `skills` | list[dict] | Capabilities | `[{"id": "resume-parsing", "name": "Resume Parsing"}]` |
| `auth` | dict or None | Auth schemes | `{"schemes": [{"type": "apiKey"}]}` |
| `raw_json` | dict | Original card JSON for re-validation | `{...}` |
| `resource_type` | str | Protocol type | `a2a-agent` |
| `created_at` | datetime | When first indexed | ISO 8601 |
| `updated_at` | datetime | When last updated | ISO 8601 |

## CrawlTarget

A URL queued for crawling.

| Field | Type | Description |
|-------|------|-------------|
| `url` | str | The URL to crawl |
| `status` | str | `pending`, `crawling`, `complete`, `failed` |
| `discovered_at` | datetime | When the URL was discovered |
| `last_attempt` | datetime or None | Last crawl attempt |
| `error` | str or None | Last error message |

## CrawlResult

The result of a single crawl attempt.

| Field | Type | Description |
|-------|------|-------------|
| `crawl_job_id` | int | References CrawlTarget |
| `status_code` | int or None | HTTP status code |
| `response_body` | str or None | Raw response body |
| `error` | str or None | Error message if failed |
| `fetched_at` | datetime | When the fetch occurred |

## SQLite Schema

```sql
CREATE TABLE resources (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    url TEXT NOT NULL,
    provider_json TEXT,
    skills_json TEXT,
    auth_json TEXT,
    raw_json TEXT NOT NULL,
    resource_type TEXT DEFAULT 'a2a-agent',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE crawl_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'pending',
    discovered_at TEXT NOT NULL,
    last_attempt TEXT,
    error TEXT
);

CREATE TABLE crawl_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crawl_job_id INTEGER NOT NULL REFERENCES crawl_jobs(id),
    status_code INTEGER,
    response_body TEXT,
    error TEXT,
    fetched_at TEXT NOT NULL
);
```

## Identifier Format

```
urn:air:<publisher>:<namespace>:<name>
```

Example: `urn:air:hashgen:agents:resume-parser`

For unverified publishers, a hash-based fallback is used:

```
urn:air:unverified:<sha256-of-card-url>:<slug>
```
