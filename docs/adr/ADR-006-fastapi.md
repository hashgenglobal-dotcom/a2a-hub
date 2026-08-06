# ADR-006: FastAPI as API Framework

**Status:** Accepted
**Date:** 2026-08-06

## Context

The MVP needs an HTTP API framework. Options include FastAPI, Flask, Django, and Starlette.

## Decision

Use FastAPI.

## Rationale

- Async by default — compatible with aiohttp-based crawler
- Auto-generated OpenAPI docs — zero effort API documentation
- Built-in pydantic integration — natural fit for schema validation
- Single-process friendly — Uvicorn runs FastAPI in one process
- Large ecosystem and community

## Consequences

- FastAPI auto-generates `/docs` and `/redoc` endpoints (free documentation)
- No need for separate OpenAPI spec generation
- Dependency injection via `Depends()` for clean separation
- ASGI deployment compatible with any ASGI server

## Replaced By

Not replaced. FastAPI is suitable for all phases.
