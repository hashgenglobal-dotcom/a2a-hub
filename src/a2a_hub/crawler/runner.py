"""Crawl orchestration: Discover → Fetch → Validate → Normalize → Store Resource."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from a2a_hub.crawler.fetcher import fetch_all
from a2a_hub.crawler.seeds import load_seed_urls
from a2a_hub.models.crawl import CrawlJobStatus, CrawlResult
from a2a_hub.models.resource import Resource
from a2a_hub.parser.adapter import AdaptOutcome, adapt_crawl_result
from a2a_hub.store.database import Database
from a2a_hub.store.repository import CrawlRepository, ResourceRepository

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _job_status_for(results: list[CrawlResult]) -> CrawlJobStatus:
    if not results:
        return CrawlJobStatus.FAILED
    if all(r.error is not None for r in results):
        return CrawlJobStatus.FAILED
    return CrawlJobStatus.COMPLETE


class CrawlRunSummary(BaseModel):
    """Summary of a full crawl+adapt run."""

    crawl_results: list[CrawlResult] = Field(default_factory=list)
    outcomes: list[AdaptOutcome] = Field(default_factory=list)
    resources: list[Resource] = Field(default_factory=list)

    @property
    def fetch_errors(self) -> int:
        return sum(1 for r in self.crawl_results if r.error)

    @property
    def resources_upserted(self) -> int:
        return len(self.resources)


async def run_crawl(
    db: Database,
    *,
    seeds_path: Path | None = None,
    timeout_seconds: float = 30.0,
) -> CrawlRunSummary:
    """Fetch seeds, store raw results, then adapt valid cards into Resources."""
    crawl_repo = CrawlRepository(db)
    resource_repo = ResourceRepository(db)
    urls = load_seed_urls(seeds_path=seeds_path)
    job_id = crawl_repo.create_job(status=CrawlJobStatus.RUNNING)

    logger.info(
        "Starting crawl job",
        extra={"fields": {"job_id": job_id, "seed_count": len(urls)}},
    )

    try:
        results = await fetch_all(urls, timeout_seconds=timeout_seconds)
        for result in results:
            crawl_repo.insert_result(result)

        outcomes: list[AdaptOutcome] = []
        resources: list[Resource] = []
        for result in results:
            outcome = adapt_crawl_result(result)
            outcomes.append(outcome)
            if outcome.resource is not None:
                stored = resource_repo.upsert(outcome.resource)
                resources.append(stored)
                logger.info(
                    "Upserted resource",
                    extra={
                        "fields": {
                            "resource_id": stored.id,
                            "name": stored.name,
                            "card_url": outcome.card_url,
                        }
                    },
                )

        final_status = _job_status_for(results)
        crawl_repo.finish_job(job_id, status=final_status, completed_at=_utc_now())
        logger.info(
            "Crawl job finished",
            extra={
                "fields": {
                    "job_id": job_id,
                    "status": final_status.value,
                    "results": len(results),
                    "fetch_errors": sum(1 for r in results if r.error),
                    "resources_upserted": len(resources),
                }
            },
        )
        return CrawlRunSummary(
            crawl_results=results,
            outcomes=outcomes,
            resources=resources,
        )
    except Exception:
        crawl_repo.finish_job(job_id, status=CrawlJobStatus.FAILED, completed_at=_utc_now())
        raise
