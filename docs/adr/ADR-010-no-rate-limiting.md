# ADR-010: No Rate Limiting in MVP

**Status:** Accepted
**Date:** 2026-08-06

## Context

The MVP API could include rate limiting to prevent abuse.

## Decision

Do not implement rate limiting in the MVP.

## Rationale

- Premature optimization — rate limiting solves a problem that may never occur
- The MVP is a public, read-only API with no write endpoints
- Rate limiting adds complexity (middleware, state storage, header management)
- Can be added when abuse is observed, not before
- Deployment platform (Railway/Fly.io/Render) may provide basic rate limiting

## Consequences

- No protection against aggressive clients (acceptable for MVP)
- No rate limit headers in API responses
- Rate limiting is Phase 2 work

## Replaced By

Rate limiting middleware (Phase 2, when abuse is observed or write endpoints are added)
