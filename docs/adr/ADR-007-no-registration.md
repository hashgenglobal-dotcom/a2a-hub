# ADR-007: No Registration Endpoint in MVP

**Status:** Accepted
**Date:** 2026-08-06

## Context

The MVP could include a `POST /register` endpoint for agents to submit their URLs for indexing.

## Decision

Do not include `POST /register` in the MVP.

## Rationale

- Registration does not validate the business — discovery does
- The crawler-first approach (ADR-005) makes registration unnecessary for MVP
- Registration adds API surface area, validation logic, and abuse vectors
- A registration endpoint without an index is useless
- The index must exist first; registration adds value on top

## Consequences

- All agent discovery is crawler-driven in MVP
- No user-submitted URLs
- No rate limiting or abuse prevention needed
- Registration API is Phase 2 work

## Replaced By

`POST /register` endpoint (Phase 2)
