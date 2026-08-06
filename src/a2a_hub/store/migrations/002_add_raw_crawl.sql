-- 002_add_raw_crawl.sql
-- Preserve raw HTTP responses for Agent Card debugging (pre-Day 2)

ALTER TABLE crawl_results ADD COLUMN response_body TEXT;
ALTER TABLE crawl_results ADD COLUMN content_type TEXT;
ALTER TABLE crawl_results ADD COLUMN headers TEXT;
ALTER TABLE crawl_results ADD COLUMN duration_ms INTEGER;
