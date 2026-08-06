"""SQLite persistence for the A2A Hub MVP."""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS resources (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    endpoint_url TEXT NOT NULL,
    publisher TEXT,
    skills TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crawl_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crawl_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    status_code INTEGER,
    error TEXT,
    fetched_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_resources_name ON resources(name);
CREATE INDEX IF NOT EXISTS idx_crawl_results_url ON crawl_results(url);
"""


class Database:
    """Thin SQLite wrapper for schema initialization and connections."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def connect(self) -> sqlite3.Connection:
        """Open a connection with row factory and foreign keys enabled."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def initialize(self) -> None:
        """Create MVP tables and indexes if they do not exist."""
        logger.info(
            "Initializing SQLite database",
            extra={"fields": {"database_path": str(self.path)}},
        )
        with self.connect() as conn:
            conn.executescript(SCHEMA_SQL)
            conn.commit()
        logger.info("SQLite schema ready")

    def table_names(self) -> list[str]:
        """Return user table names (excludes sqlite internal tables)."""
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            ).fetchall()
        return [str(row["name"]) for row in rows]
