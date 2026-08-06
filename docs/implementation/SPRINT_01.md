# A2A Hub — Sprint 1 Plan

**Duration:** 5 days (Week 1)
**Goal:** Internet → SQLite working. Raw cards fetched, parsed, stored, searchable.

---

## Day 1 — Platform Foundation

**Deliverable:** Project setup, configuration, logging, SQLite initialization, testing framework.

### Tasks

- [ ] Initialize Python project with `pyproject.toml` (already exists)
- [ ] Create project layout: `src/a2a_hub/` with subdirectories
- [ ] Implement `config.py` — settings via pydantic-settings (env vars + defaults)
- [ ] Implement `main.py` — FastAPI app factory, CLI entry point (`crawl`, `serve` commands)
- [ ] Implement `store/database.py` — SQLite connection, table creation, migration
- [ ] Set up structured logging (JSON format, stdout)
- [ ] Set up pytest with `pytest-asyncio`
- [ ] Verify: `python -m a2a_hub` starts, `pytest` passes, SQLite initializes cleanly

### Files to Create

- `src/a2a_hub/config.py`
- `src/a2a_hub/main.py`
- `src/a2a_hub/store/database.py`
- `tests/test_database.py`

---

## Day 2 — Seed Discovery & Fetch

**Deliverable:** Seed URLs loaded, HTTP fetcher working, raw JSON stored in SQLite.

### Tasks

- [ ] Create `scripts/seed_urls.py` — hardcoded list of seed URLs from A2A partner list + known domains
- [ ] Implement `crawler/fetcher.py` — aiohttp-based HTTP fetcher with configurable timeout
- [ ] Implement crawl job creation (insert seed URLs into `crawl_jobs` table)
- [ ] Implement crawl execution (fetch URL, store result in `crawl_results` table)
- [ ] Implement basic error handling (timeout, connection error, non-200 status)
- [ ] Wire crawl command into CLI: `python -m a2a_hub crawl`
- [ ] Verify: crawl command fetches seed URLs, stores raw JSON, marks jobs as complete/failed

### Files to Create

- `scripts/seed_urls.py`
- `src/a2a_hub/crawler/fetcher.py`
- `tests/test_crawler.py`

---

## Day 3 — Parse & Validate

**Deliverable:** Raw JSON validated against A2A v1.0 schema, invalid cards rejected, valid cards normalized.

### Tasks

- [ ] Implement `models/resource.py` — pydantic models for Resource, CrawlTarget, CrawlResult
- [ ] Implement `parser/validator.py` — A2A v1.0 schema validation
- [ ] Implement A2A adapter: convert validated Agent Card → Resource model
- [ ] Implement `urn:air:` identifier generation
- [ ] Implement error reporting for invalid cards (log warning, skip card)
- [ ] Verify: valid cards produce Resource objects, invalid cards produce clear error messages

### Files to Create

- `src/a2a_hub/models/resource.py`
- `src/a2a_hub/parser/validator.py`
- `tests/test_parser.py`

---

## Day 4 — Store & Index

**Deliverable:** Resources persisted to SQLite with dedup, keyword search working.

### Tasks

- [ ] Implement `store/database.py` — insert/update resource, dedup by URL
- [ ] Implement keyword search over `name`, `description`, `skills` (SQL LIKE)
- [ ] Implement simple pagination (offset/limit)
- [ ] Wire crawl → parse → store pipeline in CLI command
- [ ] Verify: running crawl twice does not create duplicates, search returns results

### Files to Modify

- `src/a2a_hub/store/database.py` (add resource CRUD + search)
- `tests/test_database.py` (add search tests)

---

## Day 5 — End-to-End Pipeline

**Deliverable:** Full pipeline working end-to-end. Crawl → Parse → Store → Search verified.

### Tasks

- [ ] Integrate all components: CLI crawl command runs full pipeline
- [ ] Add smoke test: crawl seeds → verify resources in DB → verify search returns results
- [ ] Add `scripts/run_crawl.py` — convenience script for one-shot crawl
- [ ] Document seed URLs and expected output
- [ ] Verify: `python -m a2a_hub crawl` produces searchable resources

### Files to Create

- `scripts/run_crawl.py`

---

## Definition of Done (Week 1)

- [ ] `python -m a2a_hub crawl` fetches seed URLs, parses cards, stores resources
- [ ] `python -m a2a_hub serve` starts the API server
- [ ] SQLite database contains resources, crawl_jobs, crawl_results tables
- [ ] Search returns results for known queries
- [ ] Re-running crawl does not create duplicates
- [ ] All tests pass: `pytest`
