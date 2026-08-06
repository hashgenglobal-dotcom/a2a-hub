# ADR-009: No Authentication in MVP

**Status:** Accepted
**Date:** 2026-08-06

## Context

The MVP API could include authentication for write operations or rate limiting.

## Decision

Do not implement authentication in the MVP. The API is public and read-only.

## Rationale

- The MVP has no write endpoints (no `POST /register`, no user accounts)
- Authentication adds complexity without validated need
- Public read-only APIs are standard for open-source infrastructure projects
- Rate limiting and auth can be added when abuse is observed, not before

## Consequences

- Anyone can query the API without credentials
- No rate limiting (acceptable for MVP scale)
- No API keys, no OAuth, no user management
- Authentication is Phase 2+ work

## Replaced By

API key authentication (Phase 2, when write endpoints are added)
OAuth2 (Phase 3, for enterprise features)
