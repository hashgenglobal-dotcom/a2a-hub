# A2A Hub — Domain Model (Target)

**This document describes the full target domain model.**

For the current MVP domain model, see `DOMAIN_MODEL_MVP.md`.

---

## Overview

The target domain model extends the MVP model with entities for trust, health, reputation, and ecosystem intelligence. These are not built in the MVP.

## Additional Entities (Phase 2+)

### Organization

An entity that publishes or owns resources.

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Unique identifier |
| `name` | str | Organization name |
| `description` | str | What the organization does |
| `website` | str | Organization website |
| `verified` | bool | Whether the organization has been verified |
| `resource_count` | int | Number of resources published |
| `created_at` | datetime | When first seen |

### Skill (Capability)

A discrete capability a resource exposes.

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Unique skill identifier |
| `name` | str | Human-readable name |
| `description` | str | What the skill does |
| `category` | str | Skill category |
| `embedding` | list[float] | Vector for semantic matching |

### HealthRecord

A single health check result.

| Field | Type | Description |
|-------|------|-------------|
| `resource_id` | str | Which resource was checked |
| `timestamp` | datetime | When the check was performed |
| `alive` | bool | Whether the endpoint responded |
| `status_code` | int | HTTP status code |
| `response_time_ms` | int | Response time in milliseconds |
| `error` | str | Error message if check failed |

### TrustRecord

A verification result.

| Field | Type | Description |
|-------|------|-------------|
| `resource_id` | str | Which resource was verified |
| `timestamp` | datetime | When verification was performed |
| `identity_verified` | bool | Domain ownership + card signature valid |
| `signature_valid` | bool | Resource Card signature verified |
| `security_score` | float | 0-100 security assessment |
| `trust_score` | float | 0-100 composite trust score |

### Protocol

A communication protocol a resource supports.

| Field | Type | Description |
|-------|------|-------------|
| `type` | str | `A2A_AGENT`, `MCP_SERVER`, `OPENAPI`, `CUSTOM` |
| `version` | str | Protocol version |
| `interfaces` | list[str] | Supported interfaces |

### AuthScheme

An authentication method supported by a resource.

| Field | Type | Description |
|-------|------|-------------|
| `type` | str | `apiKey`, `oauth2`, `http`, `openIdConnect`, `mutualTls` |
| `in` | str | Where the credential is sent (`header`, `query`, `cookie`) |
| `name` | str | Header or parameter name |

## Event Model (Phase 2+)

| Event | Trigger | Payload |
|-------|---------|---------|
| `resource.discovered` | Crawler finds new Resource Card | `{ resource_id, card_url, source }` |
| `resource.updated` | Re-crawl finds changed card | `{ resource_id, diff }` |
| `resource.removed` | Resource Card no longer reachable | `{ resource_id, last_seen }` |
| `health.check.completed` | Health probe finishes | `{ resource_id, alive, response_time_ms }` |
| `health.alert.triggered` | Resource fails N consecutive checks | `{ resource_id, failures }` |
| `trust.score.updated` | Trust score recalculated | `{ resource_id, old_score, new_score }` |
| `crawl.target.discovered` | New URL found for crawling | `{ url, source, priority }` |
| `crawl.target.completed` | Crawl finishes | `{ url, status, resource_id, error }` |
