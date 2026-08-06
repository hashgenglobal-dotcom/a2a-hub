"""Database initialization and migration tests."""

from __future__ import annotations

from pathlib import Path

from a2a_hub.store.database import Database


def test_database_initialize_creates_mvp_tables(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    db = Database(db_path)

    db.initialize()

    assert db_path.exists()
    assert set(db.table_names()) == {
        "crawl_jobs",
        "crawl_results",
        "resources",
        "schema_migrations",
    }


def test_database_initialize_is_idempotent(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    db = Database(db_path)

    db.initialize()
    db.initialize()

    assert db.applied_migrations() == ["001_initial", "002_add_raw_crawl"]


def test_resources_table_columns(tmp_path: Path) -> None:
    db = Database(tmp_path / "test.db")
    db.initialize()

    assert db.column_names("resources") == {
        "id",
        "name",
        "description",
        "endpoint_url",
        "publisher",
        "skills",
        "created_at",
        "updated_at",
    }


def test_crawl_results_include_raw_payload_columns(tmp_path: Path) -> None:
    db = Database(tmp_path / "test.db")
    db.initialize()

    columns = db.column_names("crawl_results")
    assert {
        "id",
        "url",
        "status_code",
        "error",
        "fetched_at",
        "response_body",
        "content_type",
        "headers",
        "duration_ms",
    } <= columns
