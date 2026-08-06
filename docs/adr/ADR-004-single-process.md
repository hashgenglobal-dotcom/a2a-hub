# ADR-004: Single Process for MVP

**Status:** Accepted
**Date:** 2026-08-06

## Context

The MVP needs to serve an API, run a crawler, and present a web UI. These could be separate services or a single process.

## Decision

Run the entire MVP as a single process. The crawler runs on startup or via CLI command, not as a background worker.

## Rationale

- Simplest possible deployment — one process, one port
- No background workers, no Redis, no Celery, no Kafka
- Crawl is a batch operation, not a continuous service
- Easy to reason about and debug
- Separation into services happens when load demands it

## Consequences

- Crawl blocks the process while running (acceptable for batch operation)
- No continuous crawl loop (Phase 2)
- No real-time health monitoring (Phase 2)
- Process restart required to re-crawl (acceptable for MVP)

## Replaced By

Separate crawler worker + API server (Phase 2, when crawl frequency increases)
