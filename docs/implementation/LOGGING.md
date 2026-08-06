# Logging policy (MVP)

Structured JSON logs go to stdout via stdlib handlers.

## What we log

- Startup / shutdown (app name, version, database path, host/port)
- Crawl job progress (job id, seed counts, URL, HTTP status, error code, duration)
- Validation warnings/errors (URL, field code, message)
- Resource upserts (resource id, name, card URL)

## What we do not log

- Raw Agent Card / HTTP **response bodies**
- Authorization headers, cookies, or API keys
- Full request/response header maps (may contain secrets)

Raw payloads are stored in SQLite `crawl_results` for debugging, not emitted to logs.
