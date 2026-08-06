"""Persistence helpers for crawl jobs, crawl results, and resources."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any

from a2a_hub.models.crawl import CrawlJobStatus, CrawlResult
from a2a_hub.models.resource import Resource
from a2a_hub.store.database import Database


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_now_iso() -> str:
    return _utc_now().isoformat()


def _skills_to_json(skills: list[Any]) -> str:
    return json.dumps(skills, default=str)


def _skills_from_json(raw: str | None) -> list[Any]:
    if not raw:
        return []
    data = json.loads(raw)
    return data if isinstance(data, list) else []


def _row_to_resource(row: sqlite3.Row) -> Resource:
    return Resource(
        id=str(row["id"]),
        name=str(row["name"]),
        description=row["description"],
        endpoint_url=str(row["endpoint_url"]),
        publisher=str(row["publisher"] or "unverified"),
        skills=_skills_from_json(row["skills"]),
        created_at=datetime.fromisoformat(str(row["created_at"])),
        updated_at=datetime.fromisoformat(str(row["updated_at"])),
    )


class CrawlRepository:
    """SQLite access for crawl_jobs / crawl_results."""

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
        done = (completed_at or _utc_now()).isoformat()
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


class ResourceRepository:
    """SQLite access for canonical Resources (upsert by stable id)."""

    def __init__(self, db: Database) -> None:
        self._db = db

    def get(self, resource_id: str) -> Resource | None:
        with self._db.connect() as conn:
            row = conn.execute(
                "SELECT * FROM resources WHERE id = ?",
                (resource_id,),
            ).fetchone()
        return _row_to_resource(row) if row else None

    def list_all(self) -> list[Resource]:
        with self._db.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM resources ORDER BY name COLLATE NOCASE"
            ).fetchall()
        return [_row_to_resource(row) for row in rows]

    def count(self) -> int:
        with self._db.connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS c FROM resources").fetchone()
        return int(row["c"]) if row else 0

    def upsert(self, resource: Resource) -> Resource:
        """Insert or update by resource id. Preserves created_at on update."""
        now = _utc_now()
        existing = self.get(resource.id)
        if existing is None:
            created = resource.created_at
            updated = resource.updated_at
            with self._db.connect() as conn:
                conn.execute(
                    """
                    INSERT INTO resources (
                        id, name, description, endpoint_url, publisher, skills,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        resource.id,
                        resource.name,
                        resource.description,
                        resource.endpoint_url,
                        resource.publisher,
                        _skills_to_json(resource.skills),
                        created.isoformat(),
                        updated.isoformat(),
                    ),
                )
                conn.commit()
            stored = self.get(resource.id)
            if stored is None:
                raise RuntimeError("Failed to insert resource")
            return stored

        with self._db.connect() as conn:
            conn.execute(
                """
                UPDATE resources SET
                    name = ?,
                    description = ?,
                    endpoint_url = ?,
                    publisher = ?,
                    skills = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    resource.name,
                    resource.description,
                    resource.endpoint_url,
                    resource.publisher,
                    _skills_to_json(resource.skills),
                    now.isoformat(),
                    resource.id,
                ),
            )
            conn.commit()
        stored = self.get(resource.id)
        if stored is None:
            raise RuntimeError("Failed to update resource")
        return stored
