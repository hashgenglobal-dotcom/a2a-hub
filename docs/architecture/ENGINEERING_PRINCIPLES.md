# A2A Hub — Engineering Principles

---

## 1. Standards Alignment

### 1.1 Build on Standards, Don't Create Them

A2A Hub is infrastructure. Infrastructure must be compatible, not novel.

| Standard | Relationship | Status |
|----------|-------------|--------|
| A2A v1.0 | Agent Card schema, protocol operations | ✅ Adopted |
| ARDS v0.9 | Discovery API, federation, identifiers | ⚠️ Monitoring (Phase 2) |
| MCP | Tool/resource discovery | ⚠️ Phase 2 |
| `urn:air:` | Resource identifier format | ✅ Adopted |

**Rule:** If a standard exists for a problem, use it. Only invent when no standard exists.

### 1.2 Conformance Over Innovation

Build to the spec, not past it. Extensions must be optional and clearly documented.

---

## 2. Replaceability

Every subsystem must be replaceable without changing other subsystems.

| Subsystem | Can be replaced by | When |
|-----------|-------------------|------|
| Crawler | Any HTTP client | Any time |
| Parser | Any validation library | Any time |
| Store | PostgreSQL, any DB | Phase 2 |
| Search | Full-text search, vector search | Phase 2 |
| UI | React, Vue, any framework | Phase 2 |
| Protocol adapter | MCP, ARDS, any protocol | Phase 2 |

**Rule:** No layer depends on the implementation details of another layer. The Resource model is the contract between layers.

---

## 3. Simplicity

### 3.1 SQLite for MVP, PostgreSQL at Scale

Do not add infrastructure before you have users. SQLite handles thousands of resources. PostgreSQL + pgvector is for when you have tens of thousands.

**Rule:** If SQLite works, use SQLite. Only add PostgreSQL when you have evidence that SQLite is the bottleneck.

### 3.2 Single Process for MVP

The entire A2A Hub runs as a single process for the MVP. The crawler, API, and UI share the same process. Separation into services happens when load demands it.

**Rule:** Monolith first. Microservices when proven necessary.

### 3.3 No Premature Optimization

Do not optimize for scale, performance, or enterprise before the MVP validates the concept.

**Rule:** If it is not needed for the 7 MVP capabilities, it does not belong in the MVP.

---

## 4. Security (MVP)

| Layer | Control |
|-------|---------|
| Network | HTTPS only (handled by deployment platform) |
| Data | Input validation (pydantic), schema enforcement |
| Crawler | Standard HTTP semantics, timeout enforcement |

**Rule:** Never trust a Resource Card's content without validation.

---

## 5. Compatibility

### 5.1 Backward Compatibility

API changes must be backward compatible within a major version. Breaking changes require a new API version and a deprecation period.

**Rule:** v1 endpoints will be supported for at least 12 months after v2 is released.

### 5.2 Graceful Degradation

If a downstream subsystem is unavailable, the API should still return results — they may just be less complete.

**Rule:** The search API must work even if the crawler has never run. The resource detail API must work even if health data is stale.

---

## 6. Open Source

### 6.1 Apache 2.0

A2A Hub is Apache 2.0 licensed. Permissive, business-friendly, and compatible with the A2A protocol's license.

### 6.2 Community First

The public registry is free. The open-source code is the product. Enterprise features are the business model.

**Rule:** Never gate basic discovery behind a paywall. Search is free. Trust and governance are the products.

### 6.3 Transparent Development

All decisions, discussions, and roadmap items are public. GitHub issues and discussions are the source of truth.

**Rule:** If it is not in a GitHub issue, it does not exist.
