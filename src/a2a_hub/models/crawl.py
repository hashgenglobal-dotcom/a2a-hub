"""Crawl job and result models (HTTP fetch layer).

CrawlResult preserves raw response data for debugging validation failures.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class CrawlJobStatus(StrEnum):
    """Lifecycle status for a batch crawl run."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"


class CrawlJob(BaseModel):
    """One batch crawl execution (CLI crawl invocation)."""

    id: int | None = None
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None
    status: CrawlJobStatus = CrawlJobStatus.PENDING


class CrawlResult(BaseModel):
    """Outcome of fetching a single Agent Card URL."""

    id: int | None = None
    url: str
    status_code: int | None = None
    error: str | None = None
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    response_body: str | None = None
    content_type: str | None = None
    headers: dict[str, Any] | None = None
    duration_ms: int | None = None
