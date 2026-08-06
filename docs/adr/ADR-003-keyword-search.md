# ADR-003: Keyword Search for MVP

**Status:** Accepted
**Date:** 2026-08-06

## Context

The MVP needs to make resources searchable. Options include SQL LIKE, SQLite FTS5, or vector embeddings.

## Decision

Use SQL `LIKE` keyword search for the MVP.

## Rationale

- Zero additional dependencies — works with SQLite out of the box
- Sufficient for MVP scale (tens to hundreds of resources)
- Simple to implement and reason about
- Easy to replace with FTS5 or vector search in Phase 2
- No embedding model, no vector database, no external API calls

## Consequences

- No semantic search (cannot match "FX" to "foreign exchange")
- No relevance ranking beyond simple matching
- Case-insensitive search requires explicit handling
- Upgrade to FTS5 or vector search is Phase 2 work

## Replaced By

SQLite FTS5 (P1) or vector search with pgvector (Phase 2)
