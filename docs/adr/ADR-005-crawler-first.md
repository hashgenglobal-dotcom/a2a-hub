# ADR-005: Crawler-First Over Registration-First

**Status:** Accepted
**Date:** 2026-08-06

## Context

The platform needs to discover A2A Agent Cards. Two approaches: wait for agents to register, or crawl the internet to find them.

## Decision

Use a crawler-first approach. Discover agents proactively rather than waiting for opt-in registration.

## Rationale

- Mirrors how the web grew — Google crawls websites, it does not wait for registration
- Solves the chicken-and-egg problem — no agents registered means no users, no users means no agents
- Registration is a Phase 2 feature that adds value on top of an existing index
- The A2A spec defines a well-known URL path (`/.well-known/agent.json`) — this is designed for crawling

## Consequences

- No `POST /register` endpoint in MVP
- Seed URLs must be manually curated initially
- Crawl coverage depends on seed quality
- Registration API is Phase 2 work

## Replaced By

`POST /register` endpoint (Phase 2, when the index has critical mass)
