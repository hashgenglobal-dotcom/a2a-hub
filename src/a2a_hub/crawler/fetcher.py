"""Async Agent Card fetcher (Discover → Fetch). Independent of FastAPI."""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import unquote, urlparse

import aiohttp

from a2a_hub.crawler.models import (
    ACCEPTABLE_CONTENT_TYPES,
    USER_AGENT,
    CrawlResult,
)

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _headers_to_dict(headers: Mapping[str, Any] | None) -> dict[str, str]:
    if headers is None:
        return {}
    return {str(k).lower(): str(v) for k, v in headers.items()}


def _is_acceptable_content_type(content_type: str | None) -> bool:
    if not content_type:
        return False
    lowered = content_type.lower().split(";")[0].strip()
    if lowered.endswith("+json"):
        return True
    return lowered in ACCEPTABLE_CONTENT_TYPES


async def _fetch_file(url: str) -> CrawlResult:
    """Read a local ``file:`` URL (deterministic fixtures; no network)."""
    started = time.perf_counter()
    parsed = urlparse(url)
    path = Path(unquote(parsed.path))
    try:
        body = path.read_text(encoding="utf-8")
        duration_ms = int((time.perf_counter() - started) * 1000)
        return CrawlResult(
            url=url,
            status_code=200,
            response_body=body,
            content_type="application/json",
            headers={"content-type": "application/json", "x-a2a-hub-source": "file"},
            fetched_at=_utc_now(),
            duration_ms=duration_ms,
            error=None,
        )
    except OSError as exc:
        duration_ms = int((time.perf_counter() - started) * 1000)
        return CrawlResult(
            url=url,
            status_code=None,
            response_body=None,
            content_type=None,
            headers=None,
            fetched_at=_utc_now(),
            duration_ms=duration_ms,
            error=f"file_error: {exc}",
        )


class Fetcher:
    """Fetch Agent Card URLs and return ``CrawlResult`` snapshots (raw body untouched)."""

    def __init__(
        self,
        *,
        timeout_seconds: float = 30.0,
        user_agent: str = USER_AGENT,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent
        self._session = session
        self._owns_session = session is None

    async def __aenter__(self) -> Fetcher:
        if self._session is None:
            timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)
            self._session = aiohttp.ClientSession(
                timeout=timeout,
                headers={"User-Agent": self.user_agent, "Accept": "application/json"},
            )
        return self

    async def __aexit__(self, *args: object) -> None:
        if self._owns_session and self._session is not None:
            await self._session.close()
            self._session = None

    async def fetch(self, url: str) -> CrawlResult:
        """Fetch one URL; never raises — failures are recorded on ``CrawlResult.error``."""
        if url.startswith("file:"):
            return await _fetch_file(url)

        if self._session is None:
            raise RuntimeError("Fetcher must be used as an async context manager")

        started = time.perf_counter()
        try:
            async with self._session.get(url) as response:
                body = await response.text(errors="replace")
                headers = _headers_to_dict(response.headers)
                content_type = headers.get("content-type")
                duration_ms = int((time.perf_counter() - started) * 1000)
                error: str | None = None

                if response.status != 200:
                    error = f"http_error: status {response.status}"
                elif not _is_acceptable_content_type(content_type):
                    error = f"invalid_content_type: {content_type!r}"

                return CrawlResult(
                    url=url,
                    status_code=response.status,
                    response_body=body,
                    content_type=content_type,
                    headers=headers,
                    fetched_at=_utc_now(),
                    duration_ms=duration_ms,
                    error=error,
                )
        except TimeoutError:
            # asyncio.TimeoutError is an alias of TimeoutError on 3.11+
            duration_ms = int((time.perf_counter() - started) * 1000)
            return CrawlResult(
                url=url,
                status_code=None,
                response_body=None,
                content_type=None,
                headers=None,
                fetched_at=_utc_now(),
                duration_ms=duration_ms,
                error="timeout",
            )
        except aiohttp.ClientError as exc:
            duration_ms = int((time.perf_counter() - started) * 1000)
            return CrawlResult(
                url=url,
                status_code=None,
                response_body=None,
                content_type=None,
                headers=None,
                fetched_at=_utc_now(),
                duration_ms=duration_ms,
                error=f"connection_error: {exc}",
            )


async def fetch_all(
    urls: list[str],
    *,
    timeout_seconds: float = 30.0,
) -> list[CrawlResult]:
    """Fetch many URLs sequentially (simple MVP; no concurrency tuning)."""
    results: list[CrawlResult] = []
    async with Fetcher(timeout_seconds=timeout_seconds) as fetcher:
        for url in urls:
            result = await fetcher.fetch(url)
            logger.info(
                "Fetched seed URL",
                extra={
                    "fields": {
                        "url": url,
                        "status_code": result.status_code,
                        "error": result.error,
                        "duration_ms": result.duration_ms,
                    }
                },
            )
            results.append(result)
    return results
