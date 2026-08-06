"""Crawler-layer types. Domain ``CrawlResult`` remains the persisted shape."""

from __future__ import annotations

from a2a_hub.models.crawl import CrawlJob, CrawlJobStatus, CrawlResult

USER_AGENT = "A2A-Hub-Crawler/0.1"

# Content types accepted for Agent Card payloads (substring match, case-insensitive)
ACCEPTABLE_CONTENT_TYPES = (
    "application/json",
    "text/json",
    "application/ld+json",
)

__all__ = [
    "ACCEPTABLE_CONTENT_TYPES",
    "CrawlJob",
    "CrawlJobStatus",
    "CrawlResult",
    "USER_AGENT",
]
