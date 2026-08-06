# ADR-008: No Background Workers in MVP

**Status:** Accepted
**Date:** 2026-08-06

## Context

The MVP could use background workers for continuous crawling, health checking, or other periodic tasks.

## Decision

Do not use background workers in the MVP. The crawler runs synchronously on startup or via CLI command.

## Rationale

- Background workers add infrastructure complexity (Redis, Celery, or threading)
- The MVP crawl is a batch operation — run once, verify results, done
- Continuous crawling is Phase 2 work
- Single process is simpler to deploy, debug, and reason about
- No need for job queues, retry queues, or worker orchestration

## Consequences

- Crawl blocks the process while running (acceptable for batch operation)
- No continuous crawl loop (Phase 2)
- No real-time health monitoring (Phase 2)
- Process restart required to re-crawl (acceptable for MVP)

## Replaced By

Background worker with crawl scheduler (Phase 2)
