"""Persistence helpers for crawl jobs and raw crawl results."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from a2a_hub.models.crawl import CrawlJobStatus, CrawlResult
from a2a_hub.store.database import Database


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class CrawlRepository:
    """SQLite access for crawl_jobs / crawl_results (no Resource writes)."""

    def __init__(self, db: Database) -> None:
        self._db = db

    def create_job(self, *, status: CrawlJobStatus = CrawlJobStatus.RUNNING) -> int:
        with self._db.connect() as conn:
            cur = conn.execute(
                "INSERT INTO crawl_jobs (started_at, completed_at, status) VALUES (?, NULL, ?)",
                (_utc_now_iso(), status.value),
            )
            conn.commit()
            job_id = cur.lastrowid
        if job_id is None:
            raise RuntimeError("Failed to create crawl job")
        return int(job_id)

    def finish_job(
        self,
        job_id: int,
        *,
        status: CrawlJobStatus,
        completed_at: datetime | None = None,
    ) -> None:
        done = (completed_at or datetime.now(timezone.utc)).isoformat()
        with self._db.connect() as conn:
            conn.execute(
                "UPDATE crawl_jobs SET completed_at = ?, status = ? WHERE id = ?",
                (done, status.value, job_id),
            )
            conn.commit()

    def insert_result(self, result: CrawlResult) -> int:
        headers_json = (
            json.dumps(result.headers, default=str) if result.headers is not None else None
        )
        with self._db.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO crawl_results (
                    url, status_code, error, fetched_at,
                    response_body, content_type, headers, duration_ms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result.url,
                    result.status_code,
                    result.error,
                    result.fetched_at.isoformat(),
                    result.response_body,
                    result.content_type,
                    headers_json,
                    result.duration_ms,
                ),
            )
            conn.commit()
            row_id = cur.lastrowid
        if row_id is None:
            raise RuntimeError("Failed to insert crawl result")
        return int(row_id)

    def list_results(self) -> list[CrawlResult]:
        with self._db.connect() as conn:
            rows = conn.execute(
                """
                SELECT id, url, status_code, error, fetched_at,
                       response_body, content_type, headers, duration_ms
                FROM crawl_results
                ORDER BY id
                """
            ).fetchall()

        results: list[CrawlResult] = []
        for row in rows:
            headers = json.loads(row["headers"]) if row["headers"] else None
            results.append(
                CrawlResult(
                    id=int(row["id"]),
                    url=str(row["url"]),
                    status_code=row["status_code"],
                    error=row["error"],
                    fetched_at=datetime.fromisoformat(str(row["fetched_at"])),
                    response_body=row["response_body"],
                    content_type=row["content_type"],
                    headers=headers,
                    duration_ms=row["duration_ms"],
                )
            )
        return results

    def count_results(self) -> int:
        with self._db.connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS c FROM crawl_results").fetchone()
        return int(row["c"]) if row else 0
