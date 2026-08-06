"""Crawl orchestration: load seeds → fetch → persist crawl_results (no parse)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

from a2a_hub.crawler.fetcher import fetch_all
from a2a_hub.crawler.seeds import load_seed_urls
from a2a_hub.models.crawl import CrawlJobStatus, CrawlResult
from a2a_hub.store.database import Database
from a2a_hub.store.repository import CrawlRepository

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _job_status_for(results: list[CrawlResult]) -> CrawlJobStatus:
    if not results:
        return CrawlJobStatus.FAILED
    if all(r.error is not None for r in results):
        return CrawlJobStatus.FAILED
    return CrawlJobStatus.COMPLETE


async def run_crawl(
    db: Database,
    *,
    seeds_path: Path | None = None,
    timeout_seconds: float = 30.0,
) -> list[CrawlResult]:
    """Execute Discover → Fetch and store raw results. No validation/normalize."""
    repo = CrawlRepository(db)
    urls = load_seed_urls(seeds_path=seeds_path)
    job_id = repo.create_job(status=CrawlJobStatus.RUNNING)

    logger.info(
        "Starting crawl job",
        extra={"fields": {"job_id": job_id, "seed_count": len(urls)}},
    )

    try:
        results = await fetch_all(urls, timeout_seconds=timeout_seconds)
        for result in results:
            repo.insert_result(result)

        final_status = _job_status_for(results)
        repo.finish_job(job_id, status=final_status, completed_at=_utc_now())
        logger.info(
            "Crawl job finished",
            extra={
                "fields": {
                    "job_id": job_id,
                    "status": final_status.value,
                    "results": len(results),
                    "errors": sum(1 for r in results if r.error),
                }
            },
        )
        return results
    except Exception:
        repo.finish_job(job_id, status=CrawlJobStatus.FAILED, completed_at=_utc_now())
        raise
