# ADR-002: Resource as the Canonical Entity

**Status:** Accepted
**Date:** 2026-08-06

## Context

The platform ingests A2A Agent Cards. The domain model must decide whether to store Agent Cards directly or normalize them into a platform-agnostic entity.

## Decision

Define `Resource` as the canonical entity. Agent Cards are parser inputs only.

## Rationale

- Protocol-agnostic — the platform should not depend on A2A-specific types
- Future-proof — MCP servers, skills, APIs, and workflows all become Resources
- Replaceability — the A2A adapter can be replaced without changing the core model
- Clarity — the domain model reflects the platform's business, not the protocol's

## Consequences

- A2A-specific fields are extracted and mapped to Resource fields
- Raw JSON is preserved for re-validation
- New protocols require new adapters, not model changes
- The Resource model is the contract between all subsystems

## Relationship

```
Raw Agent Card → A2A Adapter → Resource → SQLite
```
