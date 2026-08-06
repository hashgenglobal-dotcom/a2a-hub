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

---

## 2026-08-06 — Sprint 1 Day 1

**Decision:** Hybrid seeds (checked-in sample Agent Cards + configurable URL list). Tests must not require live external agents.
**Reason:** Deterministic CI and local development; real public URLs can be added later without changing the crawl pipeline.
**Reference:** Product approval for Sprint 1 Day 1

**Decision:** Tolerant Agent Card validation (required: name, endpoint URL, valid JSON). Optional fields warn; raw crawl payloads preserved for debugging (Day 2+).
**Reason:** Real-world cards are often incomplete; rejecting them would empty the index.
**Reference:** Product approval for Sprint 1 Day 1

**Decision:** Resource IDs are stable hashes of the canonical Agent Card URL; publisher is always `unverified` in MVP.
**Reason:** No trust verification in MVP; Resource remains the canonical entity (ADR-002).
**Reference:** Product approval for Sprint 1 Day 1; ADR-002

**Decision:** CLI crawl only — never start crawl on `serve` (no workers, no schedulers).
**Reason:** Reinforces ADR-008; keeps API boot non-blocking on PaaS.
**Reference:** ADR-008; product approval for Sprint 1 Day 1

**Decision:** Day 1 SQLite schema uses `endpoint_url` / `publisher` / `skills` on `resources`, batch-oriented `crawl_jobs`, and URL-level `crawl_results`.
**Reason:** Matches approved Day 1 foundation columns; richer DOMAIN_MODEL_MVP fields (`raw_json`, auth, etc.) land with parse/store work.
**Reference:** Sprint 1 Day 1 implementation

**Decision:** Add raw crawl columns before Day 2 (`response_body`, `content_type`, `headers`, `duration_ms`) via migration `002_add_raw_crawl`.
**Reason:** Debugging validation failures requires the original HTTP payload and metadata.
**Reference:** Pre-Day 2 product adjustment

**Decision:** Introduce ordered SQL migrations (`store/migrations/*.sql` + `schema_migrations` table) before the schema grows further.
**Reason:** `CREATE TABLE IF NOT EXISTS` alone does not support additive evolution safely.
**Reference:** Pre-Day 2 product adjustment

**Decision:** Domain models (`RawAgentCard`, `Resource`, `CrawlJob`/`CrawlResult`) exist before the crawler.
**Reason:** HTTP output must not become the database model; flow is HTTP → RawAgentCard → Validator → Resource → SQLite.
**Reference:** Pre-Day 2 product adjustment; ADR-002
