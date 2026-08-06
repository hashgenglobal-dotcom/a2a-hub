"""Crawler package — Discover → Fetch → (adapt via parser) → Resource."""

from a2a_hub.crawler.fetcher import Fetcher, fetch_all
from a2a_hub.crawler.models import USER_AGENT, CrawlResult
from a2a_hub.crawler.runner import CrawlRunSummary, run_crawl
from a2a_hub.crawler.seeds import load_seed_urls

__all__ = [
    "USER_AGENT",
    "CrawlResult",
    "CrawlRunSummary",
    "Fetcher",
    "fetch_all",
    "load_seed_urls",
    "run_crawl",
]
