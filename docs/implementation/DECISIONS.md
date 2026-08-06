# Decisions

Engineering diary for A2A Hub. Each entry records a decision, its rationale, and the ADR that formalizes it.

---

## 2026-08-06

**Decision:** SQLite instead of PostgreSQL.
**Reason:** Solo developer. Zero infrastructure. Easy deployment. Sufficient for thousands of resources.
**Reference:** ADR-001

**Decision:** Resource as canonical entity instead of Agent Card.
**Reason:** Protocol-agnostic. Future-proof for MCP, skills, APIs. Keeps core model stable across protocol changes.
**Reference:** ADR-002

**Decision:** Keyword search instead of semantic/vector search.
**Reason:** Zero additional dependencies. Sufficient for MVP scale. Easy to replace later.
**Reference:** ADR-003

**Decision:** Single process instead of microservices.
**Reason:** Simplest deployment. No background workers. No Redis, Celery, or Kafka.
**Reference:** ADR-004

**Decision:** Crawler-first instead of registration-first.
**Reason:** Solves chicken-and-egg problem. Mirrors how the web grew. Registration adds value on top of an existing index.
**Reference:** ADR-005

**Decision:** FastAPI as API framework.
**Reason:** Async, auto-docs, pydantic integration, single-process friendly.
**Reference:** ADR-006

**Decision:** No registration endpoint in MVP.
**Reason:** Registration does not validate the business. Discovery does.
**Reference:** ADR-007

**Decision:** No background workers in MVP.
**Reason:** Crawl is a batch operation. Continuous crawling is Phase 2.
**Reference:** ADR-008

**Decision:** No authentication in MVP.
**Reason:** Public read-only API. Auth adds complexity without validated need.
**Reference:** ADR-009

**Decision:** No rate limiting in MVP.
**Reason:** Premature optimization. Add when abuse is observed.
**Reference:** ADR-010
