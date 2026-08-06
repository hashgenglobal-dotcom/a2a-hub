# ADR-001: Use SQLite for MVP Storage

**Status:** Accepted
**Date:** 2026-08-06

## Context

The MVP needs to store Resource Cards, crawl jobs, and search results. The storage layer must be simple, require zero infrastructure, and be easy to replace later.

## Decision

Use SQLite as the MVP storage engine.

## Rationale

- Zero infrastructure — single file, no server process
- No external dependencies — built into Python stdlib
- Sufficient for thousands of resources
- Easy to replace with PostgreSQL + pgvector in Phase 2
- SQLite handles concurrent reads well (single writer, multiple readers)

## Consequences

- Not suitable for high write throughput (not an MVP concern)
- No native vector search (Phase 2)
- Migration to PostgreSQL required at scale
- Schema changes require migration logic (not automatic)

## Replaced By

PostgreSQL + pgvector (Phase 2, when >1,000 resources)
