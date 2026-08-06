"""SQLite persistence with ordered SQL migrations."""

from __future__ import annotations

import logging
import sqlite3
from datetime import datetime, timezone
from importlib import resources
from pathlib import Path

logger = logging.getLogger(__name__)

_MIGRATIONS_PACKAGE = "a2a_hub.store.migrations"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Database:
    """Thin SQLite wrapper: connections + schema migrations."""

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
        """Apply all pending SQL migrations in version order."""
        logger.info(
            "Initializing SQLite database",
            extra={"fields": {"database_path": str(self.path)}},
        )
        with self.connect() as conn:
            self._ensure_migrations_table(conn)
            applied = self._applied_versions(conn)
            for version, sql in self._load_migrations():
                if version in applied:
                    continue
                logger.info(
                    "Applying migration",
                    extra={"fields": {"version": version}},
                )
                conn.executescript(sql)
                conn.execute(
                    "INSERT INTO schema_migrations (version, applied_at) VALUES (?, ?)",
                    (version, _utc_now_iso()),
                )
                conn.commit()
        logger.info("SQLite schema ready")

    def table_names(self) -> list[str]:
        """Return user table names (excludes sqlite internal tables)."""
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name NOT LIKE 'sqlite_%' "
                "ORDER BY name"
            ).fetchall()
        return [str(row["name"]) for row in rows]

    def applied_migrations(self) -> list[str]:
        """Return applied migration versions in order."""
        with self.connect() as conn:
            self._ensure_migrations_table(conn)
            rows = conn.execute(
                "SELECT version FROM schema_migrations ORDER BY version"
            ).fetchall()
        return [str(row["version"]) for row in rows]

    def column_names(self, table: str) -> set[str]:
        """Return column names for a table."""
        with self.connect() as conn:
            rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
        return {str(row["name"]) for row in rows}

    @staticmethod
    def _ensure_migrations_table(conn: sqlite3.Connection) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version TEXT PRIMARY KEY,
                applied_at TEXT NOT NULL
            )
            """
        )
        conn.commit()

    @staticmethod
    def _applied_versions(conn: sqlite3.Connection) -> set[str]:
        rows = conn.execute("SELECT version FROM schema_migrations").fetchall()
        return {str(row["version"]) for row in rows}

    @staticmethod
    def _load_migrations() -> list[tuple[str, str]]:
        """Load `NNN_name.sql` files from the migrations package."""
        migration_root = resources.files(_MIGRATIONS_PACKAGE)
        items: list[tuple[str, str]] = []
        for entry in migration_root.iterdir():
            name = entry.name
            if not name.endswith(".sql"):
                continue
            version = name[: -len(".sql")]
            sql = entry.read_text(encoding="utf-8")
            items.append((version, sql))
        items.sort(key=lambda item: item[0])
        return items
