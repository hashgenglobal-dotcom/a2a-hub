"""Application startup smoke tests."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from a2a_hub.api.app import create_app
from a2a_hub.config import Settings
from a2a_hub.main import build_parser, cmd_crawl


def test_health_endpoint_starts_and_returns_ok(tmp_path: Path) -> None:
    settings = Settings(database_path=tmp_path / "app.db", log_level="WARNING")
    app = create_app(settings)

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["resources_count"] == 0
    assert (tmp_path / "app.db").exists()


def test_cli_parser_requires_command() -> None:
    parser = build_parser()
    assert parser.parse_args(["crawl"]).command == "crawl"
    assert parser.parse_args(["serve"]).command == "serve"


def test_cmd_crawl_initializes_database(tmp_path: Path) -> None:
    settings = Settings(database_path=tmp_path / "crawl.db", log_level="WARNING")
    code = cmd_crawl(settings)

    assert code == 0
    assert (tmp_path / "crawl.db").exists()
