"""Database initialization tests."""

from __future__ import annotations

from pathlib import Path

from a2a_hub.store.database import Database


def test_database_initialize_creates_mvp_tables(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    db = Database(db_path)

    db.initialize()

    assert db_path.exists()
    assert db.table_names() == ["crawl_jobs", "crawl_results", "resources"]


def test_database_initialize_is_idempotent(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    db = Database(db_path)

    db.initialize()
    db.initialize()

    assert db.table_names() == ["crawl_jobs", "crawl_results", "resources"]


def test_resources_table_columns(tmp_path: Path) -> None:
    db = Database(tmp_path / "test.db")
    db.initialize()

    with db.connect() as conn:
        rows = conn.execute("PRAGMA table_info(resources)").fetchall()

    columns = {row["name"] for row in rows}
    assert columns == {
        "id",
        "name",
        "description",
        "endpoint_url",
        "publisher",
        "skills",
        "created_at",
        "updated_at",
    }
